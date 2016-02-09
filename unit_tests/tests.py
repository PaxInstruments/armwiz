#!/usr/bin/env python3

import os
import armwiz

temporaryDirectory = ''
sampleProjectName = 'sampleProject'
sampleProjectList = ['dir1','dir2','dir3']
sampleProjectMixedList = ['dir1',['dir2','dir3']]

## Test printWizard()
if armwiz.printWizard():
	pass
else:
	print('FAIL: Cannot print the Wizard.')

## Test printHeader()
if armwiz.printHeader():
	pass
else:
	print('FAIL: Cannot print the header.')

print('\nPerforming armwiz unit tests:')

## Test makeTemporaryDirectory(directoryName)
print("makeTemporaryDirectory()... ",end='')
temporaryDirectory = armwiz.makeTemporaryDirectory('.')
if os.path.exists(temporaryDirectory):
	pass
	print('pass')
else:
	print('FAIL: Directory {} does not exist.')

## Test makeProjectTree()
print("makeProjectTree()... ",end='')
if armwiz.makeProjectTree('{}/{}'.format(temporaryDirectory,sampleProjectName),sampleProjectList):
	pass
	print('pass')
else:
	print('FAIL')