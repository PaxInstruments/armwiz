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
import subprocess
import os
import sys
import errno
import argparse
import configparser
import fileinput
import ntpath
import project

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
        action="append",
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



# def is_valid_file(parser, arg):
#     # TODO Add appropriate docstring
#     # TODO Understand this function. Maybe use the return open handler somewhere else.
#     if not os.path.exists(arg):
#         parser.error("The file {} does not exist!".format(arg))
#     else:
#         return open(arg, 'r')  # return an open file handle



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

    # Read configuration information
    configurationInformation = configparser.ConfigParser()
    try:
        configurationInformation.read(arguments.configfile)
        if len(configurationInformation.read(arguments.configfile)) == 0:
            raise Exception("File '{}' is empty or missing.".format(arguments.configfile))
    except:
        raise

    # Hangle all do-one-thing-and-exit arguments
    if arguments.L == True:
        # Print a list of all supported libraries
        project.printConfigList('library',configurationInformation)
        exit()
    elif arguments.T == True:
        # Print a list of all supported targets
        project.printConfigList('target',configurationInformation)
        exit()
    elif arguments.projectname == None:
        # If no project name is give, exit
        project.parser.print_help()
        exit()

    # Create temporary project directory
    projectTempDir = '{}/{}'.format(project.makeTemporaryDirectory(),arguments.projectname)
    print('Project temporary location: {}'.format(projectTempDir))
    sys.stdout.flush()
    projectSubdirectories = [
        'source',
        'libraries',
        'binary',
        'examples',
        '.git/modules/libraries']
    project.makeProjectTree(projectTempDir,projectSubdirectories)

    # Create target List
    if type(arguments.targetname) != list:
        pass
    else:
        targetList = project.makeObjectList(configurationInformation,arguments.targetname)

    # Create library List
    if type(arguments.libraryname) != list:
        pass
    else:
        libraryList = project.makeObjectList(configurationInformation,arguments.libraryname)

    # Deploy libraries
    for library in libraryList:
        print('Deploying {}/libraries/{}... '.format(projectTempDir,library.git_name),end="")
        sys.stdout.flush()
        project.deployLibrary(projectTempDir,library)
        if os.path.exists("{}/libraries/{}/".format(projectTempDir,library.git_name)):
            print('Okay')
        else:
            raise Exception('    - FAIL: Directory {} does not exist.')

    # # This is the blinky test copy
    # mainDotC = 'resources/stm32/source/main.c'
    #     # - Needs GPIO port (e.g. GPIOD)
    #     # - Needs GPOIO pin (e.g. GPIO_PIN_2)
    # mainDotH = 'resources/stm32/include/main.h'
    #     # - Needs HAL file (e.g. stm32f1xx_hal.h)
    # startupFile = 'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_stm32f103xb.s'
    #     # - Needs core type (e.g. cortex-m3)
    #     # - Needs FPU type (e.g. softfpv)
    #     # - Needs instruciton set (e.g. thumb)
    #     # - Needs BootRAM
    # itDotC = 'resources/stm32/source/stm32f1xx_it.c'
    #     # - Needs interrupt handler .h file (e.g. stm32f1xx_it.h)
    # itDotH = 'resources/stm32/include/stm32f1xx_it.h'
    #     # - Needs is own file name to prevent recursive inclusion (e.g. __STM32F1xx_IT_H)
    # systemFile = 'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/system_stm32f1xx.c'
    # halConf = 'libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/stm32f1xx_hal_conf.h'
    #     # - Copy this file and comment out unused libraries. There is a lot of target specific information in here.
    # # linkerFile = 'libraries/STM32CubeF1/Projects/STM32F103RB-Nucleo/Templates/TrueSTUDIO/STM32F103RB_Nucleo/STM32F103VB_FLASH.ld'
    linkerFile = 'resources/stm32xxx.ld'
    #     # - We need the per-target RAM and FLASH information. We can easily generate this file.
    # makefile = 'resources/Makefile'
    #     # - Needs the location of several target-specific folders
    # readme = 'resources/readme.txt'

    blinkyExampleList = {
        # <source file> : <destination subdirectory>
        'resources/stm32/source/main.c' : 'source',
        'resources/stm32/include/main.h' : 'include',
        'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_stm32f103xb.s' : 'source',
        'resources/stm32/source/stm32f1xx_it.c' : 'source',
        'resources/stm32/include/stm32f1xx_it.h' : 'include',
        'libraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Source/Templates/system_stm32f1xx.c' : 'source',
        'libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/stm32f1xx_hal_conf.h' : 'include',
        'resources/Makefile' : '.',
        'resources/readme.txt' : '.',
        linkerFile : '.'
    }
    exampleName = 'blinky'
    exampleSubfolders = ['binary','include','source']
    project.makeProjectTree("{}/examples/{}".format(projectTempDir,exampleName),exampleSubfolders)
    subprocess.call('cd {}/examples/{}; ln -s ../../libraries libraries'.format(projectTempDir,exampleName),shell=True)
    for sourceFile in blinkyExampleList:
        subprocess.call('cp {} {}/examples/{}/{}/'.format(sourceFile,projectTempDir,exampleName,blinkyExampleList[sourceFile]),shell=True)

    # Update Makefile values
    thisTarget = targetList[0]
    optionsList = {
        'PROJECT_NAME': arguments.projectname,
        'STM32CUBE_VERSION': thisTarget.stm32cube_version,
        'ENDIANNESS': thisTarget.endianness,
        'ARM_CORE': thisTarget.arm_core,
        'INSTRUCTION_SET': thisTarget.instruction_set,
        'CMSIS_MCU_FAMILY': thisTarget.cmsis_mcu_family,
        'LINKER_SCRIPT': ntpath.basename(linkerFile)
    }
    for option in optionsList:
        # print('{}: {}'.format(option,optionsList[option]))
        project.writeOption("{}/examples/{}/Makefile".format(projectTempDir,exampleName),option,optionsList[option])

    # Move temporary project directory to the final location
    subprocess.call('mv {} {}'.format(projectTempDir,arguments.output),shell=True)

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
