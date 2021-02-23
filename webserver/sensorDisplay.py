#!/usr/bin/python3
#This file is the main file to get and display temperature and humidity on Oled.
#imports
from board import SCL, SDA
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import sys
import Adafruit_DHT
import time
import os.path

#Initial Program States
program = False
run = False

#Functions
#Clears Oled Screen/Exits
def Clear_Oled():
    oled.fill(0)
    oled.show()

#Welcome screen when program starts running
def Splash_screen():
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=255)
    draw.text((45,24), "WELCOME", font=font, fill=0)
    oled.image(image)
    oled.show()
    time.sleep(3)

#Recieves and return Temp/Humdity Data
def get_sensorRead():
    return Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

#Turns sensor on for while loop to go through
def stateOn():
    global run
    if run == False:
        run = True

#Turns sensor off for while loop to go through
def stateOff():
    global run
    if run == True:
        run = False

#Turn On or Off Thread from server
def toggleState():
    global program
    program = not program

#Return state of Sensor for server
def getState():
    global run
    if run:
        return True
    if (not run):
        return False

#Write file to downloads/SensorReading.txt
def writeFile(humidity, temperature):
    if os.path.isfile('downloads/SensorReading.txt'):
        f = open('downloads/SensorReading.txt', 'a+')
        #f.write('Date,Time,Temperature,Humidity\r\n')
            #only execute if values of both humidity and temperature are initalized 
        if humidity is not None and temperature is not None:
            f.write('{0},{1},{2:0.1f}*C,{3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), temperature, humidity))
    #execute if the temperature and humidity is able to be initalized
        else:
            f.write("ERROR!!! Failed to retrieve data from sensor")
    else:
        f = open('downloads/SensorReading.txt', 'a+')
        f.write('Date,Time,Temperature,Humidity\r\n')
    f.close()

#Sensor display on oled and write file
def sensorRun():
    try:
        global program
        global run
        Splash_screen()
        while program:
            
            while run:
                draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
                draw.text((24,0), "Environmental", font=font, fill=255, align="center")
                draw.text((16,8), "Monitoring System", font=font, fill=255, align="center")

                humidity,temperature = get_sensorRead()
                writeFile(humidity, temperature)
                if humidity is not None and temperature is not None:
                    draw.text((0, 24), "Temp:{0:0.1f}°C".format(temperature), font=font, fill=255)
                    draw.text((0, 36), "Humidity:{0:0.1f}%".format(humidity), font=font, fill=255)
                else:
                    draw.text((0, 24), "Temp:!°C", font=font, fill=255)
                    draw.text((0, 36), "Humidity:!%", font=font, fill=255)

                oled.image(image)
                oled.show()
                time.sleep(5)
            #continue
            Clear_Oled()
    except KeyboardInterrupt:
        Clear_Oled()
        print("Program has Stopped")

#Sensor Data
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#Dimentions(dont change)
WIDTH = 128
HEIGHT = 64
i2c = busio.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

#clear Display
oled.fill(0)
oled.show()
font = ImageFont.load_default()

#Creating image
image = Image.new("1", (oled.width, oled.height))
#Get drawing object to draw
draw = ImageDraw.Draw(image)

if __name__=='__main__':
    sensorRun()