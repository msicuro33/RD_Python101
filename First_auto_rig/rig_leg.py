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
cmds.xform("grp_toe", ws=True, t=toePos)
cmds.xform("grp_ball", ws=True, t=ballPos)
cmds.xform("grp_flap", ws=True, t=ballPos)

#Parent the groups accordingly
cmds.parent('grp_heel', 'grp_footPivot')
cmds.parent('grp_toe', 'grp_heel')
cmds.parent('grp_ball', 'grp_toe')
cmds.parent('grp_flap', 'grp_toe')
cmds.parent('ikh_leg', 'grp_ball')
cmds.parent('ikh_ball', 'grp_ball')
cmds.parent('ikh_toe', 'grp_flap')

#Parent the 
cmds.parent('group_foot_pivot', 'left_ik_Handle_leg')