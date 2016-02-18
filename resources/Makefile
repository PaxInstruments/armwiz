#  █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗
# ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝
# ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝
# ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝
# ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝
#                               by Pax Instruments

# Overview =================================================================== #
# This Makefile...
# TODO Write a good overview explaining this file to a novice.

# Project Specific Definitions =============================================== #
# This section should not need to be changed if your initial project generation
# options continue to meet your needs. If you change your target, you may need to
# modify this section manually. However, the suggested method is to generate a new
# project with your newly desired options and replace this Makefile with the new
# one. Relevant information for each target can be found in armwiz.config.

## STM32CubeX library
# -------------------
# This is the option that defines which ST Microsystems library to use for your
# target device.
STM32CUBE_VERSION=REPLACE_THIS_VALUE
# Option        Description
# ------        -----------
#             - An empty right-hand side leaves this value undefined
# STM32CubeF1 - ST Microsystems STM32CubeF1 libraries. Use this if you are going to
#               use an STM32F1 microcontroller.
# STM32CubeF2 - ST Microsystems STM32CubeF2 libraries
# STM32CubeF3 - ST Microsystems STM32CubeF3 libraries
# STM32CubeF4 - ST Microsystems STM32CubeF4 libraries

## ARM Core Endianness
# --------------------
# This section defines the projects endianness. In big-endian th emost significant byte
# is stored at the data's memory address with subsequent bytes is high memory addresses;
# the least significant byte (LSB) is in the highest memory address. Little-endian uses
# the revserse order, storing the LSB in the lowest memory address and MSB in the
# highest memory address. This can be found in the chip's datasheet.
ENDIANNESS=REPLACE_THIS_VALUE
# Option          Description
# ------          -----------
#               - An empty right-hand side leaves this value undefined
# big-endian    - Big endian
# little-endian - Little endian

## ARM Core
# ---------
# This is simply the core used in the target device.
# TODO Add option descriptions.
ARM_CORE=REPLACE_THIS_VALUE
# Option       Description
# ------       -----------
#               - An empty right-hand side leaves this value undefined
# cortex-m0     -
# cortex-m0plus -
# cortex-m1     -
# cortex-m3     -
# cortex-m4     -

## Instructions set?
# ------------------
# I think this is the insturction set used.
# TODO Learn and explain here
INSTRUCTION_SET=REPLACE_THIS_VALUE
# Option   Description
# ------   -----------
#        - An empty right-hand side leaves this value undefined
# arm    -
# thumb  -

# CMSIS MCU
# ---------
# This is the definition needed by the CMSIS libraries to set several parameters.
# TODO Add a list of which chips go with which flags.
# TODO Display path to file in whic this is needed.
CMSIS_MCU_FAMILY=REPLACE_THIS_VALUE
# Option        Description
# ------        -----------
# STM32F100xB - STM32F100C4, STM32F100R4, STM32F100C6, STM32F100R6, STM32F100C8,
#               STM32F100R8, STM32F100V8, STM32F100CB, STM32F100RB, STM32F100VB
# STM32F100xE - STM32F100RC, STM32F100VC, STM32F100ZC, STM32F100RD, STM32F100VD,
#               STM32F100ZD, STM32F100RE, STM32F100VE, STM32F100ZE
# STM32F101x6 - STM32F101C4, STM32F101R4, STM32F101T4, STM32F101C6, STM32F101R6,
#               STM32F101T6
# STM32F101xB - STM32F101C8, STM32F101R8, STM32F101T8, STM32F101V8, STM32F101CB,
#               STM32F101RB, STM32F101TB, STM32F101VB
# STM32F101xE - STM32F101RC, STM32F101VC, STM32F101ZC, STM32F101RD, STM32F101VD,
#               STM32F101ZD, STM32F101RE, STM32F101VE, STM32F101ZE
# STM32F101xG - STM32F101RF, STM32F101VF, STM32F101ZF, STM32F101RG, STM32F101VG,
#               STM32F101ZG
# STM32F102x6 - STM32F102C4, STM32F102R4, STM32F102C6, STM32F102R6
# STM32F102xB - STM32F102C8, STM32F102R8, STM32F102CB, STM32F102RB
# STM32F103x6 - STM32F103C4, STM32F103R4, STM32F103T4, STM32F103C6, STM32F103R6,
#               STM32F103T6
# STM32F103xB - STM32F103C8, STM32F103R8, STM32F103T8, STM32F103V8, STM32F103CB,
#               STM32F103RB, STM32F103TB, STM32F103VB
# STM32F103xE - STM32F103RC, STM32F103VC, STM32F103ZC, STM32F103RD, STM32F103VD,
#               STM32F103ZD, STM32F103RE, STM32F103VE, STM32F103ZE
# STM32F103xG - STM32F103RF, STM32F103VF, STM32F103ZF, STM32F103RG, STM32F103VG,
#               STM32F103ZG
# STM32F105xC - STM32F105R8, STM32F105V8, STM32F105RB, STM32F105VB, STM32F105RC,
#               STM32F105VC
# STM32F107xC - STM32F107RB, STM32F107VB, STM32F107RC, STM32F107VC

## Warning Flags
# --------------
# These are the flags for compiler warnings.
CC_WARNINGS=-Wall

## Other Compiler Flags
# ---------------------
# These are other compiler flags.
CC_OTHER_FLAGS+=-ffreestanding

# Linker Script
# -------------
# This is the script that tells the linker where all the bits go.
# TODO Make an armwiz linker script. Use ifdef statements to select the flash
# and RAM parameters.
LINKER_SCRIPT=REPLACE_THIS_VALUE

STM32_COMPILER_FLAGS+=-mcpu=${ARM_CORE}
STM32_COMPILER_FLAGS+=-m${INSTRUCTION_SET}
STM32_COMPILER_FLAGS+=-m${ENDIANNESS}
STM32_COMPILER_FLAGS+=${CC_WARNINGS}
STM32_COMPILER_FLAGS+=${CC_OTHER_FLAGS}
CMSIS_MCU+=-D${CMSIS_MCU_FAMILY}

# Toolchain ================================================================== #
# GNU ARM Embedded Toolchain
# Instruction for installing this toolchain can be found at ___________.
TOOLCHAIN_DIRECTORY=
CC=${TOOLCHAIN_DIRECTORY}arm-none-eabi-gcc
CXX=${TOOLCHAIN_DIRECTORY}arm-none-eabi-g++
LD=${TOOLCHAIN_DIRECTORY}arm-none-eabi-ld
AR=${TOOLCHAIN_DIRECTORY}arm-none-eabi-ar
AS=${TOOLCHAIN_DIRECTORY}arm-none-eabi-as
CP=${TOOLCHAIN_DIRECTORY}arm-none-eabi-objcopy
OD=${TOOLCHAIN_DIRECTORY}arm-none-eabi-objdump
NM=${TOOLCHAIN_DIRECTORY}arm-none-eabi-nm
SIZE=${TOOLCHAIN_DIRECTORY}arm-none-eabi-size
A2L=${TOOLCHAIN_DIRECTORY}arm-none-eabi-addr2line

###
# File names
PROJECT_NAME=gpio

###
# Directory Structure
BINDIR=binary
INCDIR=include
SRCDIR=source

###
# Find project source files
ASOURCES=$(shell find -L $(SRCDIR) -name '*.s')
CSOURCES=$(shell find -L $(SRCDIR) -name '*.c')
CXXSOURCES=$(shell find -L $(SRCDIR) -name '*.cpp')
# Find project header directories
INC=$(shell find -L $(INCDIR) -name '*.h' -exec dirname {} \; | uniq)
# Find library source Files
ifdef STM32CUBE_VERSION
CSOURCES+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/STM32F*xx_HAL_Driver -name '*.c' | grep -iv template | grep -iv example)
# CSOURCES+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/CMSIS/Device/ST/STM32F1xx -name '*.c' | grep -iv template | grep -iv example)
# CSOURCES+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/BSP/STM32F1xx_Nucleo -name '*.c' | grep -iv template | grep -iv example)
# CSOURCES+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/CMSIS -name '*.c' | grep -iv template | grep -iv example)
# Find library header directories
INC+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/STM32F*xx_HAL_Driver  -name '*.h' -exec dirname {} \; | uniq | grep -iv template | grep -iv example)
# INC+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/CMSIS/Device/ST/STM32F1xx -name '*.h' -exec dirname {} \; | uniq | grep -iv template | grep -iv example)
# INC+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/BSP/STM32F1xx_Nucleo -name '*.h' -exec dirname {} \; | uniq | grep -iv template | grep -iv example)
INC+=$(shell find -L libraries/${STM32CUBE_VERSION}/Drivers/CMSIS -name '*.h' -exec dirname {} \; | uniq | grep -iv template | grep -iv example)
endif

# Include the include directories
INCLUDES=$(INC:%=-I%)
# Find libraries
INCLUDES_LIBS=
LINK_LIBS=
# Create object list
OBJECTS=$(ASOURCES:%.s=%.o)
OBJECTS+=$(CSOURCES:%.c=%.o)
OBJECTS+=$(CXXSOURCES:%.cpp=%.o)
# Define output files ELF & IHEX
BINELF=$(PROJECT_NAME).elf
BINHEX=$(PROJECT_NAME).hex
BINBIN=$(PROJECT_NAME).bin

###
# MCU FLAGS
MCFLAGS+=${STM32_COMPILER_FLAGS}
# -nostdlib
# COMPILE FLAGS
#####
##### The two DEFS below will cause trouble. Find the new names for these.
#####
# DEFS=-DUSE_STDPERIPH_DRIVER
DEFS+=${CMSIS_MCU}
# DEFS+=-DARM_MATH_CM3
CFLAGS=-c $(MCFLAGS) $(DEFS) $(INCLUDES)
CXXFLAGS=-c $(MCFLAGS) $(DEFS) $(INCLUDES) -std=c++11
# LINKER FLAGS
LDSCRIPT=${LINKER_SCRIPT}
LDFLAGS =-T $(LDSCRIPT) $(MCFLAGS) --specs=nosys.specs $(INCLUDES_LIBS) $(LINK_LIBS)

###
# Build Rules
.PHONY: all release release-memopt debug clean

all: release-memopt

release-memopt-blame: CFLAGS+=-g
release-memopt-blame: CXXFLAGS+=-g
release-memopt-blame: LDFLAGS+=-g -Wl,-Map=$(BINDIR)/output.map
release-memopt-blame: release-memopt
release-memopt-blame:
	@echo "Top 10 space consuming symbols from the object code ...\n"
	$(NM) -A -l -C -td --reverse-sort --size-sort $(BINDIR)/$(BINELF) | head -n10 | cat -n # Output legend: man nm
	@echo "\n... and corresponging source files to blame.\n"
	$(NM) --reverse-sort --size-sort -S -tx $(BINDIR)/$(BINELF) | head -10 | cut -d':' -f2 | cut -d' ' -f1 | $(A2L) -e $(BINDIR)/$(BINELF) | cat -n # Output legend: man addr2line

release-memopt: DEFS+=-DCUSTOM_NEW -DNO_EXCEPTIONS
release-memopt: CFLAGS+=-Os -ffunction-sections -fdata-sections -fno-builtin # -flto
release-memopt: CXXFLAGS+=-Os -fno-exceptions -ffunction-sections -fdata-sections -fno-builtin -fno-rtti # -flto
release-memopt: LDFLAGS+=-Os -Wl,-gc-sections --specs=nano.specs # -flto
release-memopt: release

debug: CFLAGS+=-g
debug: CXXFLAGS+=-g
debug: LDFLAGS+=-g
debug: release

release: $(BINDIR)/$(BINHEX)

$(BINDIR)/$(BINHEX): $(BINDIR)/$(BINELF)
	$(CP) -O ihex $< $@
	@echo "Objcopy from ELF to IHEX complete!\n"

$(BINDIR)/$(BINBIN): $(BINDIR)/$(BINELF)
	$(CP) -O binary $^ $@
	@echo "Objcopy from ELF to BIN complete!\n"

##
# C++ linking is used.
#
# Change
#   $(CXX) $(OBJECTS) $(LDFLAGS) -o $@ to
#   $(CC) $(OBJECTS) $(LDFLAGS) -o $@ if
#   C linker is required.
$(BINDIR)/$(BINELF): $(OBJECTS)
	$(CXX) $(OBJECTS) $(LDFLAGS) -o $@
	@echo "Linking complete!\n"
	$(SIZE) $(BINDIR)/$(BINELF)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
	@echo "Compiled "$<"!\n"

%.o: %.c
	$(CC) $(CFLAGS) $< -o $@
	@echo "Compiled "$<"!\n"

%.o: %.s
	$(CC) $(CFLAGS) $< -o $@
	@echo "Assambled "$<"!\n"

clean:
	rm -f $(OBJECTS) $(BINDIR)/$(BINELF) $(BINDIR)/$(BINHEX) $(BINDIR)/$(BINBIN) $(BINDIR)/output.map
flash: $(BINDIR)/$(BINBIN)
		st-flash write $(BINDIR)/$(BINBIN) 0x8000000
deploy:
ifeq ($(wildcard /opt/openocd/bin/openocd),)
	/usr/bin/openocd -f /usr/share/openocd/scripts/board/stm32f4discovery.cfg -c "program bin/"$(BINELF)" verify reset"
else
	/opt/openocd/bin/openocd -f /opt/openocd/share/openocd/scripts/board/stm32f4discovery.cfg -c "program bin/"$(BINELF)" verify reset"
endif
