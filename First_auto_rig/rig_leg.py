#Create left leg IK joints
cmds.joint(n='joint_pelvis', p=[-2, 4.212193, 2.628613])

cmds.joint(n='left_ik_joint_hip', p=[0, 4.212193, 2.628613])
cmds.joint(n='left_ik_joint_knee', p=[0, -0.0937814, 4.174347])
cmds.joint('left_ik_joint_hip', e = True, zso = True, oj = 'xyz', sao = 'yup') 
cmds.joint(n='left_ik_joint_ankle', p=[0, -4.311428, 2.319466])
cmds.joint('left_ik_joint_knee', e = True, zso = True, oj = 'xyz', sao = 'yup')
cmds.joint(n='left_ik_joint_ball', p=[0, -5.3, 4.7])
cmds.joint('left_ik_joint_ankle', e = True, zso = True, oj = 'xyz', sao = 'yup')
cmds.joint(n='left_ik_joint_toe', p=[0, -5.3, 5.8])

#Create IK Handles
cmds.ikHandle(n= "left_ik_Handle_leg", sj= 'left_ik_joint_hip', ee= "left_ik_joint_ankle", sol = "ikRPsolver"
cmds.ikHandle(n= "left_ik_Handle_ball", sj= "left_ik_joint_ankle", ee= "left_ik_joint_ball", sol = "ikSCsolver"
cmds.ikHandle(n= "left_ik_Handle_toe", sj= "left_ik_joint_ball", ee= "left_ik_joint_toe", sol = "ikSCsolver"
	