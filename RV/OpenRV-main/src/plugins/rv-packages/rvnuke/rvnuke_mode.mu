//
// Copyright (C) 2023  Autodesk, Inc. All Rights Reserved. 
// 
// SPDX-License-Identifier: Apache-2.0 
//

module: rvnuke_mode {

require rvtypes;
require commands;
require app_utils;
require extra_commands;
require io;
require rvui;
require qt;
require session_manager;
require rvnuke_process;
require runtime;

\: decodeNL (string; string str)
{
    regex.replace ("#NL#", str, "\n");
}

\: decodeNL (string[]; string[] strs)
{
    let newStrs = string[]();
    for_each (s; strs) newStrs.push_back(decodeNL(s));

    return newStrs;
}

class: RVNukeMode : rvtypes.MinorMode
{ 
    bool      _initialized;
    bool      _doDebug;
    string    _sessionFile;
    string    _nukeContact;
    int       _protocolVersion;

    io.ofstream _debOut;

    qt.QTimer _updateTimer;
    qt.QTimer _updateFoldersTimer;
    qt.QTimer _saveSessionTimer;
    qt.QTimer _heartbeatTimer;

    class: RenderInstance 
    {
        bool started;
        bool finished;
        string sourceName;

        rvnuke_process.ExternalNukeProcess proc;
        string[] renderedFiles;
        string[] newRenderedFiles;
        int expectedFrameCount;

        string outputNode;
        int startFrame, endFrame, incFrame;
        int checkpointFrame;
        string audioFile;
        float audioOffset;
        string baseDir;
        string format;
        string label;
        string date;
        string type;
        bool   stereo;
        int    _origStartFrame;
        int    _origEndFrame;

        method: RenderInstance (RenderInstance; string on, int sf, int ef, int incf,
                string af, float ao, int cpf, string bd, string ft, string lb, string d, string t, bool st)
        {
            outputNode      = on;
            startFrame      = sf;
            endFrame        = ef;
            incFrame        = incf;
            audioFile       = af;
            audioOffset     = ao;
            checkpointFrame = cpf;
            baseDir         = bd;
            format          = ft;
            label           = lb;
            date            = d;
            type            = t;
            stereo          = st;

            started = false;
            finished = false;
            sourceName = "";
            proc = nil;
            renderedFiles = string[]();
            newRenderedFiles = string[]();
            expectedFrameCount = (if (stereo) then 2 else 1) * (endFrame - startFrame + 1) / incFrame;
            _origStartFrame = int.max;
            _origEndFrame =   int.max;
        }

        method: mediaPath (string; string sessionDir)
        {
            if (sourceName != "" && _origStartFrame == int.max)
            {
                let rInfo = commands.nodeRangeInfo(sourceName);
                _origStartFrame = rInfo.start;
                _origEndFrame   = rInfo.end;
            }
            if (renderedFiles.size() == 0) 
            {
                return "smptebars,start=%s,end=%s.movieproc" % (startFrame, endFrame);
            }
            else 
            {
                let sFrame = startFrame,
                    eFrame = endFrame;
                if (_origStartFrame != int.max)
                {
                    if (_origStartFrame < sFrame) sFrame = _origStartFrame;
                    if (_origEndFrame   > eFrame) eFrame = _origEndFrame;
                }
                let fileViewStr = if (stereo) then ".%V" else "";
                return baseDir + "/seq/" + ("%s%s.%s-%s@.%s" % (outputNode, fileViewStr, sFrame, eFrame, format));
            }
        }

        method: inProgress (bool; ) { return (started && !finished); }
    }

    RenderInstance[] _renders;

    //
    //  Preferences
    //

    class: Prefs
    {
        bool updateViewDuringRender;

        method: writePrefs (void; )
        {
            commands.writeSetting ("RvNuke", "updateViewDuringRender", SettingsValue.Bool(updateViewDuringRender));
        }

        method: readPrefs (void; )
        {
            let SettingsValue.Bool b1 = commands.readSetting ("RvNuke", "updateViewDuringRender",
                    SettingsValue.Bool(true));
            updateViewDuringRender = b1;
        }

        method: Prefs (Prefs; )
        {
            readPrefs();
        }
    }

    Prefs _prefs;

    //
    //  Methods to set prefs from menu
    //

    method: toggleUpdateViewDuringRender (void; Event e)
    {
        deb ("updateViewDuringRender currently %s\n" % _prefs.updateViewDuringRender);
        _prefs.updateViewDuringRender = !_prefs.updateViewDuringRender;
        deb ("    now %s\n" % _prefs.updateViewDuringRender);

        _prefs.writePrefs();
    }

    //
    //  Methods to export prefs status to menu
    //

    method: showingUpdateViewDuringRender (int; )
    {
        deb ("updateViewDuringRender pref is %s\n" % _prefs.updateViewDuringRender);
        return if (_prefs.updateViewDuringRender == true) then commands.CheckedMenuState else commands.UncheckedMenuState; 
    }

    method: deb(void; string s) 
    { 
        if (_doDebug) 
        {
            if (_debOut eq nil) _debOut = io.ofstream ("deb.out");
            io.print (_debOut, "nuke_mode: " + s + "\n");
            io.flush (_debOut);
        }
    }

    method: nukeExePath (string; )
    {
        let s = "";

        try { s = commands.getStringProperty ("defaultSequence.nuke.exePath").back(); }
        catch (...) { ; }

        return s;
    }

    method: sessionDir (string; )
    {
        let s = "";

        try { s = commands.getStringProperty ("defaultSequence.nuke.sessionDir").back(); }
        catch (...) { ; }

        return s;
    }

    method: doNothing (void; Event event)
    {
        ;
    }

    method: doNothingState (int; )
    {
        commands.NeutralMenuState;
    }

    method: saveSessionFile (void; )
    {
        deb ("saveSessionFile '%s'" % _sessionFile);
        if (! _initialized) return;

        if (_saveSessionTimer.active()) _saveSessionTimer.stop();
        if (_sessionFile != "" ) commands.saveSession (_sessionFile, true, true);
    }

    method: exit (void; )
    {
        //
        //  Entry point from Nuke
        //

        deb ("exit: closing");
        commands.close();
        deb ("exit: done");
    }

    method: checkFolder (bool; string source, string type)
    {
        deb ("checkFolder %s %s" % (source, type));

        let nukeNode = getNukeProp (source, "node"),
            outputs = commands.nodeConnections (source, false)._1,
            ok = false;

        for_each (o; outputs)
        {
            if (commands.nodeType(o) == "RVFolderGroup")
            {
                 if ((type == "input" || type == "output") && getNukeProp(o, "type") == "input")
                 {
                     ok = true;
                     break;
                 }
                 else
                 if (nukeNode == getNukeProp (o, "node"))
                 {
                     ok = true;
                     break;
                 }
            }
        }

        return ok;
    }

    method: addToFolder (void; string source, string type)
    {
        deb ("addToFolder %s %s" % (source, type));

        let folders = commands.nodesOfType ("RVFolderGroup"),
            targetFolder = "";

        if (type == "input" || type == "output")
        //
        //  Find the "Read/Write Nodes" folder
        //
        {
            for_each (f; folders)
            {
                if (getNukeProp (f, "type") == "input")
                {
                    targetFolder = f;
                    break;
                }
            }
            if (targetFolder == "")
            {
                deb("    can't find folder, making one");
                targetFolder = commands.newNode ("RVFolderGroup", "FolderGroup000000");
                extra_commands.setUIName (targetFolder, "Read/Write Nodes");
                extra_commands.set (targetFolder + ".mode.viewType", "layout");

                setNukeProp (targetFolder, "type", "input");
            }
        }
        else
        //
        //  Find the Render folder for this node
        //
        {
            let node = getNukeProp (source, "node");

            for_each (f; folders)
            {
                if (getNukeProp (f, "node") == node)
                {
                    targetFolder = f;
                    break;
                }
            }
            if (targetFolder == "")
            {
                deb("    can't find folder, making one");
                targetFolder = commands.newNode ("RVFolderGroup", "FolderGroup000000");
                extra_commands.setUIName (targetFolder, "Renders of '%s'" % node);
                extra_commands.set (targetFolder + ".mode.viewType", "layout");

                setNukeProp (targetFolder, "node", node);
            }
        }
        deb ("    targetFolder %s %s" % (targetFolder, extra_commands.uiName(targetFolder)));
        let inputs = commands.nodeConnections (targetFolder, false)._0;
        inputs.push_back (source);
        commands.setNodeInputs (targetFolder, inputs);
    }

    method: updateFolders (void; )
    {
        deb ("updateFolders");

        if (! _initialized) return;

        if (_updateFoldersTimer.active()) _updateFoldersTimer.stop();

        let sourceGroups = commands.nodesOfType("RVSourceGroup");

        for_each (s; sourceGroups)
        {
            let type = getNukeProp (s, "type");
            if (type != "")
            {
                let ok = checkFolder (s, type);

                if (! ok) addToFolder (s, type);
            }
        }

        let folders = commands.nodesOfType("RVFolderGroup"),
            otherFolder = "";

        for_each (f; folders)
        {
            if (getNukeProp (f, "type") == "other")
            {
                otherFolder = f;
                break;
            }
        }
        if (otherFolder == "")
        {
            otherFolder = commands.newNode ("RVFolderGroup", "FolderGroup000000");
            extra_commands.setUIName (otherFolder, "Other");
            extra_commands.set (otherFolder + ".mode.viewType", "layout");

            setNukeProp (otherFolder, "type", "other");
        }
        deb ("    otherFolder %s" % otherFolder);

        let viewNodes = commands.viewNodes();
        for_each (n; viewNodes)
        {
            deb ("    checking %s" % n);
            let type = commands.nodeType(n);
            if (type != "RVFolderGroup" && type != "RVSourceGroup")
            {
                let outputs = commands.nodeConnections (n, false)._1,
                    ok = false;
                for_each (o; outputs)
                {
                    if (commands.nodeType(o) == "RVFolderGroup")
                    {
                        if (getNukeProp(o, "type") == "other")
                        {
                            ok = true;
                            break;
                        }
                    }
                }
                if (! ok)
                {
                    deb ("    adding %s '%s' to otherFolder" % (n, extra_commands.uiName(n)));
                    let inputs = commands.nodeConnections (otherFolder, false)._0;
                    inputs.push_back (n);
                    commands.setNodeInputs (otherFolder, inputs);
                }
            }
        }
        deb ("updateFolders done");
    }

    method: compareSelected (void; Event event, string style)
    {
        deb ("compareSelected %s" % style);

        if (session_manager.theMode() eq nil) return;

        let nodeType = if (style == "tile") then "RVLayoutGroup" else "RVStackGroup",
            selected = session_manager.theMode().selectedNodes();

        if (selected.size() < 2) return;

        let node = commands.newNode (nodeType, nodeType.substr(2,0) + "000000");

        commands.setNodeInputs (node, selected);
        commands.setViewNode (node);

        let nm = "Compare %s views" % selected.size();
        if (selected.size() == 2)
        {
            let nm1 = getNukeProp (selected[0], "node"),
                nm2 = getNukeProp (selected[1], "node"),
                dt1 = getNukeProp (selected[0], "date"),
                dt2 = getNukeProp (selected[1], "date");

            deb ("    nm %s %s dt %s %s" % (nm1, nm2, dt1, dt2));
            if (nm1 != "" && nm2 != "" && dt1 != "" && dt2 != "")
            {
                if (nm1 == nm2) nm = "%s  %s / %s" % (nm1, dt1, dt2);
                else            nm = "%s %s / %s %s" % (nm1, dt1, nm2, dt2);
            }
        }
        extra_commands.setUIName (node, nm);

        if (style == "tile")
        {
            extra_commands.set ("#RVLayoutGroup.layout.mode", "packed");
        }
        else
        {
            rvui.toggleWipe();
        }
        saveSessionFile();
    }

    method: removeObsoleteReads (void; string[] readNames)
    {
        //
        //  Entry point from Nuke
        //

        deb ("removeObsoleteReads \n  %s" % readNames);

        try
        {
            let sourceGroups = commands.nodesOfType("RVSourceGroup"),
                oldFrame = commands.frame();

            for_each (s; sourceGroups)
            {
                deb ("    checking source '%s'" % s);
                let type = getNukeProp (s, "type");
                if (type == "input" || type == "output")
                { 
                    let n = getNukeProp (s, "node"),
                        foundIt = false;

                    for_each (read; readNames) if (read == n) foundIt = true;

                    deb ("    found '%s': %s" % (n, foundIt));
                    if (! foundIt) commands.deleteNode (s);
                }
            }

            _saveSessionTimer.start();

            commands.setFrame(oldFrame);
            commands.redraw();
        }
        catch (exception exc)
        {
            deb ("removeObsoleteReads exception! %s %s\n" % (string(exc), exc.backtrace()));
        }
    }

    method: viewReadNodes (void; string[] nodeNames, string[] media, string[] spaces, int[] first, int[] last, string[] labels, string[] classes, int[] offsets)
    {
        //
        //  Entry point from Nuke
        //

        let labs = decodeNL (labels);

        deb ("viewReadNodes \n  %s\n  %s\n  %s\n  %s\n  %s\n  %s" % (nodeNames, media, spaces, first, last, labs));
        deb ("    cache mode %s" % commands.cacheMode());
        if (! _initialized) return;

        try
        {
            let lastSource = "",
                oldFrame = commands.frame();

            for_index (i; nodeNames)
            {
                let rangeString = "%s-%s#" % (first[i], last[i]),
                    newMedia = media[i];//regex.replace ("%[0-9]*d", media[i], rangeString);

		if (regex.match ("##", newMedia)) newMedia = regex.replace ("#", newMedia, "@");

                let src = addInputSource (nodeNames[i], newMedia, spaces[i], first[i], last[i], labs[i], classes[i], offsets[i]);
                if (src != "") lastSource = src;
            }
            updateFolders();

            if (lastSource != "") commands.setViewNode (lastSource);

            commands.setFrame(oldFrame);
            _saveSessionTimer.start();
            commands.redraw();
        }
        catch (exception exc)
        {
            deb ("viewReadNodes exception! %s %s\n" % (string(exc), exc.backtrace()));
        }
        deb ("    cache mode %s" % commands.cacheMode());
    }

    method: raiseMainWindow (void; )
    {
        //
        //  Entry point from Nuke
        //

        deb ("raiseMainWindow");
        if (! _initialized) return;

        try
        {
            commands.mainWindowWidget().raise();
            commands.mainWindowWidget().activateWindow();
            commands.redraw();
        }
        catch (exception exc)
        {
            deb ("raiseMainWindow exception! %s %s\n" % (string(exc), exc.backtrace()));
        }
    }

    method: currentDateString (string; )
    {
        qt.QDateTime d = qt.QDateTime.currentDateTime();
        return d.toLocalTime().toString("MMM-dd hh:mm:ss");
    }

    method: getNukeProp (string; string nodeName, string prop)
    {
        let val = "";
        try 
        { 
            val = commands.getStringProperty (nodeName + ".nuke." + prop).front(); 
        }
        catch (...) { ; }

        return val;
    }

    method: setNukeProp (void; string nodeName, string prop, string val)
    {
        try 
        { 
            if (getNukeProp (nodeName, prop) != val)
            {
                extra_commands.set (nodeName + ".nuke." + prop, val);
            }
        }
        catch (...) { ; }
    }

    method: fillProperty (void; string name, float value)
    {
        let a = commands.getFloatProperty(name);
        for_index (i; a) a[i] = value;
        commands.setFloatProperty(name, a);
    }

    method: nameFromLabel (string; string label)
    {
        if (label == "") return "";
        let noNewlines = regex.replace ("\n", label, " ");
        deb ("    noNewlines '%s'" % noNewlines);
        return if (noNewlines.size() < 26) then noNewlines else noNewlines.substr(0,22) + " ...";
    }

    method: uiNameFromProps (string; string source, bool inProgress=false)
    {
        let name  = getNukeProp (source, "node"),
            type  = getNukeProp (source, "type"),
            date  = getNukeProp (source, "date"),
            label = getNukeProp (source, "label"),
            labelName = nameFromLabel (label),
            finalName = if (labelName != "") then labelName else name,
            typeStr   = if (type == "input") then "read" else (
                if (type == "output") then "write" else (
                if (type == "current") then "render" else type));

        return "%s %s (%s%s)" % (finalName, date, typeStr, if (inProgress) then "++" else "");
    }

    method: setUiNameAndTip (void; string source, bool inProgress=false)
    {
        deb ("setUiNameAndTip '%s' inProgess %s" % (source, inProgress));
        let uiName = uiNameFromProps (source, inProgress);

        if (extra_commands.uiName (source) != uiName) 
        {
            deb ("    setting UI name to '%s'" % uiName);
            extra_commands.setUIName (source, uiName);
        }

        let name  = getNukeProp (source, "node"),
            label = getNukeProp (source, "label");

        if (label != "") session_manager.setToolTipProp (source, label + "\n(node: %s)\n" % name);
        deb ("   setUiNameAndTip '%s' inProgess %s, done" % (source, inProgress));
    }

    method: subNodeOfType (string; string node, string type)
    {
        let children = string[]();

        try { children = commands.nodesInGroup(node); } catch(...) {;}

        for_each (child; children)
        {
            if (commands.nodeType(child) == type) return child;

            let grandchild = subNodeOfType(child, type);

            if (grandchild neq nil) return grandchild;
        }
        return nil;
    }

    method: updateInputSourceSettings (string sourceName, string node, string colorSpace, int startFrame, int endFrame, string label, string type, int ro)
    {
        deb ("updateInputSourceSettings %s %s %s %s %s %s %s %s" % (sourceName, node, colorSpace, startFrame, endFrame, label, type, ro));

        let sourceFile   = subNodeOfType(sourceName, "RVFileSource"),
            sourceLinear = subNodeOfType(sourceName, "RVLinearize");

        deb ("    sourceFile '%s' sourceLinear '%s'" % (sourceFile, sourceLinear));

        if (    ! commands.nodeExists (sourceName) ||
                ! commands.nodeExists (sourceFile) ||
                ! commands.nodeExists (sourceLinear))
        {
            return;
        }

        extra_commands.set (sourceFile + ".cut.in", startFrame);
        extra_commands.set (sourceFile + ".cut.out", endFrame);

        extra_commands.set (sourceFile + ".group.rangeOffset", ro);

        setNukeProp (sourceName, "node", node);
        setNukeProp (sourceName, "type", type);
        setNukeProp (sourceName, "date", currentDateString());
        setNukeProp (sourceName, "label", label);

        setUiNameAndTip (sourceName);

        int l = 0;
        int s = 0;
        int r = 0;
        float g = 1.0;
        bool doit = false;

        if      (colorSpace == "linear")   { doit = true; }
        else if (colorSpace == "sRGB")     { doit = true; s = 1; }
        else if (colorSpace == "rec709")   { doit = true; r = 1; }
        else if (colorSpace == "Cineon")   { doit = true; l = 1; }
        else if (colorSpace == "Gamma1.8") { doit = true; g = 1.8; }
        else if (colorSpace == "Gamma2.2") { doit = true; g = 2.2; }
        else if (colorSpace == "ViperLog") { doit = true; l = 2; }
        else if (colorSpace == "ALEXA LogC")   { doit = true; l = 3; }
        else if (colorSpace == "ALEXA LogC Film")   { doit = true; l = 4; }
        else if (colorSpace == "RedLog")   { doit = true; l = 6; }
        else if (colorSpace == "RedLogFilm")   { doit = true; l = 7; }

        if (doit)
        {
            deb ("    setting l %s s %s r %s g %s" % (l, s, r, g));
            extra_commands.set (sourceLinear + ".color.logtype", l);
            extra_commands.set (sourceLinear + ".color.sRGB2linear", s);
            extra_commands.set (sourceLinear + ".color.Rec709ToLinear", r);
            fillProperty       (sourceLinear + ".color.fileGamma", g);
            deb ("    done setting");
        }

        commands.sendInternalEvent ("rvnuke-after-source-color-update", sourceName);
    }

    method: addErrorSource (void; string media, int startFrame, int endFrame, string sourceName=nil)
    {
        let errorMedia = "smptebars,start=%s,end=%s.movieproc" % (startFrame, startFrame),
            mySourceName = "";
	let mode = commands.cacheMode();
	deb ("    saving cache mode %d" % mode);
	commands.setCacheMode (commands.CacheOff);

        if (sourceName eq nil)
        {
            let sourceGroups = commands.nodesOfType("RVSourceGroup");

            commands.addSource (errorMedia);

            let newSourceGroups = commands.nodesOfType("RVSourceGroup");

            for_each (ns; newSourceGroups)
            {
                let foundIt = false;
                for_each (s; sourceGroups) if (s == ns) { foundIt = true; break; }
                if (!foundIt) mySourceName = ns;
            }
        }
        else
        {
            let sourceFile   = subNodeOfType(sourceName, "RVFileSource");

            commands.setSourceMedia (sourceFile, string[] { errorMedia });

            mySourceName = sourceName;
        }
	deb ("    resetting cache mode to %d" % mode);
	commands.setCacheMode (mode);

        addLoadErrorPaint (mySourceName, startFrame, media);
    }

    method: stringArraysDiffer (bool; string[] a, string[] b)
    {
        if (a eq nil && b eq nil) return false;
        if (a eq nil) return true;
        if (b eq nil) return true;
        if (a.size() != b.size()) return true;

        for_index (i; a) if (a[i] != b[i]) return true;

        return false;
    }

    method: addInputSource (string node, string media, string colorSpace, int startFrame, int endFrame, string label, string pyClass, int ro)
    {
        deb ("addInputSource %s %s" % (node, media));

        let sourceGroups = commands.nodesOfType("RVSourceGroup"),
            sourceName = "",
            myType = if (pyClass == "Read") then "input" else "output",
            ret = "";

        //
        //  We don't know whether this node is already represented
        //  in the session or not.  So look for it.
        //
        {
            deb ("    searching existing sources for input");
            for_each (s; sourceGroups)
            {
                deb ("    checking source '%s'" % s);
                if (getNukeProp (s, "type") == myType && getNukeProp (s, "node") == node) 
                { 
                    deb ("    found source '%s'" % s);
                    sourceName = s; 
                    break; 
                }
            }

            if (sourceName != "")
            {
                let sourceFile    = subNodeOfType(sourceName, "RVFileSource"),
                    sourceLinear  = subNodeOfType(sourceName, "RVLinearize");
                string[] newMedia = string[] { media };
                string[] oldMedia = commands.getStringProperty (sourceFile + ".media.movie");

                if (stringArraysDiffer (newMedia, oldMedia)) 
                {
                    deb ("    swapping media in existing source: '%s' -> '%s'" % (oldMedia, newMedia));
		    let mode = commands.cacheMode();
		    deb ("    saving cache mode %d" % mode);
		    commands.setCacheMode (commands.CacheOff);

                    try
                    {
                        commands.setSourceMedia (sourceFile, newMedia);

                        removePaint (sourceName, startFrame);

                        if (regex.match ("\\.rgb$", media))
                        {
                            deb ("    setting srgb in/display for source %s" % sourceName);
                            commands.setIntProperty(sourceLinear + ".color.logtype", int[] {0});
                            commands.setIntProperty(sourceLinear + ".color.sRGB2linear", int[] {1});
                            commands.setIntProperty(sourceLinear + ".color.Rec709ToLinear", int[] {0});

                            /*
                            commands.setIntProperty("#RVDisplayColor.color.sRGB", int[] {1});
                            commands.setIntProperty("#RVDisplayColor.color.Rec709", int[] {0});
                            commands.setFloatProperty("#RVDisplayColor.color.gamma", float[] {1.0});
                            */
                        }
                    }
                    catch (...)
                    {
                        print ("ERROR: failed to add media '%s' (1)\n" % newMedia);
                        deb   ("ERROR: failed to add media '%s' (1)"   % newMedia);

                        addErrorSource (media, startFrame, endFrame, sourceName);
                    }
		    deb ("    resetting cache mode to %d" % mode);
		    commands.setCacheMode (mode);
                }
                updateInputSourceSettings (sourceName, node, colorSpace, startFrame, endFrame, label, myType, ro);
                
                //  XXX commands.flushCachedNode (sourceName, true);
                //  XXX handled stereo !
            }
        }
        if (sourceName == "")
        //
        //  We didn't find it so make one
        //
        {
            deb ("    no source found, making new one");
	    let mode = commands.cacheMode();
	    deb ("    saving cache mode %d" % mode);
	    commands.setCacheMode (commands.CacheOff);

            try
            {
                commands.addSource (media); 
            }
            catch (...)
            {
                print ("WARNING: failed to add media '%s' (2)\n" % media);
                deb   ("WARNING: failed to add media '%s' (2)"   % media);

                addErrorSource (media, startFrame, endFrame);
            }
	    deb ("    resetting cache mode to %d" % mode);
	    commands.setCacheMode (mode);

            let newSourceGroups = commands.nodesOfType("RVSourceGroup");
            for_each (ns; newSourceGroups)
            {
                let foundIt = false;
                for_each (s; sourceGroups) if (s == ns) { foundIt = true; break; }
                if (!foundIt) sourceName = ns;
            }
            if (sourceName != "") updateInputSourceSettings (sourceName, node, colorSpace, startFrame, endFrame, label, myType, ro);

            ret = sourceName;
        }
        deb ("    addInputSource done");

        return ret;
    }

    method: findRenderByName (RenderInstance; string name)
    {
        for_each (ri; _renders)
        {
            if (ri.outputNode == name) return ri;
        }

        return nil;
    }

    method: initRenderRun (void; string outputNode, int startFrame, int endFrame, int incFrame, string audio,
            float audioOffset, int cpFrame, string format, string label, string date, string renderType, string stereo)
    {
        //
        //  Entry point from Nuke
        //

        let lab = decodeNL (label);

        deb ("initRenderRun %s %s %s %s %s %s %s %s %s %s %s\n    %s" %
                (outputNode, startFrame, endFrame, incFrame, audio, audioOffset,
                 cpFrame, format, date, renderType, stereo, lab));

        let dateForName = regex.replace(" ", regex.replace(":", date, "_"), "_"),
            dateStr = if (renderType == "current") then "" else "_" + dateForName,
            baseDir = "%s/%s/%s%s" % (sessionDir(), renderType, outputNode, dateStr); 

        if (renderType == "current" && findRenderByName (outputNode) neq nil)
        {
            deb   ("Already running a render for that node, ignoring this request.");
            print ("ERROR: Already running a render for that node, ignoring this request.\n");
            return;
        }
        deb ("    render baseDir '%s'" % baseDir);
        RenderInstance ri = RenderInstance (outputNode, startFrame, endFrame, incFrame,
                audio, audioOffset, cpFrame, baseDir, format, lab, date, renderType, (stereo == "stereo"));
        _renders.push_back (ri);

        updateTimerTimeout();
    }

    /*
    method: fileChangedCallback (void; Event event)
    {
        //  deb ("fileChangedCallback '%s'" % event.contents());
        event.reject();

        if (_renders.empty()) return;

        updateRunningRenders (true);

        if (! _updateTimer.active()) _updateTimer.start();
    }
    */

    method: recursiveDelete (void; string path)
    {
         deb ("recursiveDelete %s" % path);

         string[] subdirs;
         let d = qt.QDir(path),
             filters = qt.QDir.AllEntries | qt.QDir.NoDotAndDotDot,
             entries = d.entryInfoList(filters, qt.QDir.NoSort);

         deb ("%s entries" % entries.size());
         for_each (e; entries)
         {
             if (e.isDir()) subdirs.push_back(e.canonicalFilePath());
             else qt.QFile.remove(e.canonicalFilePath());
         }
         for_each (s; subdirs) recursiveDelete(s);

         let dirName = d.dirName();
         d.cdUp();
         d.rmdir(dirName);
    }

    method: preDeleteCallback (void; Event event)
    {
        deb ("preDeleteCallback '%s'" % event.contents());
        event.reject();

        let sourceName = event.contents(),
            type = getNukeProp (sourceName, "type");

        if (type == "current" || type == "checkpoint" || type == "checkpoint-full")
        {
             let path = sessionDir() + "/" + mediaDirName(sourceName);
             deb ("    is current/checkpoint, deleting %s" % path);
             recursiveDelete (path);
        }
        deb ("preDeleteCallback '%s' done" % event.contents());
    }

    method: preSessionDeleteCallback (void; Event event)
    {
        deb ("preSessionDeleteCallback");
        event.reject();

	if (_nukeContact != "")
	{
	    deb ("disconnecting from nukeContact");
	    commands.remoteSendMessage ("DISCONNECT", string[] {_nukeContact});
	    commands.remoteDisconnect (_nukeContact);
	}

        try 
        {
            saveSessionFile();

            if (_updateTimer.active())        _updateTimer.stop();
            if (_saveSessionTimer.active())   _saveSessionTimer.stop();
            if (_updateFoldersTimer.active()) _updateFoldersTimer.stop();
            if (_heartbeatTimer.active())     _heartbeatTimer.stop();
        }
        catch (...) { ; }

        try 
        {
            for_each (ri; _renders) 
            {
                if (ri.proc neq nil) ri.proc.cancel();
            }
        }
        catch (...) { ; }

        deb ("preSessionDeleteCallback done");
    }

    method: _updateSourceNukeInfo (void; RenderInstance ri)
    {
        if (ri.sourceName == "") { deb ("*************** HUH ?"); return; }

        deb ("_updateSourceNukeInfo source '%s'" % ri.sourceName);

        setNukeProp (ri.sourceName, "node", ri.outputNode);
        setNukeProp (ri.sourceName, "type", ri.type);
        setNukeProp (ri.sourceName, "checkpointFrame", string(ri.checkpointFrame));
        setNukeProp (ri.sourceName, "label", ri.label);
        setNukeProp (ri.sourceName, "date", ri.date);

        let path          = ri.mediaPath(sessionDir()),
            sourceLinear  = subNodeOfType(ri.sourceName, "RVLinearize"),
            sourceFile    = subNodeOfType(ri.sourceName, "RVFileSource");
        string[] newMedia = string[] { path };
        string[] oldMedia = commands.getStringProperty (sourceFile + ".media.movie");

        if (stringArraysDiffer (newMedia, oldMedia)) 
        {
            deb ("    swapping media in existing source: '%s' -> '%s'" % (oldMedia, newMedia));
	    let mode = commands.cacheMode();
	    deb ("    saving cache mode %d" % mode);
	    commands.setCacheMode (commands.CacheOff);

            try
            {
                commands.setSourceMedia (sourceFile, newMedia);

                removePaint (ri.sourceName, ri.startFrame);

                if (regex.match ("\\.rgb$", path))
                {
                    deb ("    setting srgb in/display for source %s" % ri.sourceName);
                    commands.setIntProperty(sourceLinear + ".color.logtype", int[] {0});
                    commands.setIntProperty(sourceLinear + ".color.sRGB2linear", int[] {1});
                    commands.setIntProperty(sourceLinear + ".color.Rec709ToLinear", int[] {0});

                    /*
                    commands.setIntProperty("#RVDisplayColor.color.sRGB", int[] {1});
                    commands.setIntProperty("#RVDisplayColor.color.Rec709", int[] {0});
                    commands.setFloatProperty("#RVDisplayColor.color.gamma", float[] {1.0});
                    */
                }
            }
            catch (...)
            {
                print ("ERROR: failed to add media '%s' (3)\n" % newMedia);
                deb   ("ERROR: failed to add media '%s' (3)"   % newMedia);

                addErrorSource (path, ri.startFrame, ri.endFrame, ri.sourceName);
            }
	    deb ("    resetting cache mode to %d" % mode);
	    commands.setCacheMode (mode);
        }
        if (ri.renderedFiles.size() == 0) addWaitingPaint (ri);

        setUiNameAndTip (ri.sourceName, !ri.finished);

        if (ri.finished) _saveSessionTimer.start();
    }

    method: addLoadErrorPaint (void; string s, int f, string media)
    {
        let nm = qt.QFileInfo(media).fileName();

        addPaint (s, f, "Error loading media:\n%s" % nm);
    }

    method: addWaitingPaint (void; RenderInstance ri)
    {
        addPaint (ri.sourceName, ri.startFrame, "%s\nWaiting for frames ..." % ri.outputNode);
    }

    method: addPaint (void; string s, int f, string t)
    {
        deb ("addPaint %s %s '%s'" % (s, f, t));

        let cont1 = "%s_paint.text:1:%s:rvNuke" % (s, f),
            cont2 = "%s_paint.text:2:%s:rvNuke" % (s, f);

        if (! commands.propertyExists (cont1 + ".text"))
        {
            deb ("    adding paint properties");
            commands.newProperty (cont1 + ".text",     commands.StringType, 1);
            commands.newProperty (cont1 + ".position", commands.FloatType, 2);
            commands.newProperty (cont1 + ".color",    commands.FloatType, 4);
            commands.newProperty (cont1 + ".size",     commands.FloatType, 1);

            commands.newProperty (cont2+ ".text",     commands.StringType, 1);
            commands.newProperty (cont2+ ".position", commands.FloatType, 2);
            commands.newProperty (cont2+ ".color",    commands.FloatType, 4);
            commands.newProperty (cont2+ ".size",     commands.FloatType, 1);
        }

        /*
        commands.setStringProperty (cont1 + ".text",     string[] { t            }, true);
        commands.setFloatProperty  (cont1 + ".position", float[]  { 0.095, 0.745 }, true); 
        commands.setFloatProperty  (cont1 + ".color",    float[]  { 0, 0, 0, 1   }, true);
        commands.setFloatProperty  (cont1 + ".size",     float[]  { 0.0075       }, true);

        commands.setStringProperty (cont2 + ".text",     string[] { t            }, true);
        commands.setFloatProperty  (cont2 + ".position", float[]  { 0.09, 0.75   }, true); 
        commands.setFloatProperty  (cont2 + ".color",    float[]  { 1, 1, 1, 1   }, true);
        commands.setFloatProperty  (cont2 + ".size",     float[]  { 0.0075       }, true);
        */
        commands.setStringProperty (cont1 + ".text",     string[] { t            }, true);
        commands.setFloatProperty  (cont1 + ".position", float[]  { -0.6, 0.24   }, true); 
        commands.setFloatProperty  (cont1 + ".color",    float[]  { 0, 0, 0, 1   }, true);
        commands.setFloatProperty  (cont1 + ".size",     float[]  { 0.0075       }, true);

        commands.setStringProperty (cont2 + ".text",     string[] { t            }, true);
        commands.setFloatProperty  (cont2 + ".position", float[]  { -0.605, 0.245}, true); 
        commands.setFloatProperty  (cont2 + ".color",    float[]  { 1, 1, 1, 1   }, true);
        commands.setFloatProperty  (cont2 + ".size",     float[]  { 0.0075       }, true);

        commands.newProperty       ("%s_paint.frame:%s.order" % (s, f), commands.StringType, 1);
        commands.setStringProperty ("%s_paint.frame:%s.order" % (s, f), string[] { "text:1:%s:rvNuke" % f,  "text:2:%s:rvNuke" % f}, true);

        extra_commands.set ("%s_paint.paint.show" % s, 1);
        extra_commands.set ("%s_paint.nextId.show" % s, 2);

        if (commands.viewNode() == s) commands.setFrame (f);

        deb ("    addPaint %s %s '%s', done" % (s, f, t));
    }

    method: removePaint (void; string s, int f)
    {
        try 
        {
            deb ("removePaint %s %s" % (s, f));

            let cont1 = "%s_paint.text:1:%s:rvNuke" % (s, f),
                cont2 = "%s_paint.text:2:%s:rvNuke" % (s, f);
            ;

            commands.setStringProperty (cont1 + ".text", string[] { "" }, true);
            commands.setStringProperty (cont2 + ".text", string[] { "" }, true);

            deb ("    removePaint %s %s, done" % (s, f));
        }
        catch (...) {;}
    }

    method: updateRenderInstance (void; RenderInstance ri)
    {
        deb ("updateRenderInstance source '%s'" % ri.sourceName);

        let sourceGroups = commands.nodesOfType("RVSourceGroup");

        //
        //  First copy any waiting frames into place
        //

        let newFilesArrived = (ri.newRenderedFiles.size() > 0);

        for_each (f; ri.newRenderedFiles)
        {
            let target = ri.baseDir + "/seq/" + qt.QFileInfo(f).fileName();
                
            if (qt.QFileInfo(target).exists())
            {
                for (int i = 1; ! qt.QFile.remove (target) && i < 10; ++i) 
                deb ("    remove of '%s' failed retry #%s" % (target, i));
            }
            for (int i = 1; ! qt.QFile.rename (f, target) && i < 10; ++i) 
            {
                deb ("    rename of '%s' to '%s' failed retry #%s" % (f, target, i));
            }

            ri.renderedFiles.push_back(f);
        }
        ri.newRenderedFiles.clear();

        if (ri.type == "current" && ri.sourceName == "")
        //
        //  We don't know whether this render is already represented
        //  in the session or not.  So look for it.
        //
        {
            deb ("    no source set, searching existing sources");
            for_each (s; sourceGroups)
            {
                deb ("    checking source '%s'" % s);
                if (getNukeProp (s, "type") == "current" && getNukeProp (s, "node") == ri.outputNode) 
                { 
                    deb ("    found source '%s'" % s);
                    ri.sourceName = s; 
                    break; 
                }
            }
        }
        if (ri.sourceName == "")
        //
        //  We didn't find it so make one
        //
        {
            deb ("    no source found, making new one");
            let path = ri.mediaPath (sessionDir());

            deb ("    adding source '%s'" % path);
	    let mode = commands.cacheMode();
	    deb ("    saving cache mode %d" % mode);
	    commands.setCacheMode (commands.CacheOff);

            try
            {
                commands.addSource (path); 
            }
            catch (...)
            {
                print ("ERROR: failed to add media '%s' (4)\n" % path);
                deb   ("ERROR: failed to add media '%s' (4)"   % path);

                addErrorSource (path, ri.startFrame, ri.endFrame);
            }
	    deb ("    resetting cache mode to %d" % mode);
	    commands.setCacheMode (mode);

            let newSourceGroups = commands.nodesOfType("RVSourceGroup");
            deb ("    after adding we have %s sources" % newSourceGroups.size());
            for_each (ns; newSourceGroups)
            {
                let foundIt = false;
                for_each (s; sourceGroups) if (s == ns) { foundIt = true; break; }
                if (!foundIt) ri.sourceName = ns;
            }
            deb ("    after adding source name is '%s'" % ri.sourceName);

        }
        ri.finished = (ri.renderedFiles.size() >= ri.expectedFrameCount || ri.proc.isFinished());
        deb ("    renderedFiles size %s / %s finished %s" % (ri.renderedFiles.size(), ri.expectedFrameCount, ri.finished));

        _updateSourceNukeInfo (ri);

        commands.flushCachedNode (ri.sourceName, true);
        deb ("    updateRenderInstance source now '%s', done" % ri.sourceName);
    }
     
    documentation: """
    For all renders, each represented by a RenderInstance struct in _renders,
    load any new frames.  If the source has not been created yet, create it.
    """
    method: updateRunningRenders (void; )
    {
        //  deb ("updateRunningRenders");

        try
        {
            let noNewFiles = true,
                allRendersHaveSources = true,
                noProcsFinished = true;
            for_each (ri; _renders) 
            {
                if (ri.newRenderedFiles.size() > 0) noNewFiles = false;
                if (ri.sourceName == "") allRendersHaveSources = false;
                if (ri.started && ri.proc.isFinished()) noProcsFinished = false;
            }
            if (noNewFiles && allRendersHaveSources && noProcsFinished) return;

            //
            //  Just shut off caching during this, to be safe
            //
            let mode = commands.cacheMode();
            deb ("    saving cache mode %d" % mode);
            commands.setCacheMode (commands.CacheOff);

            let sourceCount = commands.sources().size();

            //
            //  update any running renders
            //
            for_each (ri; _renders) updateRenderInstance(ri);

            if (    _renders.size() == 1 &&
                    _renders[0].sourceName != "" &&
                    _prefs.updateViewDuringRender)
            {
                if (commands.viewNode() != _renders[0].sourceName)
                {
                    commands.setViewNode (_renders[0].sourceName);
                }


                regex frameRE = ".*\\.([0-9]+)\\.[^.]+$";
                if (_renders[0].renderedFiles.size() > 0 && frameRE.match(_renders[0].renderedFiles.back())) 
                {
                    deb ("    setting render frame");
                    commands.setFrame (int(frameRE.smatch(_renders[0].renderedFiles.back())[1]));
                }
            }

            commands.reload();
            deb ("    resetting cache mode to %d" % mode);
            commands.setCacheMode (mode);

            if (sourceCount != commands.sources().size())
            {
                updateFolders();
                _saveSessionTimer.start();
            }
            commands.redraw();
        }
        catch (exception exc)
        {
            deb ("updateRunningRenders exception! %s %s\n" % (string(exc), exc.backtrace()));
        }
    }

    method: updateRenderedFiles (void; RenderInstance ri, string file)
    {
        deb ("updateRenderedFiles ri %s file %s" % (ri.outputNode, file));

        ri.newRenderedFiles.push_back(file);
    }

    \: activateProcessInfo (void; bool on)
    {
        rvtypes.State state = commands.data();

        if (state.processInfo eq nil) rvui.loadHUD();

        if (on != state.processInfo._active) state.processInfo.toggle();

        commands.redraw();
    }

    method: startWaitingRenders (void; )
    {
        for_each (ri; _renders)
        {
            if (ri.started == false)
            {
                deb ("startWaitgingRenders starting render of %s" % ri.outputNode);

                //
                //  Create necessary subdirs
                //

                qt.QDir baseDir = qt.QDir (ri.baseDir);
                if (! baseDir.exists("seq")) baseDir.mkdir ("seq");
                if (! baseDir.exists("tmp")) baseDir.mkdir ("tmp");

                //
                //  Create python script to manage render
                //

                let renderScript = ri.baseDir + "/tmp/render.py";
                if (qt.QFileInfo(renderScript).exists()) qt.QFile.remove(renderScript);

                let nukeScript    = ri.baseDir + ("/%s.nk" % ri.type),
                    writeViewsStr = if (ri.stereo) then "writeNode['views'].setValue('left right')" else "",
                    fileViewStr   = if (ri.stereo) then ".%V" else "",
                    outFile       = ri.baseDir + "/tmp/" + ri.outputNode + fileViewStr + ".#." + ri.format;

                let renderPython = """
def onRender() :
    f = nuke.frame()
    for i in range(100) :
        print "**********************************render " + str(f) + "*************************************" 

nuke.addBeforeFrameRender (onRender)
nuke.scriptOpen('%s')
targetNode = nuke.toNode('%s')
writeNode = nuke.nodes.Write (tile_color='0xff000000')
writeNode['file'].setValue ('%s')
writeNode['proxy'].setValue ('%s')
%s
writeNode.setInput (0, targetNode)
nuke.executeMultiple((writeNode,), ([%s, %s, %s],))

                """ % ( nukeScript, ri.outputNode,
                        outFile, outFile,
                        writeViewsStr, ri.startFrame, ri.endFrame, ri.incFrame); 

                io.ofstream o = io.ofstream (renderScript);
                io.print (o, renderPython);
                o.close();

                deb ("renderPython **************************************\n%s" % renderPython);
                deb ("***************************************************");

                //
                //  Create render process
                //

                rvtypes.State state = commands.data();

                /*
                let cmd  = "env",
                    args = string[] { };
                */
                let cmd = nukeExePath(),
                    args = string[] { "-i", "-t", renderScript };

                if (runtime.build_os() == "LINUX")
                {
                    //  See note in rvnuke_process.mu about why we have to do it this way.
                    //
                    cmd = "env";
                    args = string[] { "--unset=LD_LIBRARY_PATH", nukeExePath(), "-i", "-t", renderScript };
                }

                deb ("    constructing process %s %s" % (cmd, args));
                ri.proc = rvnuke_process.ExternalNukeProcess (
                        _debOut,
                        ri.outputNode,
                        cmd,
                        args,
                        10000,
                        rvtypes.ExternalProcess.Type.ReadOnly,
                        nil,
                        ri.expectedFrameCount,
                        updateRenderedFiles (ri, ));

                ri.started = true;
                deb ("    starting render of %s (done)" % ri.outputNode);
            }
        }
    }

    method: updateTimerTimeout (void; )
    {
        deb ("updateTimerTimeout");

        try
        {
            let sourceCount = commands.sources().size();

            startWaitingRenders();
            updateRunningRenders();

            //
            //  remove render instances that are finished
            //
            RenderInstance[] newRenders;
            RenderInstance firstStarted = nil;
            for_each (ri; _renders)
            {
                if (! ri.finished) 
                {
                    newRenders.push_back(ri);
                    if (firstStarted eq nil && ri.started) firstStarted = ri;
                }
                else
                if (ri.type == "current")
                //
                //  quick checkpoint 
                //
                {
                    deb ("   full render of %s finished, making checkpoint" % ri.outputNode);
                    createCheckpoint (nil, false, ri.sourceName);
                }
                else deb ("   checkpoint render of %s finished" % ri.outputNode);
            }
            _renders = newRenders;

            if (sourceCount != commands.sources().size())
            {
                updateFolders();
                _saveSessionTimer.start();
                commands.redraw();
            }

            rvtypes.State state = commands.data();
            if (_renders.empty()) 
            {
                deb ("    rendering complete");
                activateProcessInfo (false);
                state.externalProcess = nil;
            }
            else 
            {
                deb ("    %s active renders firstStarted is nil %s" % (_renders.size(), (firstStarted eq nil)));
                if (firstStarted neq nil) state.externalProcess = firstStarted.proc;
                activateProcessInfo (true);
                _updateTimer.start();
                deb ("    info active %s proc finished %s" % (state.processInfo neq nil && state.processInfo._active, 
                        state.externalProcess neq nil && !state.externalProcess.isFinished()));
            }
        }
        catch (exception exc)
        {
            deb ("updateTimerTimeout exception! %s %s\n" % (string(exc), exc.backtrace()));
        }
    }

    method: selectCurrentByNodeName (void; string nodeName)
    {
        //
        //  Entry point from Nuke
        //

        deb ("selectCurrentByNodeName %s" % nodeName);
        let sourceGroups = commands.nodesOfType ("RVSourceGroup");
        string selectedSource = nil;

        for_each (s; sourceGroups)
        {
            if (    (getNukeProp (s, "type") == "current" ||
                     getNukeProp (s, "type") == "input"   ||
                     getNukeProp (s, "type") == "output") &&
                     getNukeProp (s, "node") == nodeName) 
            { 
                deb ("    found source '%s'" % extra_commands.uiName(s));
                selectedSource = s;
                break;

            }
        }
        if (selectedSource eq nil)
        {
            for_each (s; sourceGroups)
            {
                if (   (getNukeProp (s, "type") == "checkpoint" ||
                        getNukeProp (s, "type") == "checkpoint-full") &&
                        getNukeProp (s, "node") == nodeName) 
                { 
                    deb ("    found source '%s'" % extra_commands.uiName(s));
                    selectedSource = s;
                    break;

                }
            }
        }

        if (selectedSource neq nil && commands.viewNode() != selectedSource) 
        {
            deb ("    setting view node from %s" % extra_commands.uiName(commands.viewNode()));
            commands.setViewNode (selectedSource);
            commands.redraw();
        }
    }

    method: newSourceCallback (void; Event event)
    {
        deb ("new-source '%s'" % event.contents());
        event.reject();
        if (! _initialized) return;

        _saveSessionTimer.start();
    }

    method: newNodeCallback (void; Event event)
    {
        deb ("new-node '%s'" % event.contents());
        event.reject();
        if (! _initialized) return;

        _updateFoldersTimer.start();
    }

    method: findNukeContact (void; )
    {
        for_each (c; commands.remoteConnections())
        {
            if (regex("Nuke@").match(c)) _nukeContact = c;
        }
        deb ("nuke contact name '%s'" % _nukeContact);
    } 

    method: remoteEvalPython (void; string pythonCode)
    {
        deb ("*********************** remoteEvalPython '%s' to '%s'" % (pythonCode, _nukeContact));
        commands.remoteSendEvent (
                "remote-python-eval",
                "*",
                pythonCode,
                string[] {_nukeContact});
    }

    method: selectPatternTest (void; Event event)
    {
        remoteEvalPython ("nuke.executeInMainThread(nuke.selectPattern)");
    }

    method: initSessionSubDir (void; string subPath)
    {
        qt.QDir d = qt.QDir (sessionDir());

        if (! d.mkpath (subPath)) print ("ERROR: could not make path '%s'\n" % (sessionDir() + "/" + subPath));
    }

    method: checkpointDirName (string; string node, string date, bool full)
    {
        let dateForName = regex.replace(" ", regex.replace(":", date, "_"), "_");

        if (full) return "checkpoint-full/" + node + "_" + dateForName;
        else      return "checkpoint/"      + node + "_" + dateForName;
    }

    method: mediaDirName (string; string sourceName)
    {
        let node   = getNukeProp (sourceName, "node"),
            date   = getNukeProp (sourceName, "date"),
            type   = getNukeProp (sourceName, "type");

        if (type == "current") return "current/" + node;
        if (type == "checkpoint") return checkpointDirName (node, date, false);
        if (type == "checkpoint-full") return checkpointDirName (node, date, true);

        return "";
    }

    method: oneFrameFromSource (string[]; string sourceName, string checkpointFrame)
    {
        let sourceFile = subNodeOfType(sourceName, "RVFileSource"),
            media = commands.getStringProperty (sourceFile + ".media.movie"),
            oneFrameMedia = string[]();

        for_each (m; media)
        {
            let nm = regex.replace (".[0-9]*-[0-9]*@.", m, ".%s." % checkpointFrame);
            if (nm != m) oneFrameMedia.push_back (nm);
        }
        deb ("oneFrameFromeSource %s\n" % oneFrameMedia);

        return oneFrameMedia;
    }

    method: addCheckpointSource (string; string[] media, bool full, string node, string date, string label, int cpFrame)
    {
        deb ("addCheckpointSource media %s full %s node %s date %s" % (media, full, node, date));

        let oldSourceGroups = commands.nodesOfType("RVSourceGroup");
	let mode = commands.cacheMode();
	deb ("    saving cache mode %d" % mode);
	commands.setCacheMode (commands.CacheOff);

        try
        {
            commands.addSource (media); 
        }
        catch (...)
        {
            print ("ERROR: failed to add media '%s' (5)\n" % media);
            deb   ("ERROR: failed to add media '%s' (5)"   % media);

            addErrorSource (media[0], cpFrame, cpFrame);
        }
	deb ("    resetting cache mode to %d" % mode);
	commands.setCacheMode (mode);

        let newSourceGroups = commands.nodesOfType("RVSourceGroup"),
            newSource = "";

        for_each (ns; newSourceGroups)
        {
            let foundIt = false;
            for_each (s; oldSourceGroups) if (s == ns) { foundIt = true; break; }
            if (!foundIt) newSource = ns;
        }

        deb ("    new source is %s\n" % newSource);

        bool rgbSeq = false;
        for_each (m; media) if (regex.match ("\\.rgb$", m)) rgbSeq = true;

        if (rgbSeq)
        {
            deb ("    setting srgb in/display for source %s" % newSource);
            let sourceLinear = subNodeOfType(newSource, "RVLinearize");

            commands.setIntProperty(sourceLinear + ".color.logtype", int[] {0});
            commands.setIntProperty(sourceLinear + ".color.sRGB2linear", int[] {1});
            commands.setIntProperty(sourceLinear + ".color.Rec709ToLinear", int[] {0});

            //  XXX
            /*
            commands.setIntProperty("#RVDisplayColor.color.sRGB", int[] {1});
            commands.setIntProperty("#RVDisplayColor.color.Rec709", int[] {0});
            commands.setFloatProperty("#RVDisplayColor.color.gamma", float[] {1.0});
            */
        }
        setNukeProp (newSource, "node", node);
        setNukeProp (newSource, "type", "checkpoint%s" % (if (full) then "-full" else ""));
        setNukeProp (newSource, "date", date);
        setNukeProp (newSource, "label", label);

        setUiNameAndTip (newSource);

        if (full) commands.setViewNode (newSource);

        _saveSessionTimer.start();

        deb ("    done");

        return newSource;
    }

    method: createCheckpoint (void; Event event, bool full, string sourceName)
    {
        deb ("createCheckpoint() full %s sourceName %s" % (full, sourceName));

        string source = sourceName;

        if (source eq nil)
        //
        //  Collect target source from session manager selection
        //
        {
            if (session_manager.theMode() eq nil) return;

            let selectedNodes = session_manager.theMode().selectedNodes();

            deb ("    selectedNodes %s" % selectedNodes);

            if (selectedNodes.size() != 1) return;

            source = selectedNodes[0];
        }

        let node    = getNukeProp (source, "node"),
            date    = getNukeProp (source, "date"),
            type    = getNukeProp (source, "type"),
            cpFrame = getNukeProp (source, "checkpointFrame"),
            label   = getNukeProp (source, "label");

        if (type != "current") return;

        let cpPath = checkpointDirName (node, date, full),
            seqPath = cpPath + "/seq";

        deb ("    cpPath '%s'" % cpPath);

        if (qt.QFileInfo(sessionDir() + "/" + cpPath).exists())
        {
            deb   ("ERROR: there's already a checkpoint called '%s'\n" % cpPath);
            print ("ERROR: there's already a checkpoint called '%s'\n" % cpPath);
            return;
        }

        initSessionSubDir (cpPath);
        initSessionSubDir (seqPath);

        let curPath    = sessionDir() + "/" + mediaDirName(source),
            curSeqPath = curPath + "/seq",
            curSeqDir  = qt.QDir (curSeqPath);

        if (full)
        //
        //  'full' checkpoint, copy all frames
        //
        {
            let entries = curSeqDir.entryList (string[] {}, qt.QDir.Files, 0);

            deb ("    %s entries: %s\n" % (curSeqPath, entries));

            deb ("    copying image files");
            for_each (e; entries)
            {
                let from = curSeqPath + "/" + e,
                    to   = sessionDir() + "/" + seqPath + "/" + e;

                if (! qt.QFile.copy (from, to)) 
                {
                    deb   ("ERROR: failed to checkpoint '%s'" % to);
                    print ("ERROR: failed to checkpoint '%s'" % to);
                    return;
                }
            }
        }
        else
        //
        //  Copy only one frame
        //
        {
            let oneFrameMedia = oneFrameFromSource (source, cpFrame);

            for_each (m; oneFrameMedia)
            {
                let to = sessionDir() + "/" + seqPath + "/" + qt.QFileInfo(m).fileName();
                if (! qt.QFile.copy (m, to)) 
                {
                    deb   ("ERROR: failed to checkpoint '%s'" % to);
                    print ("ERROR: failed to checkpoint '%s'" % to);
                    return;
                }
            }
        }

        deb ("    copying nuke script");

        if (! qt.QFile.copy (curPath + "/current.nk", sessionDir() + "/" + cpPath + "/checkpoint.nk"))
        {
            deb   ("ERROR: failed to checkpoint '%s'" % (curPath + "/curent.nk"));
            print ("ERROR: failed to checkpoint '%s'" % (curPath + "/curent.nk"));
            return;
        }

        deb ("    adding new source");

        let sourceFile = subNodeOfType(source, "RVFileSource"),
            media = commands.getStringProperty (sourceFile + ".media.movie"),
            newMedia = string[]();

        deb ("    media %s" % media);
        for_each (m; media) 
        {
            let nm = regex.replace ("/current/" + node, m, "/" + cpPath);

            if (!full) nm = regex.replace (".[0-9]*-[0-9]*@.", nm, ".%s." % cpFrame);

            newMedia.push_back (nm);
        }
        deb ("    newMedia %s" % newMedia);

        addCheckpointSource (newMedia, full, node, date, label, int(cpFrame));

        commands.redraw();

        deb ("    createCheckpoint done");
    }

    method: disabledFunc (int;) { return commands.DisabledMenuState; }

    method: renderProgressCallback (void; string file)
    {
        deb ("renderProgressCallback %s" % file);
        //commands.redraw();
    }

    method: runRender (void; Event event)
    {
        deb ("runRender");
        extra_commands.set ("defaultSequence.nuke.sessionDir", "/var/tmp/nuke-u501/RvDir/hippo");
        extra_commands.set ("defaultSequence.nuke.exePath", "/Applications/Nuke6.1v2/Nuke6.1v2.app/Contents/MacOS/Nuke6.1v2");
        // XXX  need to remember if this was stereo or not, frame range, etc.
        initRenderRun ("hippoBlur", 1, 100, 1,  "", 0.0, 50, "rgb", "", "Dec 05 21:04:39", "current", true);
        
        rvtypes.State state = commands.data();

        /*
        let cmd = "/Applications/Nuke6.1v2/Nuke6.1v2.app/Contents/MacOS/Nuke6.1v2",
            args = string[] { "-i", "-t", "inscript.py" };

        deb ("    constructing process");
        state.externalProcess = rvnuke_process.ExternalNukeProcess (
                _debOut,
                "my render",
                cmd,
                args,
                10000,
                rvtypes.ExternalProcess.Type.ReadOnly,
                nil,
                150,
                renderProgressCallback);

        rvui.toggleProcessInfo();
        */
    }

    method: installPython (void; Event event)
    {
        let supportPath = supportPath("rvnuke_mode", "rvnuke"),
            supportDir  = qt.QDir (supportPath),
            filters     = qt.QDir.AllEntries | qt.QDir.NoDotAndDotDot,
            entries     = supportDir.entryInfoList(filters, qt.QDir.NoSort),
            fileList    = string[] (),
            files       = "";

        deb ("installPythong supportDir '%s'" % supportDir);

        //
        //  Copy support files to home dir
        //

        for_each (i;  entries)
        {
            files += "    " + i.fileName() + "\n";
        }
        deb ("    files\n%s" % files);

        let ans = commands.alertPanel (true, commands.InfoAlert, "Copy Nuke support files to home directory ?",
                "\nThis process will install the following files in a 'tweak' " +
                "sub-directory of your $HOME/.nuke directory (creating the " +
                "necessary directories if they do not already exist):\n" +
                "\n" +
                files,
                "Yes", "No", nil);

        if (ans == 1) return;

        let envHomePath   = system.getenv ("HOME", nil),
            homeDir       = if (envHomePath neq nil) then qt.QDir(envHomePath) else qt.QDir.home(),
            tweakSubPath  = ".nuke/rvnuke",
            tweakPath     = homeDir.canonicalPath() + "/" + tweakSubPath;

        deb ("    tweakPath '%s'" % tweakPath);

        if (! qt.QFileInfo(tweakPath).exists() && ! homeDir.mkpath(tweakSubPath))
        {
            let msg = "Can't create directory '%s'" % tweakPath;
            deb (msg);
            commands.alertPanel (true, commands.ErrorAlert, msg, "", "OK", nil, nil);
            return;
        }

        for_each (i; entries)
        {
            let from = i.canonicalFilePath(),
                to   = tweakPath + "/" + qt.QFileInfo(from).fileName();

            deb ("    removing '%s'" % to);
            if (qt.QFileInfo(to).exists() && !qt.QFile.remove (to))
            {
                let msg = "Remove of existing file failed: '%s'" % to;
                deb (msg);
                commands.alertPanel (true, commands.ErrorAlert, msg, "", "OK", nil, nil);
                return;
            }
            deb ("    copying '%s' -> '%s'" % (from, to));
            if (! qt.QFile.copy (from, to)) 
            {
                let msg = "Copy failed: '%s' -> '%s'" % (from, to);
                deb (msg);
                commands.alertPanel (true, commands.ErrorAlert, msg, "", "OK", nil, nil);
                return;
            }
        }

        //
        //  Check and install or optionally modify init.py
        //

        let initPath = homeDir.canonicalPath() + "/.nuke/init.py";

        let initContents = "",
            appendRequired = true;

        if (qt.QFileInfo(initPath).exists())
        {
            deb ("    init.py '%s' exists." % initPath);

            let initFile   = qt.QFile (initPath),
                initStream = qt.QTextStream (initFile);

            if (! initFile.open (qt.QFile.ReadOnly | qt.QFile.Text))
            {
                let msg = "init.py '%s' exists but is not readable." % initPath;
                deb (msg);
                commands.alertPanel (true, commands.ErrorAlert, msg, "", "OK", nil, nil);
                return;
            }

            initContents = initStream.readAll();

            initFile.close();

            deb ("    init contents %s" % initContents);

            if (    regex ("\n[^#]*nuke.pluginAddPath\('\\./rvnuke'\)").match(initContents) ||
                    regex ("^[^#]*nuke.pluginAddPath\('\\./rvnuke'\)").match(initContents))
            {
                deb ("    init already contains pluginAddPath line");
                //  all done
                appendRequired = false;
            }
            else
            {
                let ans = commands.alertPanel (true, commands.InfoAlert, "Add rvnuke directory to plugin path ?",
                        "\nIt appears that you already have an init.py file in your $HOME/.nuke directory. Click 'Yes " +
                        "to append the following line to the end of that file.  Click 'No' if you'd like to add it " +
                        "by hand (but note that it must be added for the RV/Nuke toolset to function)." +
                        "\n\nnuke.pluginAddPath('./rvnuke')\n\n",
                        "Yes", "No", nil);

                if (ans != 0) return;
            }
        }

        if (appendRequired)
        {
            deb ("    appending plugin path line to init.py");

            let newInitFile = qt.QFile (initPath),
                newInitStream = qt.QTextStream (newInitFile);

            if (! newInitFile.open (qt.QFile.WriteOnly | qt.QFile.Text | qt.QFile.Truncate))
            {
                let msg = "cannot open init.py '%s' for writing." % initPath;
                deb (msg);
                commands.alertPanel (true, commands.ErrorAlert, msg, "", "OK", nil, nil);
                return;
            }

            print (newInitStream, initContents + "\nnuke.pluginAddPath('./rvnuke')\n");

            newInitFile.close();
        }

        commands.alertPanel (true, commands.InfoAlert, "Installation complete !", "", "OK", nil, nil);
        deb ("    install complete");
    }

    method: combineMenus (rvtypes.Menu; rvtypes.Menu a, rvtypes.Menu b)
    {
        if (a eq nil) return b;
        if (b eq nil) return a;

        rvtypes.Menu n;
        for_each (i; a) n.push_back(i);
        for_each (i; b) n.push_back(i);

        return n;
    }

    method: buildMenu (rvtypes.Menu; )
    {
        rvtypes.Menu m1 = rvtypes.Menu {
            {"Create Nuke Read Node", createNukeReadNodes, nil, sourceSelected},
            {"Wipe Selected Views", compareSelected(, "wipe"), nil, viewsSelected},
            {"Tile Selected Views", compareSelected(, "tile"), nil, viewsSelected},
            {"Restore Checkpoint", restoreCheckpoint, nil, checkpointSelected},
            {"Create Full Checkpoint", createCheckpoint (, true, nil), nil, renderSelected},
            //{"Run Render", runRender, nil, nil},
            {"_", nil},
            {"Preferences", nil, nil, disabledFunc},
            {"    Update View During Render", toggleUpdateViewDuringRender, nil, showingUpdateViewDuringRender},
        };

        rvtypes.Menu m2 = nil;
        if (system.getenv ("RV_NUKE_HIDE_INSTALL_OPTION", nil) eq nil)
        {
            m2 = rvtypes.Menu {
                {"_", nil},
                {"Install Nuke Support Files", installPython, nil, doNothingState},
            };
        }

        rvtypes.Menu m3 = rvtypes.Menu {
            {"_", nil},
            {"Help ...", showHelpFile, nil, doNothingState},
        };

        rvtypes.Menu m = rvtypes.Menu {
            {"Nuke", combineMenus (combineMenus (m1, m2), m3)}
        };

        return m;
    }

    method: initFromNuke (void; string sessionDir, int protocolVersion, string exePath)
    {
        //
        //  Entry point from Nuke
        //

        try
        {
            deb ("initFromNuke '%s' protocolVersion %s cacheMode %s\n    '%s'" % (
                    sessionDir, protocolVersion, commands.cacheMode(), exePath));

            if (protocolVersion != _protocolVersion)
            {
                print (
                """
                ERROR: ****************************************************************
                ERROR: python/mu rvnuke protcool version mismatch: %s/%s
                ERROR:     Please install the python support files for this version.
                ERROR: ****************************************************************
                """ % (protocolVersion, _protocolVersion));

                commands.alertPanel (true, commands.ErrorAlert, "Protocol version mis-match",
                        "\nThe Python and Mu components seem to be from different versions of " +
                        "the Nuke integration package (Python is %s vs Mu %s).  Please install the Python support files " 
			% (protocolVersion, _protocolVersion) +
                        "for this version by selecting \"Install Nuke Support Files\" from the Nuke " +
                        "menu in RV. Or refer to the installation instructions in the documentation.",
                        "Continue", nil, nil);
                return;
            }

            if (!_initialized)
            //
            //  First time
            //
            {
                //commands.defineModeMenu ("rvnuke-mode", buildMenu());
                ;
            }
            _initialized = false;

            if (sessionDir == sessionDir()) 
            {
                _initialized = true;
                return;
            }

            findNukeContact();

            if (commands.sources().size() != 0)
            {
                deb ("    clearEverything");
                saveSessionFile();
                rvui.clearEverything();
            }

            extra_commands.set ("defaultSequence.nuke.sessionDir", sessionDir);
            extra_commands.set ("defaultSequence.nuke.exePath", exePath);

            _sessionFile = sessionDir() + "/session.rv";
            qt.QFileInfo f = qt.QFileInfo (_sessionFile);

            deb ("    checking session file '%s' readable %s\n" % (_sessionFile, f.isReadable()));
            if (f.isReadable()) 
            {
                deb ("    reading session file");
                let mode = commands.cacheMode();
		commands.setCacheMode (commands.CacheOff);
                commands.addSource (_sessionFile);
                commands.setCacheMode (mode);
                deb ("    after reading session file, %s sources" % commands.sources().size());
            }

            extra_commands.set ("defaultSequence.nuke.sessionDir", sessionDir);
            extra_commands.set ("defaultSequence.nuke.exePath", exePath);

            saveSessionFile();

            commands.redraw();

            //  _heartbeatTimer.start();

            _initialized = true;
        }
        catch (exception exc)
        {
            deb ("exception! %s %s\n" % (string(exc), exc.backtrace()));
        }
    }

    method: restoreCheckpoint (void; Event event)
    {
        deb ("restoreCheckpoint()");

        if (session_manager.theMode() eq nil) return;

        let selectedNodes = session_manager.theMode().selectedNodes();

        deb ("    selectedNodes %s" % selectedNodes);

        if (selectedNodes.size() != 1) return;

        let source = selectedNodes[0],
            node   = getNukeProp (source, "node"),
            date   = getNukeProp (source, "date"),
            type   = getNukeProp (source, "type");

        //  XXX error dialog
        if (source == "" || node == "" || date == "" || type == "") return;

        let cpPath = mediaDirName (source),
            nukefile = if (type == "checkpoint-full") then "checkpoint" else type,
            scriptPath = sessionDir() + "/" + cpPath + "/" + nukefile + ".nk";

        if (cpPath == "") return;

        let ans = commands.alertPanel (true, commands.InfoAlert, "Restore Checkpoint ?",
            "\nOverwrite current nuke script with checkpoint of %s, dated %s ?\n\n" % (node, date), "Yes", "No", nil);
        if (ans != 0) return;

        deb ("    nuke script path '%s'" % scriptPath);

        remoteEvalPython ("nuke.executeInMainThread(restoreCheckpoint, (\"%s\",\"%s\",\"%s\"))" % (scriptPath, node, date));
    }

    method: removeTimeString (string; string m)
    {
        let types = string[] {"%[0-9]*d", "#+", "@+"},
            front = "",
            back = "",
            ret = "";

        for_each (t; types)
        {
            let re = regex("^(.*[^0-9]+)[0-9]+-[0-9]+%s(.*)$" % t);

            if (re.match(m))
            {
                let parts = re.smatch(m);
                front = parts[1];
                back = parts[2];
                deb ("    '%s' (%s) -> '%s' '%s'" % (m, t, front, back));
                break;
            }
        }
        if (front == "")
        //
        //  Now look for case without inbuilt frame range
        //
        {
            types = string[] {")%[0-9]*d", "[^#]+)#+", "[^@]+)@+"};
            for_each (t; types)
            {
                let re = regex("^(.*%s(.*)$" % t);

                if (re.match(m))
                {
                    let parts = re.smatch(m);
                    front = parts[1];
                    back = parts[2];
                    deb ("    '%s' (%s) -> '%s' '%s'" % (m, t, front, back));
                    break;
                }
            }
        }
        if (front == "") ret = m;
        else
        {
            let files = commands.existingFilesInSequence (m);

            if (files eq nil || files.size() < 2) ret = m;
            else
            {
                let re         = regex("%s([-0-9]+)%s" % (front, back)),
                    firstFrame = re.smatch(files.front())[1],
                    lastFrame  = re.smatch(files.back())[1];

                deb ("    on disk: first frame '%s', last frame '%s'" % (firstFrame, lastFrame));
                if (firstFrame.size() == lastFrame.size()) ret = front + ("%%0%sd" % firstFrame.size()) + back;
                else                                       ret = front + "%d" + back;
            }
        }
        deb ("    ret '%s'" % ret);
        return ret;
    }

    method: createNukeReadNodes (void; Event event)
    {
        deb ("creatNukeReadNodes()");

        if (session_manager.theMode() eq nil) return;

        let selectedNodes = session_manager.theMode().selectedNodes();

        deb ("    selectedNodes %s" % selectedNodes);

        if (selectedNodes.size() == 0) return;

        let str = "[",
            first = true;

        for_each (n; selectedNodes)
        {
            try
            {
                //  XXX  what about stereo here ?
                let sourceFile = subNodeOfType(n, "RVFileSource"),
                    media = commands.getStringProperty (sourceFile + ".media.movie").front(),
                    comma = ",",
                    info = commands.sourceMediaInfo (sourceFile, nil);

                if (first) { comma = ""; first = false; }

                media = removeTimeString (media);
                let newName = regex.replace ("[^0-9a-zA-Z_]", extra_commands.uiName(n), "_");

                str = str + comma + (" (\"%s\", %s, %s, \"%s\")" % (media, info.startFrame, info.endFrame, newName));
            }
            catch (...) { ; }
        }
        str = str + "]";

        deb ("    evalStr '%s'" % str);
        remoteEvalPython ("nuke.executeInMainThread(createReadNode, %s)" % str);
    }

    method: showHelpFile (void; Event event)
    {
        let helpFile = io.path.join(supportPath("rvnuke_mode", "rvnuke"), "rvnuke_help.html");
        if (rvui.globalConfig.os == "WINDOWS")
        {
            let wpath = regex.replace("/", helpFile, "\\\\");
            system.defaultWindowsOpen(wpath);
        }
        else commands.openUrl("file://" + helpFile);
    }

    method: oneWayHeartbeat (void; )
    {
        remoteEvalPython ("nuke.executeInMainThread(heartbeatFromRv)");
    }

    method: render (void; Event event)
    {
        ;
    }

    method: sourceSelected (int; )
    {
        if (session_manager.theMode() eq nil) return commands.DisabledMenuState;

        let nodes = session_manager.theMode().selectedNodes();

        for_each (n; nodes)
        {
            if (commands.nodeType(n) != "RVSourceGroup") return commands.DisabledMenuState;
        }

        return commands.NeutralMenuState;
    }

    method: viewsSelected (int; )
    {
        if (session_manager.theMode() eq nil) return commands.DisabledMenuState;

        let nodes = session_manager.theMode().selectedNodes();

        return if (nodes.size() >= 2) then commands.NeutralMenuState else commands.DisabledMenuState;
    }

    method: renderSelected (int; )
    {
        if (session_manager.theMode() eq nil) return commands.DisabledMenuState;

        let nodes = session_manager.theMode().selectedNodes();

        if (nodes.size() == 1 && getNukeProp(nodes[0], "type") == "current")
        {
            return commands.NeutralMenuState;
        }
        return commands.DisabledMenuState;
    }

    method: checkpointSelected (int; )
    {
        if (session_manager.theMode() eq nil) return commands.DisabledMenuState;

        let nodes = session_manager.theMode().selectedNodes();

        if (nodes.size() == 1)
        {
            let t = getNukeProp(nodes[0], "type");

            if (t == "checkpoint" || t == "checkpoint-full" || t == "current") return commands.NeutralMenuState;
        }
        return commands.DisabledMenuState;
    }

    method: RVNukeMode(RVNukeMode; string name)
    {
        init(name,
            nil,
            [
            ("new-source", newSourceCallback, "source added"),
            //("file-changed", fileChangedCallback, "file changed"),
            ("before-node-delete", preDeleteCallback, "node about to be deleted"),
            ("before-session-deletion", preSessionDeleteCallback, "session about to be deleted"),
            ("new-node", newNodeCallback, "node added to graph"),
            ],
            //nil 
            buildMenu()
        );

        _prefs = Prefs();
        _protocolVersion = 115;

        _doDebug = false;
        _debOut = nil;

        if (system.getenv ("RV_NUKE_DEBUG", nil) neq nil) _doDebug = true;

        _initialized = false;

        _sessionFile = "";

        _updateTimer = qt.QTimer(commands.mainWindowWidget());
        _updateTimer.setSingleShot(true);
        _updateTimer.setInterval(500);
        qt.connect (_updateTimer, qt.QTimer.timeout, updateTimerTimeout);

        _updateFoldersTimer = qt.QTimer(commands.mainWindowWidget());
        _updateFoldersTimer.setSingleShot(true);
        _updateFoldersTimer.setInterval(1000);
        qt.connect (_updateFoldersTimer, qt.QTimer.timeout, updateFolders);

        _saveSessionTimer = qt.QTimer(commands.mainWindowWidget());
        _saveSessionTimer.setSingleShot(true);
        _saveSessionTimer.setInterval(1000);
        qt.connect (_saveSessionTimer, qt.QTimer.timeout, saveSessionFile);

        _heartbeatTimer = qt.QTimer(commands.mainWindowWidget());
        _heartbeatTimer.setSingleShot(false);
        _heartbeatTimer.setInterval(1000);
        qt.connect (_heartbeatTimer, qt.QTimer.timeout, oneWayHeartbeat);

        _renders = RenderInstance[]();

        _nukeContact = ""; 

        let portFile = commands.commandLineFlag("rvnukePortFile");
        if (portFile neq nil) 
        {
            io.ofstream o = io.ofstream (portFile);
            io.print (o, "%s\n" % commands.myNetworkPort());
            o.close();
        }

        deb ("**************** NukeMode()\n");
    }
}

\: createMode (rvtypes.Mode;)
{
    return RVNukeMode("rvnuke_mode");
}

\: theMode (RVNukeMode; )
{
    RVNukeMode m = rvui.minorModeFromName("rvnuke_mode");

    return m;
}

}
