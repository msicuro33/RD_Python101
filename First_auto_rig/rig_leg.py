#Create left leg IK joints
cmds.joint(n='left_joint_pelvis', p=[-2, 4.212193, 2.628613], oj='xyz', sao = 'zup',ch = True)
cmds.joint(n='left_ik_joint_hip', p=[0, 4.212193, 2.628613])
cmds.joint(n='left_ik_joint_knee', p=[0 -0.0937814 4.174347])
cmds.joint(n='left_ik_joint_ankle', p=[0 -4.311428 2.319466])
cmds.joint(n='left_ik_joint_ball', p=[0, -3.9, 2.7])
cmds.joint(n='left_ik_joint_toe', p=[0, -3.9, 3.1])
cmds.select(d=True)