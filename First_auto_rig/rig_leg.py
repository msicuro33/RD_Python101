'''Create left leg IK joints'''
cmds.joint(n='joint_pelvis', p=[-2, 4.212193, 2.628613])

cmds.joint(n='left_ik_joint_hip', p=[0, 4.212193, 2.628613])
cmds.joint(n='left_ik_joint_knee', p=[0, -0.0937814, 4.174347])
cmds.joint('left_ik_joint_hip', e = True, zso = True, oj = 'xyz', sao = 'yup') 
cmds.joint(n='left_ik_joint_ankle', p=[0, -4.311428, 2.319466])
cmds.joint('left_ik_joint_knee', e = True, zso = True, oj = 'xyz', sao = 'yup')
cmds.joint(n='left_ik_joint_ball', p=[0, -5.3, 4.7])
cmds.joint('left_ik_joint_ankle', e = True, zso = True, oj = 'xyz', sao = 'yup')
cmds.joint(n='left_ik_joint_toe', p=[0, -5.3, 5.8])

'''Create IK Handles'''
cmds.ikHandle(n= "left_ik_Handle_leg", sj= 'left_ik_joint_hip', ee= "left_ik_joint_ankle", sol = "ikRPsolver")
cmds.ikHandle(n= "left_ik_Handle_ball", sj= "left_ik_joint_ankle", ee= "left_ik_joint_ball", sol = "ikSCsolver")
cmds.ikHandle(n= "left_ik_Handle_toe", sj= "left_ik_joint_ball", ee= "left_ik_joint_toe", sol = "ikSCsolver")

'''Create groups for foot pivots'''
footGroups = ["group_foot_Pivot", "group_toe_pivot", "group_heel_pivot", "group_ball_pivot", "group_flap"]
for item in footGroups:
		cmds.group(n=item, empty=True, world=True)

#Query the positions of the joints
hipPos = cmds.xform("left_ik_joint_hip", q=True, ws=True, t=True)
anklePos = cmds.xform("left_ik_joint_ankle", q=True, ws=True, t=True)
ballPos = cmds.xform("left_ik_joint_ball", q=True, ws=True, t=True)
toePos = cmds.xform("left_ik_joint_toe", q=True, ws=True, t=True)

#Move the Toe, Ball and Flap groups to corresponding joints
cmds.xform("group_toe_pivot", ws=True, t=toePos)
cmds.xform("group_ball_pivot", ws=True, t=ballPos)
cmds.xform("group_flap", ws=True, t=ballPos)

#Parent the groups accordingly
cmds.parent('group_heel_pivot', 'group_foot_Pivot')
cmds.parent('group_toe_pivot', 'group_heel_pivot')
cmds.parent('group_ball_pivot', 'group_toe_pivot')
cmds.parent('group_flap', 'group_toe_pivot')
#Parent ikHandles to pivot groups
cmds.parent('left_ik_Handle_leg', 'group_ball_pivot')
cmds.parent('left_ik_Handle_ball', 'group_ball_pivot')
cmds.parent('left_ik_Handle_toe', 'group_flap')

#Create IK control for the foot
cmds.circle(n='left_ik_control_leg')

#Move the control pivot to the ankle joint
cmds.xform('left_ik_control_leg', t = anklePos, ws = True)

#Freeze Transformations on control
cmds.makeIdentity('left_ik_control_leg', apply=True, translate=True, normal=0, preserveNormals=True)

#Parent the foot pivot to the foot control
cmds.parent('group_foot_pivot', 'left_ik_control_leg')