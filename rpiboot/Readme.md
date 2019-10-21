# USB boot code

This is the USB MSD boot code which should work on the Avnet SmartEdge IIOT Gateway.

This version of rpiboot is a snapshot of the mainline rpiboot (commit: 50fc0f4).  Newer versions of rpiboot
may not work properly on the Avnet SmartEdge IIOT Gateway.

## Building

Clone this on your Pi or an Ubuntu linux machine

```
$ git clone https://github.com/Avnet/smartedge-iiot-gateway-custom.git
$ cd smartedge-iiot-gateway-custom/rpiboot
$ sudo apt-get install libusb-1.0-0-dev
$ make
$ sudo ./rpiboot_secure.sh
```

rpiboot may hang, but you can safely CTRL-C out once the drive is visible.

## Running your own (not MSD) build

If you would like to boot the Gateway with a standard build you just need to copy the FAT partition
files into a subdirectory (it must have at the minimum bootcode.bin and start.elf).  If you take a
standard firmware release then this will at the very least boot the linux kernel which will then stop
(and possibly crash!) when it looks for a filesystem.  To provide a filesystem there are many options,
you can build an initramfs into the kernel, add an initramfs to the boot directory or provide some
other interface to the filesystem.

```
$ sudo ./rpiboot -d boot
```

This will serve the boot directory to the Avnet SmartEdge IIOT Gateway Device.
