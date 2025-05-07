import network
import socket
from machine import Pin, PWM, time_pulse_us, Timer
import time

# Wi-Fi Configuration
SSID = "Baslem_Robot"
PASSWORD = "12345678"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD)

while not ap.active():
    pass
print("Wi-Fi AP Active")
print("IP Address:", ap.ifconfig()[0])

# Pins
TRIGGER = 26
ECHO = 27
ENA = 23
ENB = 15
IN1, IN2 = 22, 21
IN3, IN4 = 18, 4

speed = 300
stop_distance = 25
manual_command = "stop"
distance=99
ena = PWM(Pin(ENA), freq=1000)
enb = PWM(Pin(ENB), freq=1000)
in1 = Pin(IN1, Pin.OUT)
in2 = Pin(IN2, Pin.OUT)
in3 = Pin(IN3, Pin.OUT)
in4 = Pin(IN4, Pin.OUT)

trigger = Pin(TRIGGER, Pin.OUT)
echo = Pin(ECHO, Pin.IN)


def stop_motors():
    ena.duty(0)
    enb.duty(0)
    in1.off()
    in2.off()
    in3.off()
    in4.off()


def move_forward():
    ena.duty(speed)
    enb.duty(speed)
    in1.on()
    in2.off()
    in3.off()
    in4.on()


def turn_left():
    ena.duty(speed)
    enb.duty(speed)
    in1.on()
    in2.off()
    in3.on()
    in4.off()


def turn_right():
    ena.duty(speed)
    enb.duty(speed)
    in1.off()
    in2.on()
    in3.off()
    in4.on()


def move_back():
    ena.duty(speed)
    enb.duty(speed)
    in1.off()
    in2.on()
    in3.on()
    in4.off()


def get_distance():
    trigger.on()
    time.sleep_us(10)
    trigger.off()
    duration = time_pulse_us(echo, 1)
    return (duration * 0.0343) / 2


def robot_logic(timer):
    global manual_command,distance

    if manual_command == "stop":
        stop_motors()
        return
    if distance < stop_distance:
        print("moving back")
        move_back() 
        return
    if manual_command == "forward":
        move_forward()
    elif manual_command == "left":
        turn_left()
    elif manual_command == "right":
        turn_right()
    elif manual_command == "back":
        move_back()
    else:
        stop_motors()


timer = Timer(2)
timer.init(period=100, mode=Timer.PERIODIC, callback=robot_logic)

webpage = """<!DOCTYPE html>
<html>
<head>
<title>ESP32 Robot</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { text-align: center; font-family: Arial; margin-top: 40px; user-select: none; }
button { padding: 20px; margin: 10px; font-size: 20px; border-radius: 10px; background: #4CAF50; color: white; }
button:active { background: #45a049; }
.stop { background: red; }
h3 { font-size: 20px; margin-bottom: 10px; }
.slider-container { display: flex; justify-content: center; align-items: center; }
.slider { width: 60%; }
.slider-value { margin-left: 20px; font-size: 18px; }
</style>
<script>
let cmdInterval;

function sendCommand(cmd) {
    fetch("/command?value=" + cmd);
}

function startCommand(cmd) {
    sendCommand(cmd);
    cmdInterval = setInterval(() => {
        sendCommand(cmd);
    }, 100);
}

function stopCommand() {
    clearInterval(cmdInterval);
    sendCommand("stop");
}

function updateSpeed() {
    let speed = document.getElementById("speed").value;
    document.getElementById("speed-value").innerText = speed;
    fetch("/speed?value=" + speed);
}

function updateDistance() {
    let distance = document.getElementById("distance").value;
    document.getElementById("distance-value").innerText = distance;
    fetch("/distance?value=" + distance);
}

window.onload = () => {
    ["forward", "left", "right", "back"].forEach(cmd => {
        let btn = document.getElementById(cmd);
        btn.addEventListener("pointerdown", () => startCommand(cmd));
        btn.addEventListener("pointerup", stopCommand);
        btn.addEventListener("pointercancel", stopCommand);
        btn.addEventListener("touchend", stopCommand);
    });
};
</script>
</head>
<body>
<h1>ESP32 Robot Control</h1>

<div class="slider-container">
    <h3>Speed:</h3>
    <input type="range" id="speed" min="100" max="1023" value="300" class="slider" oninput="updateSpeed()">
    <span id="speed-value" class="slider-value">300</span>
</div>

<div class="slider-container">
    <h3>Stop Distance:</h3>
    <input type="range" id="distance" min="5" max="50" value="25" class="slider" oninput="updateDistance()">
    <span id="distance-value" class="slider-value">25</span>
</div>

<button id="forward">Forward</button><br>
<button id="left">Left</button>
<button id="right">Right</button><br>
<button id="back">Back</button><br>
<button class="stop" onclick="sendCommand('stop')">STOP</button>

</body>
</html>

"""

s = socket.socket()
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    distance = get_distance()
    print("manual commande :",manual_command)
    print("distance :",distance)
    if "/command?value=" in request:
        manual_command = request.split("/command?value=")[1].split(" ")[0]

    if "/speed?value=" in request:
        speed = int(request.split("/speed?value=")[1].split(" ")[0])

    if "/distance?value=" in request:
        stop_distance = int(request.split("/distance?value=")[1].split(" ")[0])

    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    conn.send(webpage)
    conn.close()
    time.sleep(0.01)

