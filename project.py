#!/usr/bin/env python3

import os
import subprocess

#######################
## Class definitions ##
#######################
class ConfigObject:
    """A config object."""

def makePath(paths):
    """Create a directory path from a string or list of strings and return
    the same path or list.

    Usage:
        makePath('<directory>')
        makePath(['<directory 1>','<directory 2>',...,'<directory n>'])
    Example:
    >>> makePath(['temp/dir1','temp/hello/dir2'])
    True
    $ tree temp/
    temp/
    ├── dir1
    └── hello
        └── dir2
    """
    # TODO makePath() should verify the path it made exists and return the path
    #      it made, not the path it was told to make.
    # TODO Improve the error handling. It seems messy.
    try:
        for entry in paths:
            if not type(entry) is str:
                raise TypeError("The type for each path must be a string. type({}) gives {}".format(entry,type(entry)))
    except TypeError:
        raise TypeError("The type for each path must be a string. type({}) gives {}".format(entry,type(entry)))
    if type(paths) is str:
        try:
            os.makedirs(paths)
            return paths
        except:
            raise
    elif type(paths) is list:
        for path in paths:
            makePath(path)
        return paths
    else:
        raise TypeError("Value for each path must be a string or a list of strings. {} is not a string.".format(path))

def makeTemporaryDirectory():
    """Creates /tmp/armwiz/<number> and returns path.

    The <number> is iterated and will be the lowest available positive integer.

    Usage:
    myTempDir = makeTemporaryDirectory()
    """
    try:
        iteratedDir = 0
        while os.path.exists('/tmp/armwiz/{}'.format(iteratedDir)):
            iteratedDir += 1
        path = '/tmp/armwiz/{}'.format(iteratedDir)
        makePath(path)
        if os.path.exists(path):
            return path
        else:
            raise Exception('Could not make the path.')
    except:
        raise

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

def main():
    pass

if __name__ == "__main__":
    main()
