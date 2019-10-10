import maya.cmds as cmds

print('UI')

def rigarm(*args):
	print("Rig Arm is cool")
	import First_auto_rig.rig_arm as rig_arm
	reload(rig_arm)
	print(rig_arm)
	rig_arm = rig_arm.Rig_Arm()
	print(rig_arm)
	rig_arm.rig_arm()
	
mymenu = cmds.menu('RDojo_Menu', label = 'RD Menu', to = True, p = 'MayaWindow')
cmds.menuItem(label = 'Rig_Arm', p = mymenu, command = rigarm)

