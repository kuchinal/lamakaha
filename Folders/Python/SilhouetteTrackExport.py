import nuke
import nukescripts

class SillhouetteTrackExport( nukescripts.PythonPanel):
    def __init__(self, node):
        self.n = node

        if not self.n.Class() in ('Tracker4', 'Tracker3','CornerPin2D'):
            nuke.message('The selected node is neither a Tracker or a Cornerpin.')
            return

        self._trackNames = self.getTrackNames(self.n)
        if not self._trackNames:
            nuke.message('No Tracks found in %s' %self.n.name())
            return

        nukescripts.PythonPanel.__init__(self, 'Export Tracks from %s' %self.n.name())

        self.fRange = nuke.String_Knob('fRange', 'Framerange: ', '%s-%s' %(nuke.root().firstFrame(), nuke.root().lastFrame()))

        self.trackEnum = []
        self.trackXY = []
        for i in range(len(self._trackNames)):
            if i > 3:
                break

            self.trackEnum.append(nuke.Enumeration_Knob('track%d' %i, 'Track %d' %(i + 1), self._trackNames))
            self.trackEnum[i].setValue(i)

            self.trackXY.append(nuke.XY_Knob('trackpos%d', ''))
            self.trackXY[i].setExpression('root.%s.tracks.%d.track_x' %(self.n.name(), i + 1), 0)
            self.trackXY[i].setExpression('root.%s.tracks.%d.track_y' %(self.n.name(), i + 1), 1)

        self.addKnob(self.fRange)
        for j, k in enumerate(self.trackEnum):
            self.addKnob(k)
            self.addKnob(self.trackXY[j])


    def knobChanged(self, knob):
        if knob in self.trackEnum:
            i = self.trackEnum.index(knob)
            j = knob.getValue()
            self.trackXY[i].setExpression('root.%s.tracks.%d.track_x' %(self.n.name(), j + 1), 0)
            self.trackXY[i].setExpression('root.%s.tracks.%d.track_y' %(self.n.name(), j + 1), 1)


    def getTrackNames(self, tracker4Node):
        k=tracker4Node['tracks']
        s=tracker4Node['tracks'].toScript().split(' \n} \n{ \n ')
        s.pop(0)
        ss=str(s)[2:].split('\\n')
        if ss: 
            ss.pop(-1)
        if ss: 
            ss.pop(-1)
        outList=[]
        for i in ss:
            outList.append(i.split('"')[1])
        return outList

    def finishModalDialog(self, result):
        if result:

            path = nuke.getFilename('Export Tracker:', '*.nk', '', 'script', 'save', extension='.nk')

            frange = self.fRange.getValue().split('-')
            first = int(frange[0])
            last = int(frange[1])

            nuke.root().begin()
            tr = nuke.createNode('Tracker3')

            for i in range(len(self.trackEnum)):
                if 1 <= i < 4:
                    tr['enable%s' %(i + 1)].setValue(True)
                if i < 4:
                    tr['track%d' %(i + 1)].setAnimated()

            tmp = self.n['tracks']
            _numc = 31
            x = 2
            y = 3

            for k in range(len(self._trackNames)):
                if k > 3:
                    break

                index = self.trackEnum[k].getValue()

                for f in range(first, last + 1):

                    vx = tmp.getValueAt(f, int(_numc * index + x))
                    vy = tmp.getValueAt(f, int(_numc * index + y))
                    tr['track%d' %(k + 1)].setValueAt(vx, f, 0)
                    tr['track%d' %(k + 1)].setValueAt(vy, f, 1)

            if path:
                nuke.nodeCopy(path)
                nuke.delete(tr)

        self.destroy()
