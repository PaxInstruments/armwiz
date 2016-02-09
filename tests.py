#!/usr/bin/env python3

import os
import armwiz
import configparser

sampleProjectMixedList = ['dir1',['dir2','dir3']]

## Print header and information
armwiz.printWizard()
armwiz.printHeader()
print('\nThis program test the functionality of armwiz.')

## Test makeTemporaryDirectory(directoryName)
print("Tests for makeTemporaryDirectory():")
temporaryDirectoryName = 'test'
print("    - Making temporary directory '{}'... ".format(temporaryDirectoryName),end="")
try:
	temporaryDirectoryPath = armwiz.makeTemporaryDirectory(temporaryDirectoryName)
except:
	print('    - FAIL: Could not make directory')
if os.path.exists(temporaryDirectoryPath):
	print('Okay')
	print("      Path is {}".format(temporaryDirectoryPath))
else:
	print('    - FAIL: Directory {} does not exist.')

## Test makeProjectTree()
print("Tests for makeProjectTree(): ")
sampleProjectName = 'sampleProject'
sampleProjectList = ['source','include','libraries']
print("    - Generating project tree for {}.".format(sampleProjectName))
if armwiz.makeProjectTree('{}/{}'.format(temporaryDirectoryPath,sampleProjectName),sampleProjectList):
	print('    - {}/{} Okay'.format(temporaryDirectoryPath,sampleProjectName))
	for subdir in sampleProjectList:
		print('    - {}/{}/{} '.format(temporaryDirectoryPath,sampleProjectName,subdir),end="")
		if os.path.exists('{}/{}/{}'.format(temporaryDirectoryPath,sampleProjectName,subdir)):
			print('Okay')
		else:
			print('FAIL')
	temporaryProjectRootDirectory = "{}/{}".format(temporaryDirectoryPath,sampleProjectName)
else:
	print('FAIL')

## Test deployLibrary()
print("Tests for deployLibrary():")
print("    - Load library config file... ",end="")
try:
	armwizConfigFileName = 'armwiz.config'
	armwizConfig = configparser.ConfigParser()
	armwizConfig.read('armwiz.config')
	if len(armwizConfig.read(armwizConfigFileName)) == 0:
		raise Exception("File '{}'' is empty or missing.".format(armwizConfigFileName))
except:
	raise
libraryDeploymentList = ['library_mbed']
for option in libraryDeploymentList:
	if option == 'item_type':
		try:
			armwizConfig.get('{}'.format(option),'cli_argument')
			print(option)
		except:
			raise
for libraryToDeploy in libraryDeploymentList:
	try:
		thisLibrary = armwiz.Library()
		thisLibrary.proper_name = armwizConfig.get('{}'.format(libraryToDeploy),'proper_name')
		thisLibrary.cli_argument = armwizConfig.get('{}'.format(libraryToDeploy),'cli_argument')
		thisLibrary.git_name = armwizConfig.get('{}'.format(libraryToDeploy),'git_name')
		thisLibrary.git_url = armwizConfig.get('{}'.format(libraryToDeploy),'git_url')
	except:
		raise
print("Okay")
print("    - rsync library... ")
try:
	print("      library is {}".format(thisLibrary.proper_name))
	print("      git_name is {}".format(thisLibrary.git_name))
	print("      root is {}".format(temporaryProjectRootDirectory))
	armwiz.deployLibrary(temporaryProjectRootDirectory,thisLibrary)
except:
	raise
# if os.path.exists(temporaryDirectoryPath):
# 	print('Okay')
# 	print("      Path is {}".format(temporaryDirectoryPath))
# else:
# 	print('    - FAIL: Directory {} does not exist.')


