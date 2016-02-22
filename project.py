#!/usr/bin/env python3

import os
import subprocess
import configparser

#######################
## Class definitions ##
#######################
class ConfigObject:
    """Empty object"""

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

def makeTemporaryDirectory():
    """Creates /tmp/armwiz/<number> and returns path.

    The <number> is iterated and will be the lowest available positive integer.

    Usage:
    myTempDir = makeTemporaryDirectory()
    """
    iteratedDir = 0
    while os.path.exists('/tmp/armwiz/{}'.format(iteratedDir)):
        iteratedDir += 1
    path = '/tmp/armwiz/{}'.format(iteratedDir)
    makePath(path)
    if os.path.exists(path):
        return path
    else:
        raise Exception('Could not make the path.')

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

def deployLibrary(targetProjectRootPath,library):
    """Deploy library to a project directory
    """
    # TODO If library is not in the armwiz libraries directory, git submodule init into armwiz, then copy into project.
    # TODO Use the --git flag (arguments.git) to enable/disable git commands.
    if not os.path.exists(targetProjectRootPath):
        raise Exception("The target path {} does not exist.".format(targetProjectRootPath))
    try:
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

def writeOption(inputFile,variable,option):
    """Assign a value to a variable.

    Usage:
    writeOption(<input file>,<variable name>,<new value>)

    Example:
    writeOption('Makefile','STM32CUBE_VERSION','STM32CubeF1')
    """
    # TODO Make this function accept a dictionary and input file. Recursive use
    #      of self similar to makeProjectTree()
    # TODO Trim white space when doing search and replace
    lines = []
    with open(inputFile) as workingFile:
        for line in workingFile:
            index=line.find(variable)
            if index == 0:
                line = line.replace(line, "{}={}\n".format(variable,option))
            lines.append(line)
    workingFile.close()
    with open(inputFile,'w') as outputFile:
            for line in lines:
                outputFile.write(line)
    outputFile.close()

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
        objectList.append(makeObjectFromConfigInfo(configInfo,section))
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
