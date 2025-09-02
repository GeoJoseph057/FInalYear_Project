from gpiozero import AngularServo
from time import sleep
import paho.mqtt.client as mqtt
import threading
import cv2

servos = [
    AngularServo(17, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
    AngularServo(18, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
    AngularServo(27, min_angle=180, max_angle=0, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
    AngularServo(22, min_angle=180, max_angle=0, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000),
    AngularServo(23, min_angle=0, max_angle=180, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)
]

# Set servo positions
def set_servo_positions(sequence):
    for i, char in enumerate(sequence):
        angle = 180 if char == '1' else 0
        servos[i].angle = angle
    print(f"Servos set to: {sequence}")

# MQTT setup
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic = "esp8266/fsr_sensor"
state = "open"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(mqtt_topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    global state

    message = msg.payload.decode()
    print(f"MQTT Message: {message}")

    if message == "1" and state == "open":
        print("FSR HIGH -> Closing arm (00000) for 3 seconds")
        set_servo_positions("00000")
        state = "closed"
        sleep(3)

    elif message == "0" and state == "closed":
        print("FSR LOW -> Opening arm (11111)")
        set_servo_positions("11111")
        state = "open"

# Camera capture function
def capture_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera.")
        return

    print("Camera started. Press 'q' to quit video preview.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow('Video Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start camera in background thread
camera_thread = threading.Thread(target=capture_video)
camera_thread.start()

# Start MQTT loop
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

# Initial arm position
print("Initializing: Arm open (11111)")
set_servo_positions("11111")

try:
    client.loop_forever()

except KeyboardInterrupt:
    print("Program stopped by user")
    client.disconnect()

