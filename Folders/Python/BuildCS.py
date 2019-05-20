def BuildCS():
    import nuke
    import nukescripts
    import readversions
    import os
    import ftrack_api
    import getpass

    ftrack_server = os.environ.get("FTRACK_SERVER")
    ftrack_user = getpass.getuser()
    ftrack_api_key = os.environ.get("FTRACK_API_KEY")


    session = ftrack_api.Session(   server_url=ftrack_server,
                                    api_key=ftrack_api_key,
                                    api_user=ftrack_user)


    ref_node = nuke.selectedNode()

    project_name = os.environ.get("JOB")

    project = session.query("Project where name is '{0}'".format(project_name.lower())).all()
    project = project[0]

    project_short = "".join([c for c in project_name.split("_")[0] if c.isupper()])
    project_root = os.path.join("/corky/projects/", project_name)
    rv_command = os.path.join(project_root, "bin/centos-6_x86-64/rv")
    sequences_root = os.path.join(project_root, "seq")





    def make_group(name, artist_name, status, file_name, shot_in, shot_out, seq, shot, fullname, shot_obj, task_id=None):
        g = nuke.createNode("Group")
        g.setName("_".join([name, seq, shot, ""]))
        shotname_knob = nuke.String_Knob('shotname', 'Shotname:')
        if task_id:
            task_id_knob = nuke.String_Knob('taskid', 'Task ID:')
        desc = shot_obj["description"].encode("utf-8")
        desc_knob = nuke.Text_Knob('description', 'Description:', desc)
        work = shot_obj["custom_attributes"]["digital_work"].encode("utf-8")
        work_knob = nuke.Text_Knob('work', 'Work:', work)
        line1_knob = nuke.Text_Knob("line1", "", "")
        if task_id:
            artist_knob = nuke.String_Knob('artist', 'Artist:')
            status_knob = nuke.String_Knob('status', 'Status:')
            update_status_knob = nuke.PyScript_Knob('update_status', 'Update Status/Artist:', "import ftrack_api\nimport getpass\nftrack_server = os.environ.get(\"FTRACK_SERVER\")\nftrack_user = getpass.getuser()\nftrack_api_key = os.environ.get(\"FTRACK_API_KEY\")\nsession = ftrack_api.Session(server_url=ftrack_server, api_key=ftrack_api_key, api_user=ftrack_user)\ntask = session.query(\"Task where id is '{0}'\".format(nuke.thisNode().knob(\"taskid\").value()))\nnew_user = task[0][\"assignments\"][0][\"resource\"][\"username\"]\nnew_stage = task[0][\"status\"][\"name\"]\nnuke.thisNode().knob(\"artist\").setValue(new_user)\nnuke.thisNode().knob(\"status\").setValue(new_stage)")
        line2_knob = nuke.Text_Knob("line2", "", "")
        font_scale_knob = nuke.Double_Knob("font_scale", "Font Scale")
        font_opacity_knob = nuke.Double_Knob("font_opacity", "Font Opacity")
        hold_cb_knob = nuke.Boolean_Knob('enable_hold', 'enable Framehold:')
        hold_value_knob = nuke.Int_Knob("frame_value", "Frame:")
        line3_knob = nuke.Text_Knob("line2", "", "")
        open_rv_knob = nuke.PyScript_Knob("open_rv", "Open in RV",
                                          "from subprocess import Popen\nimport re\nrv_command = '{0}'\npattern = re.compile('_(comp|prep)_v[\d][\d][\d]_beauty')\nfile = nuke.thisGroup().node('Read1').knob('file').value()\ninit_file = re.sub(pattern, '_plate_v001_beauty', file)\nPopen([rv_command, file, init_file])".format(
                                              rv_command))

        g.addKnob(shotname_knob)
        if task_id:
            g.addKnob(task_id_knob)
        g.addKnob(desc_knob)
        g.addKnob(work_knob)
        g.addKnob(line1_knob)
        if task_id:
            g.addKnob(artist_knob)
            g.addKnob(status_knob)
            g.addKnob(update_status_knob)
        g.addKnob(line2_knob)
        g.addKnob(font_scale_knob)
        g.addKnob(font_opacity_knob)
        g.addKnob(hold_cb_knob)
        g.addKnob(hold_value_knob)
        g.addKnob(line3_knob)
        g.addKnob(open_rv_knob)
        g.knob("shotname").setText(str("_".join([seq, shot])))
        g.knob("shotname").setEnabled(False)
        if task_id:
            g.knob("taskid").setText(task_id)
            g.knob("taskid").setEnabled(False)
            g.knob("artist").setText(str(artist_name))
            g.knob("artist").setEnabled(False)
            g.knob("status").setText(str(status))
            g.knob("status").setEnabled(False)
        g.knob("font_scale").setValue(1.7)
        g.knob("font_opacity").setValue(.7)
        g.knob("enable_hold").setFlag(nuke.STARTLINE)
        g.knob("frame_value").setValue(int((shot_in + shot_out) / 2))
        g.begin()
        read = nuke.createNode("Read")
        read.knob("file").setValue(file_name)
        read.knob("first").setValue(shot_in)
        read.knob("last").setValue(shot_out)
        shottxt = nuke.createNode("Text2")
        shottxt.knob("opacity").setExpression("[value parent.font_opacity]")
        shottxt.knob("global_font_scale").setExpression("[value parent.font_scale]")
        shottxt.knob("font").setValue("Arial", "Bold")
        
        #descr = " [string trimleft [string trimright [file tail [value Read1.file]] beauty.1001.exr] CRE_FTR]".format(read.name())
        descr = " [string map {_comp_ _ _beauty. _} [string trimleft [string trimright [file tail [value Read1.file]] beauty.1001.exr] OW_]]"
        shottxt.knob("message").setValue(descr)

        shottxt.knob("box").setY(0)
        shottxt.knob("box").setR(3000)
        shottxt.knob("box").setT(200)
        shottxt.knob("yjustify").setValue("bottom")

        artisttxt = nuke.createNode("Text2")
        artisttxt.knob("opacity").setExpression("[value parent.font_opacity]")
        artisttxt.knob("global_font_scale").setExpression("[value parent.font_scale]")
        artisttxt.knob("font").setValue("Arial", "Bold")

        artisttxt.knob("message").setValue("[value parent.artist]")

        artisttxt.knob("box").setValue(0, 0)
        artisttxt.knob("box").setExpression("height",1)
        artisttxt.knob("box").setExpression("width", 2)
        artisttxt.knob("box").setExpression("height",3)
        artisttxt.knob("xjustify").setValue("right")
        artisttxt.knob("yjustify").setValue("top")
        hold = nuke.createNode("FrameHold")
        hold.knob("first_frame").setExpression("[value parent.frame_value]")
        hold.knob("disable").setExpression("![value parent.enable_hold]")
        out_dot = nuke.createNode("Dot")
        out = nuke.createNode("Output")
        out.setInput(0, out_dot)
        g.end()
        readversions.updateVersioning(g)
        if task_id:
            g.knob("label").setText(
            "[value artist] ([value status])\nv[value Read1_vpd]\n[if {[value enable_hold]} {return \"frame [value frame_value]\"}]")
        else:
            g.knob("label").setText(
                "v[value Read1_vpd]\n[if {[value enable_hold]} {return \"frame [value frame_value]\"}]")
        return g



    seq = ref_node.knob("sequence").value()

    exclude_list = ref_node.knob("excludestatus").value().split("_")

    path_to_plates = "data/plates"
    path_to_comps = "compositing/images/versions"

    comp1_suffix = "plate_v001_beauty"
    master_plate = "master"

    all_shots = session.query(
    "Shot where project.full_name is '{0}' and "
    "parent.name is '{1}' and "
    "status.name not_in ('{2}') and "
    "name is_not 'sequence'".format(project_name, seq, "', '".join(exclude_list))).all()

    all_shots_sorted = sorted(all_shots, key=lambda k: k["name"])


    xpos = ref_node.xpos()
    ypos = ref_node.ypos()
    y_offset = 80
    x_offset = int(ref_node.knob("x_offset").value())
    extra_offset = 80
    min_shot = ref_node.knob("min_shot").value()
    max_shot = ref_node.knob("max_shot").value()
    all_assets = ref_node.knob("all_assets").value()


    for shot_obj in all_shots_sorted:
        shot = shot_obj["name"]
        shot_num = int(shot)

        print shot, shot_num
        if len(shot)>4:
            continue
        if shot_num < min_shot:
            continue
        if shot_num > max_shot:
            break
        shot_file_basename = "_".join([project_short, seq, shot])
        shot_root = os.path.join(sequences_root, seq, shot)

        comps_root = os.path.join(shot_root, path_to_comps)
        shot_in = int(shot_obj["custom_attributes"]["frame_work_in"]) - int(shot_obj["custom_attributes"]["frame_handle_in"])
        shot_out = int(shot_obj["custom_attributes"]["frame_work_out"]) + int(shot_obj["custom_attributes"]["frame_handle_out"])
        shot_comp_artist = None
        shot_comp_status = None
        comp_dict = False

        comp_task = session.query("Task where parent.id is '{0}' and "
                                  "name is 'compositing'".format(shot_obj["id"]))
        if comp_task:
            comp_task = comp_task[0]
            comp_task_id = comp_task["id"]
            if len(comp_task["assignments"]) > 0:
                print shot, len(comp_task["assignments"])
                comp_artist = comp_task["assignments"][0]["resource"]["username"]
            else:
                comp_artist = "None"
            comp_status = comp_task["status"]["name"]
            shot_comp_artist = comp_artist
            shot_comp_status = comp_status


        xpos += x_offset


        query_expression = ('AssetVersion where asset.parent.project.name is "{0}" '
                            'and asset.parent.parent.name is "{1}" '
                            'and asset.parent.name in ("{2}") and '
                            'task.type.name is "Compositing" order by version descending'.format(project_name,seq,shot))

        result = session.query(query_expression)

        print "+"*50
        print bool(result)
        print "+"*50
        if result:
            versions = result.all()
            # First one (example)
            asset_version= versions[0]
            
            print asset_version
            for component in asset_version.get('components'):
                if component.values()[1] == 'review_mov':
                    media = component['component_locations'][0]["resource_identifier"]
                    #print media





        if os.path.exists(comps_root):
            renders = os.listdir(comps_root)
            comps = []

            for r in renders:
                if r.startswith(shot_file_basename + "_comp_"):
                    if r.endswith("_beauty"):
                        comps.append(r)


            if comps:
                comps = sorted(comps, reverse=True)
                compfile = os.path.join(comps_root, comps[0], "output", comps[0] + ".%04d.exr")
                grp = make_group("COMP", shot_comp_artist, shot_comp_status, media, 2, 2, seq, shot,
                                 "compositing", shot_obj, comp_task_id)
                grp.setXYpos(xpos, ypos)
                nuke.toNode("CS_Tools")['setCache'].execute()



