#Create IK joints
cmds.joint(n='ik_shoulder_joint', p=[-7.253066, 0, 0.590704])
cmds.joint(n='ik_elbow_joint', p=[-1.365397, 0, -0.939316])
cmds.joint(n='ik_wrist_joint', p=[4.193028, 0, 0.861846])
cmds.joint(n='ik_wristEnd_joint', p=[5.316333, 0, 1.617172])
cmds.select(d=True)

#Create FK joints
cmds.joint(n='fk_shoulder_joint', p=[-7.253066, 0, 0.590704])
cmds.joint(n='fk_elbow_joint', p=[-1.365397, 0, -0.939316])
cmds.joint(n='fk_wrist_joint', p=[4.193028, 0, 0.861846])
cmds.joint(n='fk_wristEnd_joint', p=[5.316333, 0, 1.617172])
cmds.select(d=True)

#Create rig joints
cmds.joint(n='rig_shoulder_joint', p=[-7.253066, 0, 0.590704])
cmds.joint(n='rig_elbow_joint', p=[-1.365397, 0, -0.939316])
cmds.joint(n='rig_wrist_joint', p=[4.193028, 0, 0.861846])
cmds.joint(n='rig_wristEnd_joint', p=[5.316333, 0, 1.617172])
cmds.select(d=True)

#Create IK Rig


#1st Step: Create IK Handle
cmds.ikHandle(n='ikhandle_arm', sj='ik_shoulder_joint', ee='ik_wrist_joint', sol='ikRPsolver',p = 2, w = 1)

#2nd Step: Create IK control
#Query ik wrist joint world space position
ik_ctrl_pos = cmds.xform('ik_wrist_joint',q=True, t = True, ws = True)
#Create empty group
cmds.group(em=1, n='group_ctrl_IKwrist')
#Create IK control handle(circle)
cmds.circle(n='ctrl_ik_wrist', )
#Parent the group to the control
cmds.parent('ctrl_ik_wrist','group_ctrl_IKwrist')
#Move the group pivot to the wrist joint
cmds.xform('group_ctrl_IKwrist', t = ik_ctrl_pos, ws = True)
#Parent ikHandle to control
cmds.parent('ikhandle_arm','ctrl_ik_wrist')

#Create FK Rig


#Connect IK and FK to rig joints