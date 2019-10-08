import maya.cmds as cmds
import json
import tempfile

def writeJson(fileName,data):
	with open(fileName, 'w') as outfile:
		json.dump(data, outfile)
	file.close(oufile)

def readJson(fileName):
	with open(fileName, 'r') as outfile:
		data = (open(fileName, 'r').read())
	return data