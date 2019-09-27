import maya.cmds as cmds

'''Create joints'''
#Hold IK joint names + positions
ik_joint_names = [['ik_shoulder_joint', [-7.253066, 0, 0.590704]],['ik_elbow_joint', [-1.365397, 0, -0.939316]], ['ik_wrist_joint', [4.193028, 0, 0.861846]], ['ik_wristEnd_joint', [5.316333, 0, 1.617172]]]
#Hold FK joint names + positions
fk_joint_names = [['fk_shoulder_joint', [-7.253066, 0, 0.590704]],['fk_elbow_joint', [-1.365397, 0, -0.939316]], ['fk_wrist_joint', [4.193028, 0, 0.861846]], ['fk_wristEnd_joint', [5.316333, 0, 1.617172]]]
#Hold rig joint names + positions
rig_joint_names = [['rig_shoulder_joint', [-7.253066, 0, 0.590704]],['rig_elbow_joint', [-1.365397, 0, -0.939316]], ['rig_wrist_joint', [4.193028, 0, 0.861846]], ['rig_wristEnd_joint', [5.316333, 0, 1.617172]]]

'''
Function to create joints: 
Uses joint names variable as an argument and iterates through the name and position

'''
def createJoint(joint_info):
	for i in joint_info:
		cmds.joint(n=i[0], p=i[1])

#Create IK joints
createJoint(ik_joint_names)
cmds.select(cl=True)

#Create FK joints
createJoint(fk_joint_names)
cmds.select(cl=True)

#Create rig joints
createJoint(rig_joint_names)
cmds.select(cl=True)



'''Create IK Rig'''

#1st Step: Create IK Handle
cmds.ikHandle(n='ikhandle_arm', sj='ik_shoulder_joint', ee='ik_wrist_joint', sol='ikRPsolver',p = 2, w = 1)


#2nd Step: Create IK control

#Query ik wrist joint world space position
ik_wrist_joint_pos = cmds.xform('ik_wrist_joint',q=True, t = True, ws = True)
#Create empty group
cmds.group(em=1, n='group_ctrl_IKwrist')
#Create IK control handle(circle)
cmds.circle(n='ctrl_ik_wrist', )
#Parent the group to the control
cmds.parent('ctrl_ik_wrist','group_ctrl_IKwrist')
#Move the group pivot to the wrist joint
cmds.xform('group_ctrl_IKwrist', t = ik_wrist_joint_pos, ws = True)
#Parent control to the IK Handle
cmds.parent('ikhandle_arm','ctrl_ik_wrist')
#Deselect
cmds.select(cl=True)


'''Create FK rig'''

#FK Joint world space positions
fk_shoulder_joint_pos = cmds.xform('fk_shoulder_joint',q=True, t = True, ws = True)
fk_elbow_joint_pos = cmds.xform('fk_elbow_joint',q=True, t = True, ws = True)
fk_wrist_joint_pos = cmds.xform('fk_wrist_joint',q=True, t = True, ws = True) 

'''
Function to create controls
'''
def createControl(group_name,ctrl_name,intended_joint):
	#Create empty group
	cmds.group(em=1, n= group_name)
	#Create FK control handle(circle)
	cmds.circle(n= ctrl_name)
	#Parent the group to the control
	cmds.parent(ctrl_name,group_name)
	#Move the group to the wrist joint
	cmds.xform(group_name, t = intended_joint, ws = True)
	cmds.select(cl=True)
	
#Run function to create shoulder, elbow and wrist controls
createControl('group_ctrl_FKshoulder','ctrl_fk_shoulder',fk_shoulder_joint_pos)
createControl('group_ctrl_FKelbow','ctrl_fk_elbow',fk_elbow_joint_pos)
createControl('group_ctrl_FKwrist','ctrl_fk_wrist',fk_wrist_joint_pos)


'''Create Pole vector for IK Handle'''
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


'''Connect IK and FK to rig joints'''
#parent Constrain fk->ik->rig
#cmds.parentConstraint('fk_shoulder_joint', 'ik_shoulder_joint', 'rig_shoulder_joint', maintainOffset=True, weight=1)
#To switch between FK and IK, change values of the two attributes (FK shoulder joint and IK shoulder joint)
# and set one or the other to zero

print("IT'S ALIIIIIIVE")