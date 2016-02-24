/*  █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗
 * ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝
 * ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝
 * ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝
 * ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
 * ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝
 *                               by Pax Instruments
 */


MEMORY {
    FLASH (rx) : ORIGIN = FLASH_ORIGIN, LENGTH = FLASH_LENGTH
    RAM (xrw)  : ORIGIN = RAM_ORIGIN, LENGTH = RAM_LENGTH
}

/***************/
/*   Memory    */
/***************/
#if defined STM32F100xB
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 128K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 8K
 }
#elif defined STM32F100xE
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 32K
 }
#elif defined STM32F101x6
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 32K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 6K
 }
#elif defined STM32F101xB
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 128K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 16K
 }
#elif defined STM32F101xE
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 48K
 }
#elif defined STM32F101xG
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 1000K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 80K
 }
#elif defined STM32F102x6
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 32K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 6K
 }
#elif defined STM32F102xB
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 128K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 16K
 }
#elif defined STM32F103x6
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 32K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 10K
 }
#elif defined STM32F103xB
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 128K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 20K
 }
#elif defined STM32F103xE
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 64K
 }
#elif defined STM32F103xG
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 1000K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 96K
 }
#elif defined STM32F105xC
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 256K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 64K
 }
#elif defined STM32F107xC
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 256K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 64K
 }
 #elif defined STM32F401xC
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 256K
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 64K
  }
 #elif defined STM32F401xE
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 96K
  }
 #elif defined STM32F405xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F407xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F410Tx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F410Cx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F410Rx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F411xE
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F415xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F417xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F427xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F429xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F437xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F439xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F446xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F469xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
 #elif defined STM32F479xx
  MEMORY {
     FLASH (rx) : ORIGIN = 0x08000000, LENGTH =
     RAM (xrw)  : ORIGIN = 0x20000000, LENGTH =
  }
#else
/* Using the smallest values */
 MEMORY {
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 32K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 6K
 }
 #endif



ENTRY(Reset_Handler) /* Entry point of the reset handler */
_estack = ORIGIN(RAM) + LENGTH(RAM);

/***************/
/*  Sections   */
/***************/
SECTIONS {
    .text : {
        KEEP(*(.isr_vector))
        *(.text*)
        KEEP (*(.init))
        KEEP (*(.fini))
        _etext = .;
    } > FLASH

    .rodata : {
        . = ALIGN(4);
        *(.rodata)
        *(.rodata*)
        . = ALIGN(4);
    } >FLASH

    .ARM.extab : {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > FLASH

    .ARM : {
        __exidx_start = .;
        *(.ARM.exidx*)
        __exidx_end = .;
    } > FLASH

    .preinit_array : {
        PROVIDE_HIDDEN (__preinit_array_start = .);
        KEEP (*(.preinit_array*))
        PROVIDE_HIDDEN (__preinit_array_end = .);
    } > FLASH

    .init_array : {
        PROVIDE_HIDDEN (__init_array_start = .);
        KEEP (*(SORT(.init_array.*)))
        KEEP (*(.init_array*))
        PROVIDE_HIDDEN (__init_array_end = .);
    } > FLASH

    .fini_array : {
        PROVIDE_HIDDEN (__fini_array_start = .);
        KEEP (*(SORT(.fini_array.*)))
        KEEP (*(.fini_array*))
        PROVIDE_HIDDEN (__fini_array_end = .);
    } > FLASH

    _sidata = LOADADDR(.data);

    .data : {
        . = ALIGN(4);
        _sdata = .;
        *(.data)
        *(.data*)

        . = ALIGN(4);
        _edata = .;
    } > RAM AT > FLASH

    . = ALIGN(4);

    .bss : {
        /* This is used by the startup in order to initialize the .bss secion */
        _sbss = .;         /* define a global symbol at bss start */
        __bss_start__ = _sbss;
        *(.bss)
        *(.bss*)
        *(COMMON)

        . = ALIGN(4);
        _ebss = .;         /* define a global symbol at bss end */
        __bss_end__ = _ebss;
    } > RAM

    /DISCARD/ : {
        libc.a ( * )
        libm.a ( * )
        libgcc.a ( * )
    }

    .ARM.attributes 0 : { *(.ARM.attributes) }
}
