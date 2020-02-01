import maya.cmds as cmds
import json
import os
import system.utils as utils


class Rig_Arm:
	"""docstring for ClassName"""
	
	def __init__(self):
		#Get the joint list from the arm json file
		data_path = os.environ["RDOJO_DATA"] + "/rig/arm.json"
		#Use the read json function
		data = utils.readJson(data_path)
		#Load the json into a dictionary
		self.module_info = json.loads(data)
		'''NOTE: If we want to build the arm from some set of joints
		in the scene, we could overwrite self.module_info['positions']'''


	def rig_arm(self):
		#################
		##Create joints##
		#################

		#Create IK joints
		self.createJoint(self.module_info['ik_joints'])
		cmds.select(cl=True)

		#Create FK joints
		self.createJoint(self.module_info['fk_joints'])
		cmds.select(cl=True)

		#Create rig joints
		self.createJoint(self.module_info['rig_joints'])
		cmds.select(cl=True)


		#################
		##Create IK Rig##
		#################

		#1st Step: Create IK Handle
		ik_handle = cmds.ikHandle(n=self.module_info['ik_controls'][1], sj=self.module_info['ik_joints'][0], ee=self.module_info['ik_joints'][2], sol='ikRPsolver',p = 2, w = 1)

		#2nd Step: Define info to be passed into createControl function to create IK control
		self.createControl([[self.module_info['positions'][2], self.module_info['ik_controls'][0]]])
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

	def createJoint(self, joint_info):
		'''
		Takes in joint info as an argument and iterates through the name and position to create joint
		'''
		[cmds.joint(n=joint_info[i], p=self.module_info['positions'][i]) for i in range(len(joint_info))]


	def createControl(self, ctrlInfo):
		'''
		Iterates through joint_names+positions to create control curves
		'''
		control_info = []
		for info in ctrlInfo:
			#Get WS position of joint
			pos = info[0]
			#Create an empty group
			ctrl_group = cmds.group(em=1, n="group_" + info[1])
			#Create circle control object
			ctrl = cmds.circle(n=info[1])
			#Parent the control under the group
			cmds.parent(ctrl,ctrl_group)
			#Move the group to the joint
			cmds.xform(ctrl_group, t = pos, ws = True)
			#Append control info to control_info List
			control_info.append([ctrl_group, ctrl])
		return(control_info)

	def calculatePoleVectorPosition(self, joints):
		from maya import cmds , OpenMaya
		start = cmds.xform(joints[0], q = True, ws = True, t = True)
		mid = cmds.xform(joints[1], q = True, ws = True, t = True)
		end = cmds.xform(joints[2], q = True, ws = True, t = True)
		
		startVector = OpenMaya.MVector(start[0], start[1], start[2])
		midVector = OpenMaya.MVector(mid[0], mid[1], mid[2])
		endVector = OpenMaya.MVector(end[0], end[1], end[2])
		
		startEnd = endVector - startVector
		startMid = midVector - startVector
		dotP = startMid * startEnd
		proj = float(dotP) / float(startEnd.length())
		startEndN = startEnd.normal()
		projV = startEndN * proj
		arrowV = startMid - projV
		arrowV *= 0.5
		finalV = arrowV + midVector
		return([finalV.x, finalV.y, finalV.z])



print("IT'S ALIIIIIIVE")