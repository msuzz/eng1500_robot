"""
All of our prototype robot's utility functions are included in here
This way, the main.py file can stay clean and be modified easily.
"""

from time import sleep

def line_distance_mm(adc1, adc2, adc3, adc4):
    """
    Ultrasonic sensor reading function that averages the result of the
    past numReadings. Returns distance in mm of object in front of
    ultrasonic sensor.
    :param adc1: ADC input for the left-most (from head-on) line sensor
    :param adc2: ADC input for the centre-left (from head-on) line sensor
    :param adc3: ADC input for the centre-right (from head-on) line sensor
    :param adc4: ADC input for the right-most (from head-on) line sensor
    :return: Distance in mm of object in front of ultrasonic sensor
    """
    # These values contain the offset of the line sensors relative to the centre of the vehicle.
    x1 = -21
    x2 = -7
    x3 = 7
    x4 = 21

    # Read our sensor data
    w1 = adc1.read()
    w2 = adc2.read()
    w3 = adc3.read()
    w4 = adc4.read()

    num = w1*x1 + w2*x2 + w3*x3 + w4*x4
    denom = w1 + w2 + w3 + w4

    # line_dist contains the offset of the line relative to the centre of the vehicle
    dist_mm = num/denom
    #dist_mm = (w1*x1)/denom + (w2*x2)/denom + (w3*x3)/denom + (w4*x4)/denom

    return dist_mm


# Globals for ultrasonic_read()
ultraRunOnce = 0
ultraReadArray = []
ultraReadIndex = 0
ultraReadTotal = 0

def ultrasonic_read(ultraSens, numReadings):
    """
    Ultrasonic sensor reading function that averages the result of the
    past numReadings. Returns distance in mm of object in front of
    ultrasonic sensor.
    :param ultraSens: Ultrasonic sensor object from ultrasonic.py
    :param numReadings: Number of readings to take and average
    :return: Distance in mm of object in front of ultrasonic sensor
    """
    global ultraRunOnce
    global ultraReadArray
    global ultraReadIndex
    global ultraReadTotal

    if ultraRunOnce == 0:
        ultraReadArray = [0]*numReadings
        ultraRunOnce = 1

    ultraReadTotal -= ultraReadArray[ultraReadIndex]
    ultraReadArray[ultraReadIndex] = ultraSens.distance_mm()
    ultraReadTotal += ultraReadArray[ultraReadIndex]
    ultraReadIndex += 1

    if ultraReadIndex >= numReadings:
        ultraReadIndex = 0

    readAvg = ultraReadTotal / numReadings
    sleep(0.1)

    return readAvg


# Globals for proximity_read()
proxRunOnce = 0
proxReadArray = []
proxReadIndex = 0
proxReadTotal = 0

def proximity_read(apds9960, numReadings):
    """
    Averages the result of past numReadings.
    :param apds9960: APDS9960 object from APDS9960LITE.py
    :param numReadings: Number of readings to take and average
    :return: Averaged APDS9960 proximity sensor reading.
    """

    global proxRunOnce
    global proxReadArray
    global proxReadIndex
    global proxReadTotal

    if proxRunOnce == 0:
        proxReadArray = [0]*numReadings
        proxRunOnce = 1

    proxReadTotal -= proxReadArray[proxReadIndex]
    proxReadArray[proxReadIndex] = apds9960.prox.proximityLevel
    proxReadTotal += proxReadArray[proxReadIndex]
    proxReadIndex += 1

    if proxReadIndex >= numReadings:
        proxReadIndex = 0

    readAvg = proxReadTotal / numReadings

    return readAvg


def motor_calibration(motor_left, motor_right, enc):
    """
    This function generates lines of CSV in the REPL output representing the:
        Current PWM value
        Encoder count for left wheel
        Encoder count for right wheel
    In three respective columns. This should be copy-pasted into a file and
    parsed with the motor_calibration_plot() function.
    :param motor_left: Motor object from motor.py, corresponding to left wheel
    :param motor_right: Motor object from motor.py, corresponding to right wheel
    :param enc: Encoder object from encode.py
    """
    print("PWM, ENC_L, ENC_R")
    for testPWM in range(0, 101, 5):  # Loop from 0-100% increasing by 5%
        enc.clear_count()
        # Drive forwards for 1 second at specified pwm
        motor_left.ctrl_alloc(1, testPWM)
        motor_right.ctrl_alloc(1, testPWM)
        sleep(1)

        # Wait for 1 second, print encoder counts in CSV format
        motor_left.ctrl_alloc(1, 0)
        motor_right.ctrl_alloc(1, 0)
        left_count = enc.get_left()
        right_count = enc.get_right()
        print("{:3d}, {:4d}, {:4d}".format(testPWM, left_count, right_count))
        sleep(1)
    print("Measurements generated! Paste the above inside motor_csv.txt")


def apds9960_distance_calibration(apds9960, ultra):
    """
    Generates lines of CSV in the REPL output representing the:
        Proximity of the APDS9960 RGB Sensor, and
        Proximity of the ultrasonic sensor in mm
    In two respective columns. This should be copy-pasted into a file
    :param apds9960: APDS9960 sensor object from APDS9960LITE.py
    :param ultra: Ultrasonic object from ultrasonic.py
    """
    for i in range(100):  # Take 100 measurements
        proximity_measurement = apds9960.prox.proximityLevel  # Read the proximity
        ultrasonic_measurement_mm = ultrasonic_read(ultra, 10)
        print("{:3d}, {:4.2f}".format(proximity_measurement, ultrasonic_measurement_mm))
        sleep(0.2)  # Wait for measurement to be ready
    print("Measurements generated! Paste the above inside rgb_csv.txt")
