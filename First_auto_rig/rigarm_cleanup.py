def createControl(ctrlInfo):
	for info in jointInfo:
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

#Hold IK joint names + positions
ik_joint_names = [['ik_shoulder_joint', [-7.253066, 0, 0.590704]],['ik_elbow_joint', [-1.365397, 0, -0.939316]], ['ik_wrist_joint', [4.193028, 0, 0.861846]], ['ik_wristEnd_joint', [5.316333, 0, 1.617172]]]
#Hold FK joint names + positions
fk_joint_names = [['fk_shoulder_joint', [-7.253066, 0, 0.590704]],['fk_elbow_joint', [-1.365397, 0, -0.939316]], ['fk_wrist_joint', [4.193028, 0, 0.861846]], ['fk_wristEnd_joint', [5.316333, 0, 1.617172]]]
#Hold rig joint names + positions
rig_joint_names = [['rig_shoulder_joint', [-7.253066, 0, 0.590704]],['rig_elbow_joint', [-1.365397, 0, -0.939316]], ['rig_wrist_joint', [4.193028, 0, 0.861846]], ['rig_wristEnd_joint', [5.316333, 0, 1.617172]]]

#Create rig controls
createControl(rig_joint_names)
cmds.select(cl=True)

#Create IK controls
ik_ctrl_info = [ik_joint_names[0][1], 'ctrl_ik_wrist', 'group_ctrl_IKwrist']
createControl(ik_ctrl_info)

#Create IK controls
fk_ctrl_info = []