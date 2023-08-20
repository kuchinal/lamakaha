import nuke

toolbar = nuke.menu("Nodes")
DeepCMenu = toolbar.addMenu("DeepC", icon="DeepC.png")
DeepCDraw = DeepCMenu.addMenu("Draw", icon="ToolbarDraw.png")
DeepCChannel = DeepCMenu.addMenu("Channel", icon="ToolbarChannel.png")
DeepCColor = DeepCMenu.addMenu("Color", icon="ToolbarColor.png")
DeepC3D = DeepCMenu.addMenu("3D", icon="Cube.png")
DeepCDraw.addCommand(
    "DeepCPMatte",
    lambda: nuke.createNode("DeepCPMatte"),
    icon="DeepCPMatte.png")
DeepCDraw.addCommand(
    "DeepCPNoise",
    lambda: nuke.createNode("DeepCPNoise"),
    icon="DeepCPNoise.png")
DeepCDraw.addCommand(
    "DeepCID",
    lambda: nuke.createNode("DeepCID"),
    icon="DeepCID.png")
DeepCChannel.addCommand(
    "DeepCAddChannels",
    lambda: nuke.createNode("DeepCAddChannels"),
    icon="DeepCAddChannels.png")
DeepCChannel.addCommand(
    "DeepCRemoveChannels",
    lambda: nuke.createNode("DeepCRemoveChannels"),
    icon="DeepCRemoveChannels.png")
DeepCChannel.addCommand(
    "DeepCShuffle",
    lambda: nuke.createNode("DeepCShuffle"),
    icon="DeepCShuffle.png")
DeepCColor.addCommand(
    "DeepCGrade",
    lambda: nuke.createNode("DeepCGrade"),
    icon="DeepCGrade.png")
DeepCColor.addCommand(
    "DeepCSaturation",
    lambda: nuke.createNode("DeepCSaturation"),
    icon="DeepCSaturation.png")
DeepC3D.addCommand(
    "DeepCWorld",
    lambda: nuke.createNode("DeepCWorld"),
    icon="DeepCWorld.png")
