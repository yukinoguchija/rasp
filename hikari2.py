# coding: utf-8
import spidev
import time
 
#Define Variables
delay = 2
ldr_channel = 0
 
#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
 
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data
 
 
while True:
    ldr_value = readadc(ldr_channel)
    print("LDR Value: %d" % ldr_value)
    ldr_value1 = readadc(1)
    print("LDR2 Value: %d" %  ldr_value1)
time.sleep(delay)

