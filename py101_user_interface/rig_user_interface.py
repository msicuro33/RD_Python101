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

#The UI Class
class RDojo_UI(object):
	"""docstring for RDojo_UI"""
	def __init__(self, *args):
		print("In RDojo_UI")
		mi = cmds.window("MayaWindow", ma = True, q = True)
		for m in mi:
			if m == "RDojo_Menu":
				cmds.deleteUI('RDojo_Menu' ,m=True)

		mymenu = cmds.menu('RDojo_Menu', label = 'RD Menu', to = True, p = 'MayaWindow')
		cmds.menuItem(label = 'Rig_Tool', p = mymenu, command = self.ui)

		#Create a dictionary to store UI elements we can access later
		self.UIElements = {}


 		
	

