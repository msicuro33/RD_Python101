import os
import sys
import maya.cmds as cmds

#References the RiggingTool.mod Module file in Maya Modules folder, looks like this:
'''
Adding new module = "+ Rigging_Tool 1.0 C:\Users\MATTI\Documents\GitHub\RD_Python101
Create Environment variable = "RIGGING_TOOL=C:\Users\MATTI\Documents\GitHub\RD_Python101"
Append to Mayas default scripts path = scripts: "C:\Users\MATTI\Documents\GitHub\RD_Python101"
'''

print("In User Setup")

sys.path.append("C:/Users/MATTI/Documents/GitHub/RD_Python101")
cmds.evalDeferred('import startup')