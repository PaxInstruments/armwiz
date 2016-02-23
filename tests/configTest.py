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
    objectList = []
    for section in configurationInformation:
        # print(section)
        a = makeObjectFromConfigInfo(configurationInformation,section)
        # print(vars(a))
        objectList.append(a)
    for thing in objectList:
        try:
            print('Object:', thing.cli_argument)
            myList = vars(thing)
            print('    item_type:', thing.item_type)
            print('    cli_argument:', thing.cli_argument)
            for item in myList:
                pass
                # print('  ',item + ':',myList[item])
        except AttributeError:
            pass
        except:
            raise

if __name__ == "__main__":
    main()
