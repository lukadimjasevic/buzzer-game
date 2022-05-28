import RPi.GPIO as GPIO

a = 4
b = 17
c = 22
d = 27
e = 18
f = 23
g = 24

numbers = {
           0: [a, b, c, d, e, f],
           1: [b, c],
           2: [a, b, g, e, d],
           3: [a, b, g, c, d],
           4: [f, g, b, c],
           5: [a, f, g, c, d],
           6: [a, f, e, d, c, g],
           7: [a, b, c],
           8: [a, b, c, d, e, f, g],
           9: [g, f, a, b, c, d]
}


def initialize(buzzer, greenLed, redLed):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(greenLed, GPIO.OUT)
    GPIO.setup(redLed, GPIO.OUT)
    GPIO.setup(a, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    GPIO.setup(c, GPIO.OUT)
    GPIO.setup(d, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    GPIO.setup(f, GPIO.OUT)
    GPIO.setup(g, GPIO.OUT)

    reset_items(buzzer, redLed, greenLed)


def light_on_num(num):
    for i in range(len(numbers[num])):
        GPIO.output(numbers[num][i], GPIO.HIGH)


def light_off_num(num):
    for i in range(len(numbers[num])):
        GPIO.output(numbers[num][i], GPIO.LOW)


def reset_items(buzzer, redLed, greenLed):
    GPIO.output(buzzer, GPIO.LOW)
    GPIO.output(redLed, GPIO.LOW)
    GPIO.output(greenLed, GPIO.LOW)
    for k in range(10):
        light_off_num(k)