#!/usr/bin/env python3

import os, sys
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
sys.stdout.flush()
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
sampleProjectName = 1#'sampleProject'
sampleProjectList = ['source','include','libraries','.git/modules/libraries']
print("    - Generating project tree for {}.".format(sampleProjectName))
sys.stdout.flush()
try:
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
except:
	raise
## Test deployLibrary()
print("Tests for deployLibrary():")
print("    - Load library config file... ",end="")
try:
	armwizConfigFileName = 'armwiz.config'
	armwizConfig = configparser.ConfigParser()
	armwizConfig.read('armwiz.config')
	if len(armwizConfig.read(armwizConfigFileName)) == 0:
		raise Exception("File '{}'' is empty or missing.".format(armwizConfigFileName))
	print("Okay")
except:
	raise
libraryDeploymentList = ['library_mbed','library_freertos']
for libraryToDeploy in libraryDeploymentList:
	try:
		thisLibrary = armwiz.Library()
		thisLibrary.proper_name = armwizConfig.get('{}'.format(libraryToDeploy),'proper_name')
		thisLibrary.git_name = armwizConfig.get('{}'.format(libraryToDeploy),'git_name')
		thisLibrary.git_url = armwizConfig.get('{}'.format(libraryToDeploy),'git_url')
		print("    - rsyncing {}... ".format(thisLibrary.proper_name))
		print("      library is '{}'".format(thisLibrary.proper_name))
		print("      git_name is '{}'".format(thisLibrary.git_name))
		print("      root is {}".format(temporaryProjectRootDirectory))
		print("    - Deploying to {}/{}... ".format(temporaryProjectRootDirectory,thisLibrary.git_name),end="")
		sys.stdout.flush()
		armwiz.deployLibrary(temporaryProjectRootDirectory,thisLibrary)
		if os.path.exists("{}/libraries/{}/".format(temporaryProjectRootDirectory,thisLibrary.git_name)):
			print('Okay')
		else:
			raise Exception('    - FAIL: Directory {} does not exist.')
	except:
		raise



