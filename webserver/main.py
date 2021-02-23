#!/usr/bin/python3
#This Program Runs a webserver for users to control the EMS device
from flask import render_template, Flask, send_file, send_from_directory, request, url_for, redirect
from sensor import sensor
from downloads import downloads

ip='0.0.0.0'

app = Flask(__name__)
#Links py files with corresponding routes
app.register_blueprint(sensor, url_prefix="/sensorread")
app.register_blueprint(downloads, url_prefix="/downloads")

#When routed to homepage
@app.route('/')
def index():
    return render_template('index.html')


#Run Webserver Via Flask library
if __name__ == '__main__':
    app.run(debug=True, host=ip, port=8080)

