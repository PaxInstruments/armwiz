# User Configuration ====================================================#
PROJECT_NAME=gpio_example
MAIN_SOURCE_FILE=main.c
LINKER_SCRIPT=myLinkerScript.ld

# Output files ==========================================================#
EXECUTABLE=$(PROJECT_NAME).elf
BIN_IMAGE=$(PROJECT_NAME).bin

# Toolchain =============================================================#
CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy

# Compiler Flags ========================================================#
# Detailed arm-none-eabi-gcc compiler documentation can be found at
# https://www.mankier.com/1/arm-none-eabi-gcc

# Pre processor flags: The -D flag defines a compiler macro. This is the same as
# a '#define' statement in as included source file. For example, using
# '-D DEBUG_DISABLE' is the same as having '#define DEBUG_DISABLE' in your
# included source source code. Macros can also be defined with the '-D MY_VALUE=1'
# notation, which is the same as having '#define MY_VALUE=1' in an included source file.
CFLAGS=-D USE_STDPERIPH_DRIVER
CFLAGS+=-D STM32F10X_HD

CFLAGS+=-Wall -g -mlittle-endian -mthumb -nostdlib -ffreestanding
CFLAGS+=-mcpu=cortex-m3
CFLAGS+=-Wl,-T,$(LINKER_SCRIPT)

# Include Files =========================================================#
CFLAGS+=-I./
CFLAGS+=-Iinclude
CFLAGS+=-Icmsis
CFLAGS+=-Istm32-libraries

# Source Files ==========================================================#
#SRC=$(MAIN_SOURCE_FILE)
#SRC+=./system_stm32f10x.c
SRC=source/*.c
SRC+=stm32-libraries/misc.c
SRC+=stm32-libraries/stm32f10x_rcc.c
SRC+=stm32-libraries/stm32f10x_gpio.c

#========================================================================#
#STM32 startup file
STARTUP=./startup_stm32f10x_hd.s

# Make rules ============================================================#
STARTUP_OBJ = startup_stm32f10x_hd.o
#Make all
all: $(BIN_IMAGE)

$(BIN_IMAGE): $(EXECUTABLE)
	$(OBJCOPY) -O binary $^ $@

$(EXECUTABLE): $(SRC) $(STARTUP_OBJ)
	$(CC) $(CFLAGS) $^ -o $@

$(STARTUP_OBJ): $(STARTUP)
	$(CC) $(CFLAGS) $^ -c $(STARTUP)

clean:
	rm -rf *.bin *.elf *.o

flash:
	st-flash write $(BIN_IMAGE) 0x8000000
openocd:
	openocd -f "../commom/openocd.cfg"
gdb:
	arm-none-eabi-gdb -x ../commom/gdb_init.gdb
gdbtui:
	arm-none-eabi-gdb -tui -x ../commom/gdb_init.gdb
#========================================================================#
.PHONY:all clean flash
