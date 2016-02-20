#!/usr/bin/env python3

import configparser

class ConfigObject:
    """A config object."""

def makeObjectFromConfigInfo(configInfo,section):
    """Return an object"""
    thisObject=ConfigObject()
    sectionDict = dict(configInfo.items(section))
    for item in sectionDict:
        setattr(thisObject,item,configInfo.get(section,item))
    return thisObject

def main():
    # Config this
    configurationFilePath = 'configTest.config'
    configOption = 'mbed'

    # Open the config file
    configurationInformation = configparser.ConfigParser()
    try:
        configurationInformation.read(configurationFilePath)
    except:
        raise

    # Create a new configObject
    myNewObject = makeObjectFromConfigInfo(configurationInformation,configOption)

    # Print the configObject information
    myList = vars(myNewObject)
    for item in myList:
        print(item + ':',myList[item])

if __name__ == "__main__":
    main()
