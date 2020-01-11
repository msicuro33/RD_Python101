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
cmds.addAttr('left_ik_control_leg', shortName = "Stretch", longName = "Stretch", defaultValue = 0, keyable = True)

#Create a distance tool to measure distance between hip and ankle joints
'''Use Create/Measure Tools/Distance Tool. Snap one locator to
the ik hip joint and name it ‘lctrDis_hip’. Parent this locator to the pelvis joint
Snap the other locator to ikj_ankle and name it ‘lctrDis_ankle’.
Parent this locator to the heel group'''

#"hipPos" already exists
#hipPos = cmds.xform('ikj_hip', q=True, ws=True, t=True)
#"anklePos" already exists
#anklePos = cmds.xform('ikj_ankle', q=True, ws=True, t=True)

#Make a new locator so the Distance tool doesn't use the "left_locatorPv_leg" 
#as the starting point
tempLoc = cmds.spaceLocator()
cmds.xform(tempLoc, ws = True, t = hipPos)


disDim = cmds.distanceDimension(startPoint=(hipPos), endPoint=(anklePos))

cmds.rename('distanceDimension1', 'disDimNode_legStretch')
cmds.rename('locator1', 'left_locator_hip_Distance')
cmds.rename('locator2', 'left_locator_ankle_Distance')
cmds.parent('left_locator_hip_Distance', 'joint_pelvis')
cmds.parent('left_locator_ankle_Distance', 'group_ball_pivot')

#Get the translate X value of the Knee and Ankle to get the length of the leg when fully extended
kneeLen = cmds.getAttr('left_ik_joint_knee.tx')
print(kneeLen)
ankleLen = cmds.getAttr('left_ik_joint_ankle.tx')
print(ankleLen)
legLen = (ankleLen + kneeLen)
print(legLen)

#Enter the length values into the corresponding nodes
cmds.setAttr('adlNode_LegStretch.input2', legLen)
cmds.setAttr('mdNode_LegStretch.input2X', legLen)
cmds.setAttr('mdNode_KneeStretch.input2X', kneeLen)
cmds.setAttr('mdNode_AnkleStretch.input2X', ankleLen)

#Connect the nodes to get the final stretch value that will be applied to our joints. 
#The clamp node lets us control the amount of stretch
cmds.connectAttr('left_ik_control_leg.Stretch', 'adlNode_LegStretch.input1')
cmds.setAttr ("clampNode_LegStretch.minR", 12.800084)
cmds.setAttr ("mdNode_LegStretch.operation", 2)


#Connect the distance dimension so we always know the current length of the leg.
cmds.connectAttr('disDimNode_legStretch.distance', 'clampNode_LegStretch.inputR')
cmds.connectAttr('adlNode_LegStretch.output', 'clampNode_LegStretch.maxR')

#Now we feed the total value into a multiply divide so we can distribute the value to our joints.
cmds.connectAttr('clampNode_LegStretch.outputR', 'mdNode_LegStretch.input1X')
cmds.connectAttr('mdNode_LegStretch.outputX', 'mdNode_KneeStretch.input1X')
cmds.connectAttr('mdNode_LegStretch.outputX', 'mdNode_AnkleStretch.input1X')

#Finally, we output our new values into the translateX of the knee and ankle joints.
cmds.connectAttr('mdNode_KneeStretch.outputX', 'left_ik_joint_knee.tx')
cmds.connectAttr('mdNode_AnkleStretch.outputX', 'left_ik_joint_ankle.tx')

'''Step 7: Create the Foot Roll'''
#Add a "Roll Break" and "Foot Roll" attribute to the leg control
cmds.addAttr('left_ik_control_leg', shortName = "Roll_Break", longName = "Roll_Break", defaultValue = 0, keyable = True)
cmds.addAttr('left_ik_control_leg', shortName = "Foot_Roll", longName = "Foot_Roll", defaultValue = 0, keyable = True)

#Setup the foot roll and Create utility nodes
cmds.shadingNode("condition", asUtility=True, n='conditionNode_ballRoll')
cmds.shadingNode("condition", asUtility=True, n='conditionNode_negBallRoll')
cmds.shadingNode("condition", asUtility=True, n='conditionNode_toeRoll')
cmds.shadingNode("plusMinusAverage", asUtility=True, n='pmaNode_ballRoll')
cmds.shadingNode("plusMinusAverage", asUtility=True, n='pmaNode_toeRoll')
cmds.shadingNode("condition", asUtility=True, n='conditionNode_heelRoll')
cmds.setAttr('pmaNode_toeRoll.operation', 2)
cmds.setAttr("conditionNode_toeRoll.operation", 2)
cmds.setAttr("conditionNode_toeRoll.colorIfFalseR", 0)
cmds.setAttr("conditionNode_toeRoll.colorIfFalseG", 0)
cmds.setAttr("conditionNode_toeRoll.colorIfFalseB", 0)
cmds.setAttr('conditionNode_heelRoll.operation', 4)
cmds.setAttr('conditionNode_heelRoll.colorIfFalseB', 0)
cmds.setAttr('conditionNode_heelRoll.colorIfFalseR', 0)
cmds.setAttr('conditionNode_heelRoll.colorIfFalseG', 0)
cmds.setAttr("pmaNode_ballRoll.operation", 2)
cmds.setAttr("conditionNode_negBallRoll.operation", 3)
cmds.setAttr("conditionNode_ballRoll.operation", 3)

#Setup Toe
cmds.connectAttr('left_ik_control_leg.Foot_Roll', 'conditionNode_toeRoll.firstTerm')
cmds.connectAttr('left_ik_control_leg.Foot_Roll', 'conditionNode_toeRoll.colorIfTrueR')
cmds.connectAttr('left_ik_control_leg.Roll_Break', 'conditionNode_toeRoll.secondTerm')
cmds.connectAttr('left_ik_control_leg.Roll_Break', 'conditionNode_toeRoll.colorIfFalseR')
cmds.connectAttr('left_ik_control_leg.Roll_Break', 'pmaNode_toeRoll.input1D[1]')
cmds.connectAttr('conditionNode_toeRoll.outColorR', 'pmaNode_toeRoll.input1D[0]')
cmds.connectAttr('pmaNode_toeRoll.output1D', 'group_toe_pivot.rx')

#Setup Heel
cmds.connectAttr('left_ik_control_leg.Foot_Roll', 'conditionNode_heelRoll.firstTerm')
cmds.connectAttr('left_ik_control_leg.Foot_Roll', 'conditionNode_heelRoll.colorIfTrueR')
cmds.connectAttr('conditionNode_heelRoll.outColorR', 'group_heel_pivot.rotateX')

#Setup Ball
cmds.connectAttr('left_ik_control_leg.Foot_Roll', 'conditionNode_ballRoll.firstTerm')
cmds.connectAttr('left_ik_control_leg.Foot_Roll', 'conditionNode_ballRoll.colorIfTrueR')
cmds.connectAttr('left_ik_control_leg.Roll_Break', 'conditionNode_negBallRoll.secondTerm')
cmds.connectAttr('left_ik_control_leg.Roll_Break', 'conditionNode_negBallRoll.colorIfTrueR')
cmds.connectAttr('conditionNode_negBallRoll.outColorR', 'pmaNode_ballRoll.input1D[0]')
cmds.connectAttr('group_toe_pivot.rx', 'pmaNode_ballRoll.input1D[1]')
cmds.connectAttr('pmaNode_ballRoll.output1D', 'group_ball_pivot.rx')
cmds.connectAttr('conditionNode_ballRoll.outColorR', 'conditionNode_negBallRoll.firstTerm')
cmds.connectAttr('conditionNode_ballRoll.outColorR', 'conditionNode_negBallRoll.colorIfFalseR')

#Make the Toe Flap attribute and connect to the flap group
cmds.addAttr('left_ik_control_leg', shortName='Toe_Flap', longName='Toe_Flap', defaultValue= 0, keyable = True)
cmds.connectAttr('left_ik_control_leg.Toe_Flap', 'group_flap.rx')

'''Step 8: Pivot for Bank and Twist'''
#Create a new control object for the foot pvot and move it to the Ball group
cmds.circle(n='left_ctrl_footPivot')
cmds.xform('left_ctrl_footPivot', t=ballPos)

#Create an empty group for the foot pivot control
cmds.group(n='group_ctrl_footPivot', empty=True)

#Parent the foot pivot ctrl group to the footPivot control.
cmds.parent('group_ctrl_footPivot', 'left_ctrl_footPivot')

#Parent the ctrl_footPivot to ctrl_foot and freeze transforms (make identiy) on ctrl_footPivot.
cmds.parent('left_ctrl_footPivot', 'left_ik_control_leg')
cmds.makeIdentity('left_ctrl_footPivot', apply=True)

#Now we will connect the grp_ctrl_footPivot.translate to grp_footPivot.rotatePivot
cmds.connectAttr('group_ctrl_footPivot.translate', 'group_ctrl_footPivot.rotatePivot')

#Move group_ctrl_footPivot to the position of the ball group.
cmds.xform('group_ctrl_footPivot', t=ballPos)

'''Wrap up:'''
#Make a couple more attributes for twist and bank, then hook those up to the grp_footPivot.
cmds.addAttr('left_ik_control_leg', shortName='Foot_Pivot', longName='Foot_Pivot', defaultValue = 0, keyable = True)
cmds.addAttr('left_ik_control_leg', shortName='Foot_Bank', longName='Foot_Bank', defaultValue = 0, keyable = True)
cmds.connectAttr('left_ik_control_leg.Foot_Pivot', 'group_foot_pivot.ry')
cmds.connectAttr('left_ik_control_leg.Foot_Bank', 'group_foot_pivot.rz')

