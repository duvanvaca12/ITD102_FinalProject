from flask import Flask, jsonify, render_template, request, Response, stream_with_context, json
import redis
import RPi.GPIO as gpio
import time
from ipget import run_ipscript

time.sleep(30)
run_ipscript()

app = Flask(__name__)
red = redis.StrictRedis()

# Give the GPIO pins a variable

motor1_A = 17
motor1_B = 22
motor2_A = 23
motor2_B = 24
motor1_ENA = 4
motor2_ENB = 27

# Setup all the GPIO pins

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(motor1_ENA, gpio.OUT)
gpio.setup(motor2_ENB, gpio.OUT)
gpio.setup(motor1_A, gpio.OUT)
gpio.setup(motor1_B, gpio.OUT)
gpio.setup(motor2_A, gpio.OUT)
gpio.setup(motor2_B, gpio.OUT)

# Set up the PWM for the motors
pwm1 = gpio.PWM(motor1_ENA,100)
pwm1.start(0)
pwm2 = gpio.PWM(motor2_ENB,100)
pwm2.start(0)

speed_motor = 0

def event_stream():
    def info_motor():
        redes = str(speed_motor)
        yield 'data: ' + json.dumps(redes) + '\n\n'
    return stream_with_context(info_motor())


@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/stream', methods=['GET','POST']) 
def stream():
    return Response(event_stream(),
        mimetype="text/event-stream")
    # Cpmentass

@app.route('/Forward')
def Forward():
    gpio.output(motor1_A, True)
    gpio.output(motor1_B, False)
    gpio.output(motor2_A, False)
    gpio.output(motor2_B, True)
    return "Nothing"

@app.route('/Stop')
def Stop():
    gpio.output(motor1_A, False)
    gpio.output(motor1_B, False)
    gpio.output(motor2_A, False)
    gpio.output(motor2_B, False)
    return "Nothing"

@app.route('/Reverse')
def Reverse():
    gpio.output(motor1_A, False)
    gpio.output(motor1_B, True)
    gpio.output(motor2_A, True)
    gpio.output(motor2_B, False)
    return "Nothing"

@app.route('/Left')
def Left():
    gpio.output(motor1_A, False)
    gpio.output(motor1_B, False)
    gpio.output(motor2_A, False)
    gpio.output(motor2_B, True)
    
    return "Nothing"

@app.route('/Right')
def Right():
    gpio.output(motor1_A, True)
    gpio.output(motor1_B, False)
    gpio.output(motor2_A, False)
    gpio.output(motor2_B, False)
    return "Nothing"

@app.route('/Increase')
def Increase():
    global speed_motor
    if speed_motor < 100.0:
        speed_motor+=20
    else:
        pass
    pwm1.ChangeDutyCycle(speed_motor)
    pwm2.ChangeDutyCycle(speed_motor)
    user = speed_motor
    return "Nothing"


@app.route('/Decrease')
def Decrease():
    global speed_motor
    if speed_motor > 0:
        speed_motor-=20
    else:
        pass
    pwm1.ChangeDutyCycle(speed_motor)
    pwm2.ChangeDutyCycle(speed_motor)
    user = speed_motor
    return "Nothing"



if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0")