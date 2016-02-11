# User Configuration ====================================================#
PROJECT_NAME=gpio_example
MAIN_SOURCE_FILE=main.c
LINKER_SCRIPT=libraries/mbed/libraries/mbed/targets/cmsis/TARGET_STM/TARGET_STM32F1/TARGET_NUCLEO_F103RB/TOOLCHAIN_GCC_ARM/STM32F103XB.ld
#LINKER_SCRIPT=stm32_flash.ld

# Output files ==========================================================#
EXECUTABLE=$(PROJECT_NAME).elf
BIN_IMAGE=$(PROJECT_NAME).bin

# Toolchain =============================================================#
CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy

# Compiler Flags ========================================================#
CFLAGS=-Wall -g -mlittle-endian -mthumb -nostdlib -ffreestanding
CFLAGS+=-mcpu=cortex-m3
CFLAGS+=-D USE_STDPERIPH_DRIVER
CFLAGS+=-D STM32F10X_HD
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
