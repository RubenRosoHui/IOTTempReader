#!/usr/bin/python3
#This python file is used to run the following code when navigating [ip]/sensorread route
from flask import render_template, Flask, send_file, send_from_directory, request, url_for, redirect, Blueprint, jsonify
import Adafruit_DHT
from sensorDisplay import sensorRun, Clear_Oled, get_sensorRead, stateOff, stateOn, getState, toggleState
from threading import Thread

#Targets pin to get sensor data
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#Create thread object
t = Thread(target=sensorRun)

#Links to main.py
sensor = Blueprint("sensor", __name__, template_folder="templates")

#When routed to Sensordisplay Page
@sensor.route('/')
def sensorP():
    humidity,temperature = get_sensorRead()
    state = getState()
    return render_template('sensordata.html', Temp=temperature, Humidity=humidity, State=state)

#Starts or return state to on
@sensor.route('/On')
def turnOn():
    if t.is_alive() != True:
        t.start()
        toggleState()   
    stateOn()
    return redirect(url_for('sensor.sensorP'))

#Turn off State of Sensor
@sensor.route('/Off')
def turnOff():
    stateOff()
    Clear_Oled()
    return redirect(url_for('sensor.sensorP'))

@sensor.route('/test')
def testPage():
    return render_template('Test.html')

#Return humidity and temperature for javascript refresh
@sensor.route('/data')
def process():
    humidity,temperature = get_sensorRead()
    return jsonify(hum=humidity, temp=temperature)
        