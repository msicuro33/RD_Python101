import maya.cmds as cmds
import json
import os
import system.utils as utils
reload(utils)

#Create variables above the Class level that can be read on Class import
#This is also known as Attributes of a Class
class_name = 'Rig_Arm'
layout_file = arm.json
num_joints = 4


class Rig_Arm:
	"""docstring for ClassName"""
	
	def __init__(self):
		#Get the joint list from the arm json file
		data_path = os.environ["RDOJO_DATA"] + "data/rig/arm.json"
		#Use the read json function
		data = utils.readJson(data_path)
		#Load the json into a dictionary
		self.module_info = json.loads(data)
		'''NOTE: If we want to build the arm from some set of joints
		in the scene, we could overwrite self.module_info['positions']'''
		
		#Make new Dictionary to store information about the arm rig
		self.rig_info = {}

		#Check if we have a selection of joints to get new positions from
		if len(cmds.ls(sl = True, type = 'joint',)) == num_joints:
			sel = cmds.ls(sl = True, type = 'joint')
			positions = []
			for i in sel:
				positions.append(cmds.xform(i, q = True, ws = True, t = True))
			self.rig_info['positions'] = positions
		else:
			self.rig_info['positions'] = self.module_info['positions']
		
		'''Instead of using Else, we could just return a message saying the selection
		doesn't meet the requirements for an arm'''

		#Set a temporary variable to override the name of the side to determine Left or Right
		self.instance = "L_"

		#Run rig_arm function
		self.rig_arm()


	def rig_arm(self):
		cmds.select(cl=True)
		#################
		##Create joints##
		#################

		#Create IK joints
		self.rig_info['ik_joints'] = utils.createJoint(self.module_info['ik_joints'], self.rig_info['positions'], self.instance)
		cmds.select(cl=True)

		#Create FK joints
		self.rig_info['fk_joints'] =utils.createJoint(self.module_info['fk_joints'])
		cmds.select(cl=True)

		#Create rig joints
		self.rig_info['rig_joints'] =utils.createJoint(self.module_info['rig_joints'])
		cmds.select(cl=True)


		#################
		##Create IK Rig##
		#################

		#1st Step: Create IK Handle
		ikHandle_name = self.module_info['ik_controls'][1].replace('s_',self.instance)
		self.rig_info['ik_handle'] = cmds.ikHandle(n=ikHandle_name, sj=self.rig_info['ik_joints'][0], ee=self.rig_info['ik_joints'][2], sol='ikRPsolver',p = 2, w = 1)

		#2nd Step: Define info to be passed into createControl function to create IK control
		self.rig_info['ik_controls'] = utils.createControl([[self.rig_info['positions'][2], self.module_info['ik_controls'][0].replace('s_',self.instance)]])
		#Thought it should be: self.createControl([[self.module_info['positions'][2], self.module_info['ik_controls'][0], self.module_info['ik_controls'][1]]])
		#But there isn't a name in the data for an IK ctrlgroup name

		#3rd Step: Parent IK handle to the control
		cmds.parent('ikhandle_arm','ctrl_ik_wrist')

		#Deselect
		cmds.select(cl=True)


		#################
		##Create FK Rig##
		#################

		#Create FK controls
		fk_ctrl_info = self.createControl([[self.module_info['positions'][0],self.module_info['fk_controls'][0]],
		[self.module_info['positions'][1],self.module_info['fk_controls'][1]], [self.module_info['positions'][2],self.module_info['fk_controls'][2]]])
		cmds.select(cl=True)

		#Parent FK controls
		cmds.parent(fk_ctrl_info[0][0],fk_ctrl_info[1][1][0])
		cmds.parent(fk_ctrl_info[1][0],fk_ctrl_info[2][1][0])


		####################################
		##Create Pole vector for IK Handle##
		####################################
		
		#Get the location for the pole vector, store it and create a pole vector control
		pole_vector_position = self.calculatePoleVectorPosition([self.module_info['ik_joints'][0],self.module_info['ik_joints'][1],self.module_info['ik_joints'][2]])
		pole_vector_ctrl_info = [[pole_vector_position,self.module_info['ik_controls'][2]]]
		self.createControl(pole_vector_ctrl_info)

		#Create Pole Vector Constraint
		cmds.poleVectorConstraint(self.module_info['ik_controls'][2], self.module_info['ik_controls'][1])


		##################################################
		##Orient constraint IK wrist joint to IK control##
		##################################################
		cmds.orientConstraint(self.module_info['ik_controls'][0], self.module_info['ik_joints'][2], mo = True)



		'''Connect IK and FK to rig joints'''
		#parent Constrain fk->ik->rig
		#cmds.parentConstraint('fk_shoulder_joint', 'ik_shoulder_joint', 'rig_shoulder_joint', maintainOffset=True, weight=1)
		#To switch between FK and IK, change values of the two attributes (FK shoulder joint and IK shoulder joint)
		# and set one or the other to zero		

	



print("IT'S ALIIIIIIVE")