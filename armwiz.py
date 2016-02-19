#!/usr/bin/env python3

#  █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗
# ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝
# ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝
# ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝
# ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝
#                               by Pax Instruments

# Notes
# =======
# - This code only fors for STM32F103XB.

# TODO Milestone 1
# ================
# TODO Function: Copy linker scrip based on armwiz.config entry
# TODO Function: rsync a file from source to destination and return path to
#      destination. call("rsync -ac <source> <destination>; cd <destination>",
#      shell=true)
# TODO Function:Generate Makefile based on a template and armwiz.config

# TODO Milestone 2
# ================
# TODO Make armwiz capable of running from any directory. All tasks are done
#      from the current directory.
# TODO Issue: Add a proper license header
# TODO Issue: Ensure git knows about empty directories in the project tree by putting
#      readmefiles in there or .git files if that makes sense.
# TODO Function: Generate README based on libraries copied.
# TODO Ignore duplicated library options while parsing arguments. This could happen
#      for free if armwiz first checks if a target library already exists.

# Icebox
# ======
# TODO Reach parity with the code that CubeMX generates. I should output
#      the same files.
# TODO Feature: download and compile the arm-none-eabi toolchain. Figure out a
#      way to include a toolchain or download a toolchain with
#      armwiz.
# TODO Make a tool that can be deployed within a project to give the project
#      some armz functionality. This would be handy for changing which target
#      processor is used or which which libraries are loaded. The armwiz project
#      can just be an empty project generated by itself.
# TODO Implement a spinner to display while each library is being copied
# TODO Function to generate linker scripts. It would be nice if this functionality
#      could be used independently of the rest of armwiz.
# TODO FreeRTOS: Generate FreeRTOSConfig.h
# TODO FreeRTOS: Make FreeRTOS checkout the most recent version from the tags
# TODO PROJECTS: Project generator will make a bare ARM project that does not use any
#      pripherial libraries. Just i++ and use a debugger to view it.
# TODO LIBRARIES GIT: List the download status of each library.
# TODO LIBRARIES: Make function to checkout the latest version or a specified version of
#      each library. Maybe have an entry in the libraries.config file
# TODO LIBRARIES: Add a function to pull in the desired submodules as they are needed.
# TODO OPTIONS GIT: Make git repo initilization command line option
# TODO OPTIONS GIT: If git is not present, do not initialize a git repo
# TODO OPTIONS GIT: Function: git submodule add a module into the armwiz git repo
# TODO If armwiz is pointed to an existing project, it should add any
#      specified libraries. Directly use git submodule add command. Maybe point
#      to a local repo to clone, then change to the github repo.
# TODO Can I combine the core, target, and other classes together? Maybe have a
#      parent class.

## Import standard libraries
from subprocess import call
import os
import sys
import errno
import argparse
import configparser
import fileinput
import ntpath

## Standard Python header information
__author__ = "Charles Edward Pax"
__copyright__ = "Copyright 2016, Pax Instruments LLC"
__date__ = "2016"
__credits__ = ["Charles Pax"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Charles Pax"
__email__ = "charles.pax@gmail.com"
__status__ = "Development"

#######################
## Class definitions ##
#######################

class Manufacturer(object):
    """The manufacturer of an object"""
    # TODO Add appropriate docstring
    def __init__(self):
        self.item_type = 'manufacturer'
        self.proper_name = ''
        self.website_url = ''

class Core(object):
    """The MCU core designed by ARM."""
    # TODO Add appropriate docstring
    def __init__(self):
        self.item_type = 'core'
        self.proper_name = ''
        self.chip_family = ''
        self.architecture = ''
        self.manufacturer = ''
        self.gcc_flag_mcpu = ''

class Target(object):
    """The target for which armwiz will generate a project. This could be
    a development board or just an MCU."""
    # TODO Add appropriate docstring
    def __init__(self):
        self.item_type = 'target'
        self.proper_name = ''
        self.mcu = ''
        self.cli_argument = ''
        self.core = ''
        self.manufacturer = ''
        self.short_description = ''
        self.long_description = ''
        self.website_url = ''

class Library(object):
    """Libraries in git."""
    # TODO Add appropriate docstring
    def __init__(self):
        self.item_type = 'library'
        self.proper_name = ''
        self.cli_argument = ''
        self.short_description = ''
        self.long_description = ''
        self.git_name = ''
        self.git_url = ''
        self.website_url = ''

##########################
## Function definitions ##
##########################
def printWizard():
    """Prints the wizard and returns True."""
    print("                             ____                   ")
    print("                          .'* *.'                   ")
    print("                       __/_*_*(_                    ")
    print("                      / _______ \                   ")
    print("                     _\_)/___\(_/_                  ")
    print("                    / _((\- -/))_ \                 ")
    print("                    \ \())(-)(()/ /                 ")
    print("                     ' \(((()))/ '                  ")
    print("                    / ' \)).))/ ' \                 ")
    print("                   / _ \ - | - /_  \                ")
    print("                  (   ( .;''';. .'  )               ")
    print("                  _\\\"__ /    )\ __\"/_            ")
    print("                    \/  \   ' /  \/                 ")
    print("                     .'  '...' ' )                  ")
    print("                      / /  |  \ \                   ")
    print("                     / .   .   . \                  ")
    print("                    /   .     .   \                 ")
    print("                   /   /   |   \   \                ")
    print("                 .'   /    b    '.  '.              ")
    print("             _.-'    /     Bb     '-. '-._          ")
    print("         _.-'       |      BBb       '-.  '-.       ")
    print("        (__________/\____.dBBBb.________)____)      ")
    return True

def printHeader():
    """Prints the header and returns True."""
    print("")
    print("     █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗")
    print("    ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝")
    print("    ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝ ")
    print("    ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝  ")
    print("    ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗")
    print("    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝")
    print("                    version {} by Pax Instruments"
        .format(__version__))
    return True

def parseArguments():
    """Parses command line arguments and returns ArgumentParser object."""
    parser = argparse.ArgumentParser(
        description='Generate a template embedded ARM project.',
        epilog="armwiz {}".format(__date__))
    parser.add_argument('-p','--projectname',
        help='Specify project name via -p <projectname>',
        metavar="<projectname>",
        required=False)
    parser.add_argument('-t','--targetname',
        help='Specify target microcontroller or processor via -t <targetname>',
        metavar="<targetname>",
        required=False)
    parser.add_argument('-l','--libraryname',
        help='Specify a library to include via -l <libraryname>',
        metavar="<libraryname>",
        action="append",
        required=False)
    parser.add_argument('-L',
        help='List all libraries available to -l <libraryname> and exit.',
        action="store_true",
        required=False)
    parser.add_argument('-T',
        help='List all targets available to -t <targetname> and exit',
        action="store_true",
        required=False)
    parser.add_argument('-c','--configfile',
        help='Specify a configuration file via -t <config file name>',
        default='armwiz.config',
        metavar="<config file name>",
        required=False)
    parser.add_argument('-o','--output',
        help='Target location -o <target location>',
        default='./',
        metavar="<target location>",
        required=False)
    parser.add_argument('-w','--wizard',
        help='Print the wizard',
        action="store_true",
        required=False)
    parser.add_argument('-n','--no_header',
        help='Print the wizard',
        default=False,
        action="store_true",
        required=False)
    parser.add_argument('-g','--git',
        help='Initialize project as a git repository. Default is True. Ignored if git is not present.',
        default=True,
        action="store_true",
        required=False)
    parser.add_argument('-v','--verbose',
        help='Print extra information to the terminal',
        action="store_true",
        required=False)
    parser.add_argument('-q','--quite',
        help='Suppress terminal message as best we can',
        action="store_true",
        required=False)
    parser.add_argument('--version',
        version='%(prog)s {version}'.format(version=__version__),
        action='version')
    return parser

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
        call('cd {}; git init -q'.format(root),shell=True)
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
        call('rsync -ac libraries/{} {}/libraries/'.format(library.git_name,targetProjectRootPath,library.git_name),shell=True)
    except:
        raise Exception('ERROR using rsync to copy {}'.format(library.proper_name))
    try:
        call('rsync -ac .git/modules/libraries/{} {}/.git/modules/libraries/'.format(library.git_name,targetProjectRootPath,library.git_name),shell=True)
        moduleFile = open('{}/.gitmodules'.format(targetProjectRootPath), 'a')
        moduleFile.write("\n[submodule \"libraries/{}\"]\n".format(library.git_name))
        moduleFile.write("\tpath = libraries/{}\n".format(library.git_name))
        moduleFile.write("\turl = {}\n".format(library.git_url))
        moduleFile.close()
    except:
        raise Exception('ERROR copying git stuff')
    try:
        call('cd {}; git add .gitmodules; git add libraries/{}; git submodule init -q '.format(targetProjectRootPath,library.git_name),shell=True)
    except:
        raise
    try:
        call("cd {}; git commit -qam 'armwiz added {}'".format(targetProjectRootPath,library.proper_name),shell=True)
    except:
        raise

# def is_valid_file(parser, arg):
#     # TODO Add appropriate docstring
#     # TODO Understand this function. Maybe use the return open handler somewhere else.
#     if not os.path.exists(arg):
#         parser.error("The file {} does not exist!".format(arg))
#     else:
#         return open(arg, 'r')  # return an open file handle

def printConfigList(entryType,configurationFilePath):
    """Print a list of configuration entries and descriptions and return True."""
    configurationInformation = configparser.ConfigParser()
    try:
        configurationInformation.read(configurationFilePath)
    except:
        raise
    if len(configurationInformation.read(configurationFilePath)) == 0:
        raise Exception("File '{}'' is empty or missing.".format(configurationFilePath))
        return False
    else:
        print('Argument Name  Argument Description')
        print('-------------  --------------------------------')
        for entry in configurationInformation:
            try:
                if configurationInformation.get('{}'.format(entry),'item_type') == entryType:
                    print('{:<12}   {}'.format(configurationInformation.get(entry,'cli_argument'),configurationInformation.get(entry,'short_description')))
            except configparser.NoOptionError:
                pass
            except:
                raise
        return True

def writeOption(inputFile,variable,option):
    """Assign a value to a variable.

    Usage:
    writeOption(<input file>,<variable name>,<new value>)

    Example:
    writeOption('Makefile','STM32CUBE_VERSION','STM32CubeF1')
    """
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

def deployMakefile():
    pass

def main():
    """
    armwiz project template generator for ARM processors and development
    boards.

    Usage: armwiz.py [-h] [-p <projectname>] [-t <targetname>] [-l <libraryname>]
                     [-L] [-T] [-w] [-v] [-q] [--version]
    Example:
    The example below will make a project named 'myProject' for the STM32F4 Discovery
    board and deploy within it the ARM mbed libraries.

    $ armwiz.py -p myProject -t stm32f4discovery --l mbed
    """

    # Parse all command line arguments
    parser = parseArguments()
    arguments = parser.parse_args()

    # Handle all do-then-proceed arguments
    if arguments.wizard == True:
        printWizard()
    if arguments.no_header == False:
        printHeader()

    # Hangle all do-one-thing-and-exit arguments
    if arguments.L == True:
        printConfigList('library',arguments.configfile)
        exit()
    elif arguments.T == True:
        printConfigList('target',arguments.configfile)
        exit()
    elif arguments.projectname == None:
        parser.print_help()
        exit()

    # Create temporary project directory
    emptyTempDir = makeTemporaryDirectory()
    projectTempDir = '{}/{}'.format(emptyTempDir,arguments.projectname)
    print('Project temporary location: {}'.format(projectTempDir))
    sys.stdout.flush()
    projectSubdirectories = ['source','libraries','binary','examples','.git/modules/libraries']
    makeProjectTree(projectTempDir,projectSubdirectories)

    # Deploy libraries to temporary project directory
    configurationInformation = configparser.ConfigParser()
    try:
        configurationInformation.read(arguments.configfile)
    except:
        raise
    if len(configurationInformation.read(arguments.configfile)) == 0:
        raise Exception("File '{}' is empty or missing.".format(arguments.configfile))
    else:
        for libraryName in arguments.libraryname:
            for section in configurationInformation:
                thisLibrary = Library()
                try:
                    if configurationInformation.get('{}'.format(section),'cli_argument') == libraryName:
                        sys.stdout.flush()
                        thisLibrary.proper_name = configurationInformation.get('{}'.format(section),'proper_name')
                        thisLibrary.git_name = configurationInformation.get('{}'.format(section),'git_name')
                        thisLibrary.git_url = configurationInformation.get('{}'.format(section),'git_url')
                        thisLibrary.website_url = configurationInformation.get('{}'.format(section),'website_url')
                        try:
                            print('Deploying {}/libraries/{}... '.format(projectTempDir,thisLibrary.git_name),end="")
                            sys.stdout.flush()
                            deployLibrary(projectTempDir,thisLibrary)
                            if os.path.exists("{}/libraries/{}/".format(projectTempDir,thisLibrary.git_name)):
                                print('Okay')
                            else:
                                raise Exception('    - FAIL: Directory {} does not exist.')
                        except:
                            raise
                except configparser.NoOptionError:
                    pass
                except:
                    raise

    # # Copy GPIO example
    # call('rsync -ac resources/gpio_example/ {}/examples/gpio_example'.format(projectTempDir),shell=True)
    # call('cd {}/examples/gpio_example; ln -s ../../libraries libraries'.format(projectTempDir),shell=True)
    # linkerScript = 'libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/TARGET_NUCLEO_F103RB/TOOLCHAIN_GCC_ARM/STM32F103XB.ld'
    # call('cp {} {}/examples/gpio_example/myLinkerScript.ld'.format(linkerScript,projectTempDir),shell=True)
    # # Copy stm32 example
    # call('rsync -ac resources/stm32/ {}/examples/stm32'.format(projectTempDir),shell=True)
    # call('cd {}/examples/stm32; ln -s ../../libraries libraries'.format(projectTempDir),shell=True)
    # linkerScript = 'libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/TARGET_NUCLEO_F103RB/TOOLCHAIN_GCC_ARM/STM32F103XB.ld'
    # call('cp {} {}/examples/stm32/myLinkerScript.ld'.format(linkerScript,projectTempDir),shell=True)
    # # Other crap
    # # call('rsync -ac libraries/STM32CubeF1/Projects/STM32F103RB-Nucleo/Examples/GPIO/GPIO_IOToggle/ {}/examples/GPIO_IOToggle/'.format(projectTempDir),shell=True)
    # #call('rsync -ac resources/gpio_template/ {}'.format(projectTempDir),shell=True)


    # This is the blinky test copy
    exampleName = 'blinky'
    mainDotC = 'resources/stm32/source/main.c'
        # - Needs GPIO port (e.g. GPIOD)
        # - Needs GPOIO pin (e.g. GPIO_PIN_2)
    mainDotH = 'resources/stm32/include/main.h'
        # - Needs HAL file (e.g. stm32f1xx_hal.h)
    startupFile = 'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_stm32f103xb.s'
        # - Needs core type (e.g. cortex-m3)
        # - Needs FPU type (e.g. softfpv)
        # - Needs instruciton set (e.g. thumb)
        # - Needs BootRAM
    itDotC = 'resources/stm32/source/stm32f1xx_it.c'
        # - Needs interrupt handler .h file (e.g. stm32f1xx_it.h)
    itDotH = 'resources/stm32/include/stm32f1xx_it.h'
        # - Needs is own file name to prevent recursive inclusion (e.g. __STM32F1xx_IT_H)
    systemFile = 'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/system_stm32f1xx.c'
    halConf = 'libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/stm32f1xx_hal_conf.h'
        # - Copy this file and comment out unused libraries. There is a lot of target specific information in here.
    # linkerFile = 'libraries/STM32CubeF1/Projects/STM32F103RB-Nucleo/Templates/TrueSTUDIO/STM32F103RB_Nucleo/STM32F103VB_FLASH.ld'
    linkerFile = 'resources/stm32xxx.ld'
        # - We need the per-target RAM and FLASH information. We can easily generate this file.
    makefile = 'resources/Makefile'
        # - Needs the location of several target-specific folders
    readme = 'resources/readme.txt'

    # # This copy of the blinky paths works
    # exampleName = 'blinky'
    # mainDotC = 'resources/stm32/source/main.c'
    # mainDotH = 'resources/stm32/include/main.h'
    # startupFile = 'resources/stm32/source/startup_stm32f103xb.s'
    # itDotC = 'resources/stm32/source/stm32f1xx_it.c'
    # itDotH = 'resources/stm32/include/stm32f1xx_it.h'
    # systemFile = 'resources/stm32/source/system_stm32f1xx.c'
    # halConf = 'resources/stm32/include/stm32f1xx_hal_conf.h'
    # linkerFile = 'resources/stm32/STM32F103VB_FLASH.ld'
    # makefile = 'resources/Makefile'
    # readme = 'resources/readme.txt'

    # Deploy blinky example
    exampleSubfolders = ['binary','include','source']
    makeProjectTree("{}/examples/{}".format(projectTempDir,exampleName),exampleSubfolders)
    call('cd {}/examples/{}; ln -s ../../libraries libraries'.format(projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/source/'.format(mainDotC,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/include/'.format(mainDotH,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/source/'.format(startupFile,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/source/'.format(itDotC,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/include/'.format(itDotH,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/source/'.format(systemFile,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/include/'.format(halConf,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/'.format(makefile,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/'.format(readme,projectTempDir,exampleName),shell=True)
    call('cp {} {}/examples/{}/'.format(linkerFile,projectTempDir,exampleName),shell=True)

    # Update Makefile values
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'PROJECT_NAME','myProject')
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'STM32CUBE_VERSION','STM32CubeF1')
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'ENDIANNESS','little-endian')
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'ARM_CORE','cortex-m3')
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'INSTRUCTION_SET','thumb')
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'CMSIS_MCU_FAMILY','STM32F103xB')
    writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),'LINKER_SCRIPT',ntpath.basename(linkerFile))

    # Move temporary project directory to the final location
    call('mv {} {}'.format(projectTempDir,arguments.output),shell=True)

    # TODO Write readme.md files to the temporary project directory tree folders
    # TODO Generate Makefile
    # TODO Copy Makefile to project temp directory
    # TODO Generate linker script
    # TODO Copy linker scrip to project temp directory
    # TODO Generate hello world code
    # TODO Copy hello worl code to temp project directory
    # TODO mv temporary froject directory to destination


if __name__ == "__main__":
    # TODO Read about python file structure
    #      https://www.artima.com/weblogs/viewpost.jsp?thread=4829
    main()
