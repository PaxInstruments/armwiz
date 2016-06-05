#!/usr/bin/env python3

import os
import subprocess
import configparser
import glob
import ntpath

#######################
## Class definitions ##
#######################
class ConfigObject:
    """Empty object"""

# class testObject:
#     __init__(self):
#         self.name = "myName"

def replaceInFile(inputFile,valueDictionary):
    with open(inputFile) as workingFile:
        newText = replace(workingFile,valueDictionary)
        workingFile.close()
    with open(inputFile,'w') as outputFile:
        for line in newText:
            outputFile.write(line)
        outputFile.close()

def replace(workingFile,valueDictionary):
    """Replace entries in text using dictionary and return text."""
    lines = []
    for line in workingFile:
        for tag in valueDictionary:
            line = line.replace(tag,valueDictionary[tag])
        lines.append(line)
    return lines

def makePath(pathList):
    """Create a directory path from a string or list of strings and return
    the same path or list.

    Usage:
        makePath('<directory>')
        makePath(['<directory 1>','<directory 2>',...,'<directory n>'])
    Example:
    >>> makePath(['temp/dir1','temp/hello/dir2'])
    $ tree temp/
    temp/
    ├── dir1
    └── hello
        └── dir2
    """
    # TODO makePath() should verify the path it made exists and return the path
    #      it made, not the path it was told to make.
    # TODO Improve the error handling. It seems messy.
    if type(pathList) is str:
        os.makedirs(pathList)
        return pathList
    elif type(pathList) is list:
        for path in pathList:
            makePath(path)
        return paths
    else:
        raise Exception("Value for each path must be a string or a list of strings. {} is not a string.".format(path))

def makeProjectTree(root,paths):
    """ Create a directory tree inside of root directory and return True.
    Usage:
        makeProjectTree(<rootDirectory>,<list of paths>)

    Example:
    >>> makeProjectTree('~/myProject',['subDir1','subDir2'])
    $ tree ~/myProject # Executed in terminal
    ~/myProject
    ├── subDir1
    └── subDir2
    """
    # TODO Do something such that git knows to also track the empty directories.
    #      Add a .git file to each directory or use other method.
    # TODO Use the --git flag (arguments.git) to enable/disable git commands.
    if not type(root) is str:
        raise TypeError("Value for <root directory> must be a string. type({}) gives {}".format(root,type(root)))
    try:
        makePath(root)
        subprocess.call('cd {}; git init -q'.format(root),shell=True)
    except FileExistsError:
        raise FileExistsError("The directory {} already exists.".format(root))
    if type(paths) is str:
        try:
            makePath("{}/{}".format(root,paths))
        except FileExistsError:
            pass
        except:
            raise
    elif type(paths) is list:
        for path in paths:
            try:
                makePath("{}/{}".format(root,path))
            except:
                raise
    return True

def getStartupFile(root,family):
    sourceFile = subprocess.getoutput('find {}/libraries/STM32CubeF* -iname startup_* | grep -iv projects | grep gcc | grep -i {}'.format(root,family))
    return sourceFile

def getSystemCFile(root,family):
    series = family[:7]
    command = 'find {}/libraries/STM32CubeF* -iname system_{}*.c | grep -iv projects'.format(root,series)
    # command = 'find {}/libraries/STM32CubeF* -iname system_* | grep -iv projects | grep -i {}'.format(root,family[:6])
    sourceFile = subprocess.getoutput(command)
    return sourceFile

def getHALFile(root,family):
    series = family[:7]
    command = 'find {}/libraries/STM32CubeF* -iname stm32f*_hal_conf_template.h | grep -iv projects'.format(root,series)
    # command = 'find {}/libraries/STM32CubeF* -iname system_* | grep -iv projects | grep -i {}'.format(root,family[:6])
    sourceFile = subprocess.getoutput(command)
    return sourceFile

def deployExample(targetProjectRootPath,example,target):
    """Deploy example to project Directory"""
    subprocess.call('rsync -ac resources/examples/{} {}/examples/'.format(example.example_directory,targetProjectRootPath,example.example_directory),shell=True)
    subprocess.call('cd {}/examples/{}; ln -s ../../libraries libraries'.format(targetProjectRootPath,example.example_directory),shell=True)
    # TODO Make this work for more than just STM32 chips
    startupFile = getStartupFile(targetProjectRootPath,target.cmsis_mcu_family)
    # TODO The following two files should be found and not hard-coded.
    # HALConfFile = 'libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/stm32f1xx_hal_conf.h'
    HALConfFile = getHALFile(targetProjectRootPath,target.cmsis_mcu_family)
    newHAL = ntpath.basename(HALConfFile)[:18]
    interruptHeader = 'resources/stm32fxxx_it.h'
    interruptC = 'resources/stm32fxxx_it.c'
    # interruptFile = 'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/system_stm32f1xx.c'
    systemFile = getSystemCFile(targetProjectRootPath,target.cmsis_mcu_family)
    exampleFileList = {
        # <source file> : <destination subdirectory>
        startupFile : 'source/',  # Needs core type (e.g. cortex-m3), Needs FPU type (e.g. softfpv), Needs instruciton set (e.g. thumb), Needs BootRAM
        systemFile : 'source/',
        interruptHeader : 'include/',  # Needs core type (e.g. cortex-m3), Needs FPU type (e.g. softfpv), Needs instruciton set (e.g. thumb), Needs BootRAM
        interruptC : 'source/',
        HALConfFile : 'include/{}.h'.format(newHAL),  # Copy this file and comment out unused libraries. There is a lot of target specific information in here.
        target.makefile : '.',  # Needs the location of several target-specific folders
        target.readme : '.',
        target.linker_file : '.'  # We need the per-target RAM and FLASH information. We can easily generate this file.
    }
    for sourceFile in exampleFileList:
        subprocess.call('cp {} {}/examples/{}/{}'.format(sourceFile,targetProjectRootPath,example.example_directory,exampleFileList[sourceFile]),shell=True)
    try:
        subprocess.call('cd {}; git add examples/{}'.format(targetProjectRootPath,example.example_directory),shell=True)
        subprocess.call("cd {}; git commit -qam 'armwiz added {}'".format(targetProjectRootPath,example.proper_name),shell=True)
    except:
        raise

def deployLibrary(targetProjectRootPath,library):
    """Deploy library to a project directory
    """
    # TODO If library is not in the armwiz libraries directory, git submodule init into armwiz, then copy into project.
    # TODO Use the --git flag (arguments.git) to enable/disable git commands.
    if not os.path.exists(targetProjectRootPath):
        raise Exception("The target path {} does not exist.".format(targetProjectRootPath))
    try:
        subprocess.call('git submodule init libraries/{}'.format(library.git_name),shell=True)
        subprocess.call('git submodule update libraries/{}'.format(library.git_name),shell=True)
        subprocess.call('rsync -ac libraries/{} {}/libraries/'.format(library.git_name,targetProjectRootPath,library.git_name),shell=True)
    except:
        raise Exception('ERROR using rsync to copy {}'.format(library.proper_name))
    try:
        subprocess.call('rsync -ac .git/modules/libraries/{} {}/.git/modules/libraries/'.format(library.git_name,targetProjectRootPath,library.git_name),shell=True)
        moduleFile = open('{}/.gitmodules'.format(targetProjectRootPath), 'a')
        moduleFile.write("\n[submodule \"libraries/{}\"]\n".format(library.git_name))
        moduleFile.write("\tpath = libraries/{}\n".format(library.git_name))
        moduleFile.write("\turl = {}\n".format(library.git_url))
        moduleFile.close()
    except:
        raise Exception('ERROR copying git stuff')
    try:
        subprocess.call('cd {}; git add .gitmodules; git add libraries/{}; git submodule init -q '.format(targetProjectRootPath,library.git_name),shell=True)
    except:
        raise
    try:
        subprocess.call("cd {}; git commit -qam 'armwiz added {}'".format(targetProjectRootPath,library.proper_name),shell=True)
    except:
        raise

def printConfigList(entryType,configInfo):
    """Print a list of configuration entries and descriptions and return True."""
    print('Argument Name  Argument Description')
    print('-------------  --------------------------------')
    for entry in configInfo:
        try:
            if configInfo.get('{}'.format(entry),'item_type') == entryType:
                print('{:<12}   {}'.format(configInfo.get(entry,'cli_argument'),configInfo.get(entry,'short_description')))
        except configparser.NoOptionError:
            pass
        except:
            raise
    return True

def makeObjectList(configInfo,sectionList):
    objectList = []
    for section in sectionList:
        try:
            objectList.append(makeObjectFromConfigInfo(configInfo,section))
        except configparser.NoSectionError:
            pass
    return objectList

def makeObjectFromConfigInfo(configInfo,section):
    """Return an object"""
    thisObject = ConfigObject()
    sectionDict = dict(configInfo.items(section))
    for item in sectionDict:
        setattr(thisObject,item,configInfo.get(section,item))
    return thisObject

def main():
    pass

if __name__ == "__main__":
    main()
