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
footGroups = ["group_foot_pivot", "group_toe_pivot", "group_heel_pivot", "group_ball_pivot", "group_flap"]
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
cmds.circle(n='left_ik_leg_control')

#Move the control pivot to the ankle joint
cmds.xform('left_ik_leg_control', t = anklePos, ws = True)

#Freeze Transformations on control
cmds.makeIdentity('left_ik_leg_control', apply=True, translate=True, normal=0, preserveNormals=True)

#Parent the foot pivot to the foot control
cmds.parent('group_foot_pivot', 'left_ik_leg_control')

#Create locator and snap to pelvis
cmds.spaceLocator(n = 'left_locatorPv_leg')
#pelvisPos = cmds.xform("joint_pelvis", q=True, ws=True, t=True)
cmds.xform('left_locatorPv_leg', ws = True, t = hipPos)

#Pole vector constrain ik handle and locator
cmds.poleVectorConstraint('left_locatorPv_leg','left_ik_Handle_leg', weight = 1)

#Create a float attribute called “Twist” on the ikFootCtrl controller.
cmds.addAttr('left_ik_leg_control', shortName = "Twist", longName = "Twist", defaultValue = 0, keyable = True)

#Create a plusMinusAverage utility, and call it pmaNode_LegTwist.
cmds.shadingNode("plusMinusAverage", asUtility=True, n='pmaNode_LegTwist'
#Create a multiplyDivide utility and call it mdNode_LegTwist.
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_LegTwist')

#Set up the connections
cmds.connectAttr('left_ik_leg_control.Twist', 'mdNode_LegTwist.input1X')
cmds.connectAttr('left_ik_leg_control.ry', 'mdNode_LegTwist.input1Y')
cmds.connectAttr('left_ik_joint_hip.ry', 'mdNode_LegTwist.input1Z')
cmds.setAttr('mdNode_LegTwist.input2X', -1)
cmds.setAttr('mdNode_LegTwist.input2Y', -1)
cmds.setAttr('mdNode_LegTwist.input2Z', -1)
cmds.connectAttr('mdNode_LegTwist.input1X', 'pmaNode_LegTwist.input1D[0]')
cmds.connectAttr('mdNode_LegTwist.input1Y', 'pmaNode_LegTwist.input1D[1]')
cmds.connectAttr('pmaNode_LegTwist.output1D', 'left_ik_Handle_leg.twist')

#Create nodes needed for stretchy IK
cmds.shadingNode("addDoubleLinear", asUtility=True, n='adlNode_LegStretch'
cmds.shadingNode("clamp", asUtility=True, n='clampNode_LegStretch')
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_LegStretch'
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_KneeStretch'
cmds.shadingNode("multiplyDivide", asUtility=True, n='mdNode_AnkleStretch'

#Add a "Stretch" attribute to ctrl_leg
cmds.addAttr('left_ik_control_leg', shortName = "Stretch", longName = "Stretch", defaultValue = 0)
cmds.setAttr('left_ik_control_leg.Stretch', e=True, k = True)

#Create a distance tool to measure distance between hip and ankle joints
'''Use Create/Measure Tools/Distance Tool. Snap one locator to
the ik hip joint and name it ‘lctrDis_hip’. Parent this locator to the pelvis joint
Snap the other locator to ikj_ankle and name it ‘lctrDis_ankle’.
Parent this locator to the heel group'''

#"hipPos" already exists
#hipPos = cmds.xform('ikj_hip', q=True, ws=True, t=True)

#"anklePos" already exists
#anklePos = cmds.xform('ikj_ankle', q=True, ws=True, t=True)

disDim = cmds.distanceDimension(sp=(hipPos), ep=(anklePos))

cmds.rename('distanceDimension1', 'disDimNode_legStretch')
cmds.rename('locator1', 'left_locator_hip_Distance')
cmds.rename('locator2', 'left_locator_ankle_Distance')
cmds.parent('left_locator_hip_Distance', 'joint_pelvis')
cmds.parent('left_locator_ankle_Distance', 'group_ball_pivot')