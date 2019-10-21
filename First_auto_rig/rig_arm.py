import maya.cmds as cmds
import json
import os
import system.utils as utils

#Hold IK joint names + positions
ik_joint_names = [['ik_shoulder_joint', [-7.253066, 0, 0.590704]],['ik_elbow_joint', [-1.365397, 0, -0.939316]], ['ik_wrist_joint', [4.193028, 0, 0.861846]], ['ik_wristEnd_joint', [5.316333, 0, 1.617172]]]
#Hold FK joint names + positions
fk_joint_names = [['fk_shoulder_joint', [-7.253066, 0, 0.590704]],['fk_elbow_joint', [-1.365397, 0, -0.939316]], ['fk_wrist_joint', [4.193028, 0, 0.861846]], ['fk_wristEnd_joint', [5.316333, 0, 1.617172]]]
#Hold rig joint names + positions
rig_joint_names = [['rig_shoulder_joint', [-7.253066, 0, 0.590704]],['rig_elbow_joint', [-1.365397, 0, -0.939316]], ['rig_wrist_joint', [4.193028, 0, 0.861846]], ['rig_wristEnd_joint', [5.316333, 0, 1.617172]]]
		

class Rig_Arm:
	"""docstring for ClassName"""
	
	def __init__(self):
		#Get the joint list from the arm json file
		data_path = os.environ["RDOJO_DATA"] + "rig/arm.json"
		#Use the read json function
		data = utils.readJson(data_path)
		#Load the json into a dictionary
		self.module_info = json.loads(data)

	def rig_arm(self):
		#################
		##Create joints##
		#################

		#Create IK joints
		self.createJoint(ik_joint_names)
		cmds.select(cl=True)

		#Create FK joints
		self.createJoint(fk_joint_names)
		cmds.select(cl=True)

		#Create rig joints
		self.createJoint(rig_joint_names)
		cmds.select(cl=True)


		#################
		##Create IK Rig##
		#################

		#1st Step: Create IK Handle
		cmds.ikHandle(n='ikhandle_arm', sj='ik_shoulder_joint', ee='ik_wrist_joint', sol='ikRPsolver',p = 2, w = 1)

		#2nd Step: Define info to be passed into createControl function to create IK control
		ik_ctrl_info = [[ik_joint_names[2][1], 'ctrl_ik_wrist', 'group_ctrl_IKwrist']]
		self.createControl(ik_ctrl_info)

		#3rd Step: Parent IK handle to the control
		cmds.parent('ikhandle_arm','ctrl_ik_wrist')

		#Deselect
		cmds.select(cl=True)


		#################
		##Create FK Rig##
		#################

		#Create FK controls
		fk_ctrl_info = [[fk_joint_names[0][1], 'ctrl_fk_shoulder' ,'group_ctrl_FKshoulder'], [fk_joint_names[1][1], 'ctrl_fk_elbow', 'group_ctrl_FKelbow'], [fk_joint_names[2][1], 'ctrl_fk_wrist','group_ctrl_FKwrist']]
		self.createControl(fk_ctrl_info)
		cmds.select(cl=True)


		####################################
		##Create Pole vector for IK Handle##
		####################################
		
		#Query IK elbow joint world space position
		ik_elbow_joint_pos = cmds.xform('ik_elbow_joint',q=True, t = True, ws = True)
		#Create Locator for Pole Vector
		cmds.spaceLocator(n='elbow_pole_vector')
		#Move the Locator to the elbow joint
		cmds.xform('elbow_pole_vector', t = ik_elbow_joint_pos, ws = True)
		#Move the Locator away from the elbow in the Z axis
		cmds.setAttr('elbow_pole_vector.translateZ', -4.0,)
		#Create Pole Vector Constraint
		cmds.poleVectorConstraint('elbow_pole_vector', 'ikhandle_arm')

		##################################################
		##Orient constraint IK wrist joint to IK control##
		##################################################
		cmds.orientConstraint(ik_ctrl_info[0][1], ik_joint_names[2][0], mo = True)



		'''Connect IK and FK to rig joints'''
		#parent Constrain fk->ik->rig
		#cmds.parentConstraint('fk_shoulder_joint', 'ik_shoulder_joint', 'rig_shoulder_joint', maintainOffset=True, weight=1)
		#To switch between FK and IK, change values of the two attributes (FK shoulder joint and IK shoulder joint)
		# and set one or the other to zero		

	def createJoint(self, joint_info):
		'''
		Takes in joint info as an argument and iterates through the name and position to create joint
		'''
		for i in joint_info:
			cmds.joint(n=i[0], p=i[1])


	def createControl(self, ctrlInfo):
		'''
		Iterates through joint_names+positions to create control curves
		'''
		for info in ctrlInfo:
			#Get WS position of joint
			pos = info[0]
			#Create an empty group
			ctrl_group = cmds.group(em=1, n=info[2])
			#Create circle control object
			ctrl = cmds.circle(n=info[1])
			#Parent the control to the group
			cmds.parent(ctrl,ctrl_group)
			#Move the group to the joint
			cmds.xform(ctrl_group, t = pos, ws = True)





print("IT'S ALIIIIIIVE")