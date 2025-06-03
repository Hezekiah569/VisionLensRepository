import RPi.GPIO as GPIO
import time
import threading

# Shared flag to stop the vibration loop from other threads
stop_vibration = threading.Event()

# Sensor 1 GPIOs (Left)
TRIG_1 = 4
ECHO_1 = 18
MOTOR_1 = 12

# Sensor 2 GPIOs (Right)
TRIG_2 = 27
ECHO_2 = 24
MOTOR_2 = 19

# Sensor 3 GPIOs (Back)
TRIG_3 = 17
ECHO_3 = 23
MOTOR_3 = 13

THRESHOLD_DISTANCE = 50  # cm
MAX_DISTANCE_CM = 400
VIBRATION_MAX = 100
VIBRATION_MIN = 10
MEASUREMENT_INTERVAL = 0.1  # seconds

def measure_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    timeout = start_time + 0.1
    while GPIO.input(echo) == 0:
        start_time = time.time()
        if start_time > timeout:
            return MAX_DISTANCE_CM
    stop_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()
        if stop_time > timeout:
            return MAX_DISTANCE_CM

    pulse_duration = stop_time - start_time
    distance = pulse_duration * 17150
    return min(round(distance, 2), MAX_DISTANCE_CM)

def calculate_vibration_intensity(distance):
    if distance >= THRESHOLD_DISTANCE:
        return 0
    intensity = VIBRATION_MAX - ((VIBRATION_MAX - VIBRATION_MIN) * distance / THRESHOLD_DISTANCE)
    return int(max(min(intensity, VIBRATION_MAX), 0))

def start_vibration_feedback():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup GPIO for all sensors
    GPIO.setup(TRIG_1, GPIO.OUT)
    GPIO.setup(ECHO_1, GPIO.IN)
    GPIO.output(TRIG_1, False)
    GPIO.setup(MOTOR_1, GPIO.OUT)
    pwm1 = GPIO.PWM(MOTOR_1, 100)
    pwm1.start(0)

    GPIO.setup(TRIG_2, GPIO.OUT)
    GPIO.setup(ECHO_2, GPIO.IN)
    GPIO.output(TRIG_2, False)
    GPIO.setup(MOTOR_2, GPIO.OUT)
    pwm2 = GPIO.PWM(MOTOR_2, 100)
    pwm2.start(0)

    GPIO.setup(TRIG_3, GPIO.OUT)
    GPIO.setup(ECHO_3, GPIO.IN)
    GPIO.output(TRIG_3, False)
    GPIO.setup(MOTOR_3, GPIO.OUT)
    pwm3 = GPIO.PWM(MOTOR_3, 100)
    pwm3.start(0)

    try:
        print("Vibration feedback started...")
        while not stop_vibration.is_set():
            dist1 = measure_distance(TRIG_1, ECHO_1)
            pwm1.ChangeDutyCycle(calculate_vibration_intensity(dist1))

            dist2 = measure_distance(TRIG_2, ECHO_2)
            pwm2.ChangeDutyCycle(calculate_vibration_intensity(dist2))

            dist3 = measure_distance(TRIG_3, ECHO_3)
            pwm3.ChangeDutyCycle(calculate_vibration_intensity(dist3))

            time.sleep(MEASUREMENT_INTERVAL)

    except Exception as e:
        print(f"Vibration error: {e}")
    finally:
        pwm1.stop()
        pwm2.stop()
        pwm3.stop()
        GPIO.cleanup()
        print("Vibration feedback stopped and GPIO cleaned.")