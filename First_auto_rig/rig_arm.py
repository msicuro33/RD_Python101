#Create IK joints
cmds.joint(n='ik_shoulder_joint', p=[-7.253066, 0, 0.590704])
cmds.joint(n='ik_elbow_joint', p=[-1.365397, 0, -0.939316])
cmds.joint(n='ik_wrist_joint', p=[4.193028, 0, 0.861846])
cmds.joint(n='ik_wristEnd_joint', p=[5.316333, 0, 1.617172])
cmds.select(cl=True)

#Create FK joints
cmds.joint(n='fk_shoulder_joint', p=[-7.253066, 0, 0.590704])
cmds.joint(n='fk_elbow_joint', p=[-1.365397, 0, -0.939316])
cmds.joint(n='fk_wrist_joint', p=[4.193028, 0, 0.861846])
cmds.joint(n='fk_wristEnd_joint', p=[5.316333, 0, 1.617172])
cmds.select(cl=True)

#Create rig joints
cmds.joint(n='rig_shoulder_joint', p=[-7.253066, 0, 0.590704])
cmds.joint(n='rig_elbow_joint', p=[-1.365397, 0, -0.939316])
cmds.joint(n='rig_wrist_joint', p=[4.193028, 0, 0.861846])
cmds.joint(n='rig_wristEnd_joint', p=[5.316333, 0, 1.617172])
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

#1st Step: Create FK Shoulder control
#Query FK shoulder joint world space position
fk_shoulder_joint_pos = cmds.xform('fk_shoulder_joint',q=True, t = True, ws = True)
#Create empty group
cmds.group(em=1, n='group_ctrl_FKshoulder')
#Create FK control handle(circle)
cmds.circle(n='ctrl_fk_shoulder', )
#Parent the group to the control
cmds.parent('ctrl_fk_shoulder','group_ctrl_FKshoulder')
#Move the group to the shoulder joint
cmds.xform('group_ctrl_FKshoulder', t = fk_shoulder_joint_pos, ws = True)
#Deslect
cmds.select(cl=True)

#2nd Step: Create FK Elbow control
#Query FK elbow joint world space position
fk_elbow_joint_pos = cmds.xform('fk_elbow_joint',q=True, t = True, ws = True)
#Create empty group
cmds.group(em=1, n='group_ctrl_FKelbow')
#Create FK control handle(circle)
cmds.circle(n='ctrl_fk_elbow', )
#Parent the group to the control
cmds.parent('ctrl_fk_elbow','group_ctrl_FKelbow')
#Move the group to the shoulder joint
cmds.xform('group_ctrl_FKelbow', t = fk_elbow_joint_pos, ws = True)
#Deslect
cmds.select(cl=True)

#3rd Step: Create FK Wrist control
#Query FK wrist joint world space position
fk_wrist_joint_pos = cmds.xform('fk_wrist_joint',q=True, t = True, ws = True)
#Create empty group
cmds.group(em=1, n='group_ctrl_FKwrist')
#Create FK control handle(circle)
cmds.circle(n='ctrl_fk_wrist', )
#Parent the group to the control
cmds.parent('ctrl_fk_wrist','group_ctrl_FKwrist')
#Move the group to the wrist joint
cmds.xform('group_ctrl_FKwrist', t = fk_wrist_joint_pos, ws = True)
#Deslect
cmds.select(cl=True)

'''Create Pole vector for IK Handle'''
#Query IK elbow joint world space position
ik_elbow_joint_pos = cmds.xform('ik_elbow_joint',q=True, t = True, ws = True)
#Create Locator for Pole Vector
cmds.spacelocator(n='elbow_pole_vector')
#Move the Locator to the elbow joint
cmds.xform('elbow_pole_vector', t = ik_elbow_joint_pos, ws = True)
#Move the Locator away from the elbow in the Z axis
cmds.setAttr('elbow_pole_vector.translateZ', -4.0,)
#Create Pole Vector Constraint
cmds.poleVectorConstraint('elbow_pole_vector', 'ikhandle_arm')


'''Connect IK and FK to rig joints'''
#parent Constrain fk->ik->rig
cmds.parentConstraint('fk_shoulder_joint', 'ik_shoulder_joint', 'rig_shoulder_joint', maintainOffset=True, weight=1)
#To switch between FK and IK, change values of the two attributes (FK shoulder joint and IK shoulder joint)
# and set one or the other to zero
