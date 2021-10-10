# -*- coding: utf-8 -*-
"""
//Created by Aditya Chandran
"""
import time
import math
from datetime import datetime
import board
import busio
import adafruit_sgp30
import adafruit_bme680
import SI1145.SI1145 as SI1145
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
import adafruit_lis3mdl


i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
lsm6ds33  = LSM6DS33(i2c)
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8AAE)
bme680.sea_level_pressure = 1013.25
si1145 = SI1145.SI1145()
temperature_offset = -5

elapsed_sec = 0
warmedUp = False


while True:
    if not warmedUp:
        print("SGP30 is warming up. Wait 10 seconds.")
        time.sleep(10)
        warmedUp = True
        print("SGP30 is warmed up.")
        print(
            "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x\n"
            % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
        )

    sgp = "%d, %d, " % (sgp30.eCO2, sgp30.TVOC)
    #sgpData =  "SGP30 eCO2 = %d ppm \t SGP30 TVOC = %d ppb \n" % (sgp30.eCO2, sgp30.TVOC)
    sgpTime = str(datetime.now())
    sgpWrite = sgp + sgpTime + '\n'
    with open("sgpLog.csv", "a") as sgpLog:
        sgpLog.write(sgpWrite)
    bme = "%0.1f, %d, %0.1f, %0.3f, %0.2f, " % ((bme680.temperature + temperature_offset), bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude)
    #bmeTemp = "BME688  Temperature: %0.1f C \n" % (bme680.temperature + temperature_offset)
    #bmeGas = "BME688 Gas: %d ohm \n" % (bme680.gas)
    #bmeHum = "BME688 Humidity: %0.1f %% \n" % (bme680.relative_humidity)
    #bmePres = "BME688 Pressure: %0.3f hPa \n" % (bme680.pressure)
    #bmeAlt = "BME688 Altitude = %0.2f meters \n" % (bme680.altitude)
    bmeTime = str(datetime.now())
    bmeWrite = bme + bmeTime + '\n'
    with open("bmeLog.csv", "a") as bmeLog:
        bmeLog.write(bmeWrite)
    si = "%d, %d, %d, " % (si1145.readVisible(), si1145.readIR(), si1145.readUV())
    siTime = str(datetime.now())
    siWrite = si + siTime + '\n'
    with open("siLog.csv", "a") as siLog:
        siLog.write(siWrite)
    accelX, accelY, accelZ = lsm6ds33.acceleration
    accelX = accelX - 4.1
    accelY = accelY - 2.4
    accelZ = accelZ - 8.7
    lsmAccel = "{0:5.2f}, {1:5.2f}, {2:5.2f}, ".format(accelX, accelY, accelZ)
    lsmAWrite = lsmAccel + str(datetime.now()) + '\n'
    lsmGyro = "%.2f, %.2f, %.2f " % (lsm6ds33.gyro)
    lsmGWrite = lsmGyro + str(datetime.now()) + '\n'
    mag_x, mag_y, mag_z = lis3mdl.magnetic
    lis = '{0:10.2f}, {1:10.2f}, {2:10.2f}'.format(mag_x, mag_y, mag_z)
    lisWrite = lis + str(datetime.now()) + '\n'
    with open("lsmAccelLog.csv", "a") as lsmALog:
        lsmALog.write(lsmAWrite)

    with open("lsmGyroLog.csv", "a") as lsmGLog:
        lsmGLog.write(lsmGWrite)

    with open("lisLog.csv", "a") as lisLog:
        lisLog.write(lisWrite)
    #vis = si1145.readVisible()
    #IR = si1145.readIR()
    #UV = si1145.readUV()
    #uvIndex = UV / 100.0
    #writeVis = 'SI1145 Visible Light:             ' + str(vis) + "\n"
    #writeIR = 'SI1145 IR:              ' + str(IR) + '\n'
    #writeUV = 'SI1145 UV Index:        ' + str(uvIndex) + '\n'
    #print(sensTime)
    #write = sgpData + bmeTemp + bmeGas + bmeHum + bmePres + bmeAlt + writeVis + writeIR + writeUV +  writeTime
    #with open("sensor_log.csv", "a") as log:
    #    log.write(write)
    print(sgpWrite, bmeWrite, siWrite, lsmAWrite, lsmGWrite, lisWrite)
    time.sleep(3)