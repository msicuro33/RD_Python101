import maya.cmds as cmds

print('UI')

def rigarm(*args):
	print("Rig Arm is cool")

mymenu = cmds.menu('RDojo_Menu', label = 'RD Menu', to = True, p = 'MayaWindow')
cmds.menuItem(label = 'Rig_Arm', p = mymenu, command = rigarm)

