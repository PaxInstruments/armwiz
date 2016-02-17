#  █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗
# ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝
# ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝
# ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝
# ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝
#                               by Pax Instruments

# Overview =================================================================== #
# This Makefile...

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

# Option        Description
# ------        -----------
#             - An empty right-hand side leaves this value undefined
# STM32CubeF1 - ST Microsystems STM32CubeF1 libraries. Use this if you are going to
#               use an STM32F1 microcontroller.
# STM32CubeF2 - ST Microsystems STM32CubeF2 libraries
# STM32CubeF3 - ST Microsystems STM32CubeF3 libraries
# STM32CubeF4 - ST Microsystems STM32CubeF4 libraries
STM32CUBE_VERSION=STM32CubeF1

## ARM Core Endianness
# --------------------
# This section defines the projects endianness. In big-endian th emost significant byte
# is stored at the data's memory address with subsequent bytes is high memory addresses;
# the least significant byte (LSB) is in the highest memory address. Little-endian uses
# the revserse order, storing the LSB in the lowest memory address and MSB in the
# highest memory address. This can be found in the chip's datasheet.
#
# option          Description
# ------          -----------
#               - An empty right-hand side leaves this value undefined
# big-endian    - Big endian
# little-endian - Little endian
ENDIANNESS=little-endian

## ARM Core
# ---------
# This is simply the core used in the target device.
#
# option       Description
# ------       -----------
#            - An empty right-hand side leaves this value undefined
# cortex-m3 -
# cortex-m4
ARM_CORE=cortex-m3


STM32_COMPILER_FLAGS+=-mcpu=${ARM_CORE}
STM32_COMPILER_FLAGS+=-mthumb
STM32_COMPILER_FLAGS+=-m${ENDIANNESS}
STM32_COMPILER_FLAGS+=-Wall
STM32_COMPILER_FLAGS+=-ffreestanding
CMSIS_MCU=-DSTM32F103xB
LINKER_SCRIPT=STM32F103VB_FLASH.ld


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
