import os
import sys
import maya.cmds as cmds


print("In User Setup")

sys.path.append("C:/Users/MATTI/Documents/GitHub/RD_Python101")
cmds.evalDeferred('import startup')