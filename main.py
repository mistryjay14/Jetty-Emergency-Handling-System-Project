import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import requests

#defining flask object
app = Flask(__name__)

#defining GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#defining input jetty ESD 
button1 = 20      

#defining outputs GPIOs
alarm = 13
siren = 19
relay = 26	

#initializing GPIO status variables 
button1_store = 0
alarm_store = 0
siren_store = 0
relay_store = 0
   
#Set input button jetty ESD as input
GPIO.setup(button1, GPIO.IN)   
	
#Set outputs
GPIO.setup(alarm, GPIO.OUT)
GPIO.setup(siren, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)

#turning off the output initially
GPIO.output(alarm, GPIO.LOW)
GPIO.output(siren, GPIO.LOW)
GPIO.output(relay, GPIO.LOW)


@app.route("/")
def index():
	# Reading status of inputs and outputs and storing them
	button1_store = GPIO.input(button1)
	alarm_store = GPIO.input(alarm)
	siren_store = GPIO.input(siren)
	relay_store = GPIO.input(relay)

	if GPIO.input(button1) == 1:
		GPIO.output(alarm, GPIO.HIGH)
		GPIO.output(siren, GPIO.HIGH)
		#sms module for jetty side ESD
		url = "https://www.fast2sms.com/dev/bulk"
		my_data = {
			'sender_id': 'TXTIND',
			'message': 'Jetty ESD activated.',
			'language': 'english',
			'route': 'p',
			'numbers': '9999999999' #for multiple nos. separate the nos. by comma and no space in between	
		}
		headers = {
			'authorization': 'API key',
			'Content-Type': "application/x-www-form-urlencoded",
			'Cache-Control': "no-cache"
		}
		response = requests.request("POST", url, data=my_data, headers=headers)
		print(response.text)
		#end of sms module

	elif GPIO.input(button1) == 0:
		GPIO.output(alarm, GPIO.LOW)
		GPIO.output(siren, GPIO.LOW)


	templateData = {
      'button1'  : button1_store,
      'alarm'    : alarm_store,
      'siren'	  : siren_store,
      'relay'    : relay_store,	
      }
	return render_template('index.html', **templateData)


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	
	if action == "on":
		GPIO.output(alarm, GPIO.HIGH)
		GPIO.output(siren, GPIO.HIGH)
		GPIO.output(relay, GPIO.HIGH)
		#sending SMS
		url = "https://www.fast2sms.com/dev/bulk"
		my_data = {
			'sender_id': 'TXTIND',
			'message': 'Terminal ESD activated.',
			'language': 'english',
			'route': 'p',
			'numbers': '9999999999' #for multiple nos. separate the nos. by comma and no space in between		
		}
		headers = {
			'authorization': 'API key',
			'Content-Type': "application/x-www-form-urlencoded",
			'Cache-Control': "no-cache"
		}
		response = requests.request("POST", url, data=my_data, headers=headers)
		print(response.text)
		#end of sms module

		#mail module 	
	elif action == "off":
		GPIO.output(alarm, GPIO.LOW)
		GPIO.output(siren, GPIO.LOW)
		GPIO.output(relay, GPIO.LOW)

#again reading the status and storing it
	button1_store = GPIO.input(button1)
	alarm_store = GPIO.input(alarm)
	siren_store = GPIO.input(siren)
	relay_store = GPIO.input(relay)

	templateData = {
			'button1' : button1_store,
			'alarm'   : alarm_store,
			'siren'   : siren_store,
			'relay'   : relay_store,
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)


