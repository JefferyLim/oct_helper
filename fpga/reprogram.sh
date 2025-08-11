config-fpga reset ~/private_key.pem
echo Y | sudo xbflash2 program --spi --image ~/fpga.mcs -d 3b:00.0 --bar 2
config-fpga boot ~/private_key.pem
