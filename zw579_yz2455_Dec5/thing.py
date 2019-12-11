import threading

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import sqlite3
import sys
import os
import subprocess

LED_PIN = 23
SWITCH_PIN = 19
TRIG = 16
ECHO = 26
signal = -1

class global_var:
    signal = -1
def set_name(signal):
    global_var.signal = -1
def get_name():
    return global_var.signal

class PiThing(object):
    """Internet 'thing' that can control GPIO on a Raspberry Pi."""

    def __init__(self):
        """Initialize the 'thing'."""
        # Setup GPIO library.
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Setup LED as an output and switch as an input.
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(SWITCH_PIN, GPIO.IN)

        # Setup Echo and Trigger
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.output(TRIG, 0)
        GPIO.setup(ECHO, GPIO.IN)

        # Create a lock to syncronize access to hardware from multiple threads.
        self._lock = threading.Lock()

        # Setup a thread to read the DHT sensor every 2 seconds and store
        self._humidity = None
        self._temperature = -2
        self.id = 0
        self.sent = False
        # self._dht_thread = threading.Thread(target=self._update_dht)
        # self._dht_thread.daemon = True  # Don't let this thread block exiting.
        # self._dht_thread.start()

        conn = sqlite3.connect('echo.db')
        c = conn.cursor()
        c.execute('DELETE FROM readings')
        conn.commit()
        conn.close()

    def read_switch(self):
        """Read the switch state and return its current value.
        """
        with self._lock:
            return GPIO.input(SWITCH_PIN)

    def set_led(self, value):
        """Set the LED to the provided value (True = on, False = off).
        """
        with self._lock:
            GPIO.output(LED_PIN, value)

    def read_echo(self):
        """Read the echo state and return its current value.
        """
        # with self._lock:
            # # Trigger signal
        # global signal
        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)
        while GPIO.input(ECHO) == 0:
            pass
        start = time.time()

        while GPIO.input(ECHO) == 1:
            pass
        stop = time.time()
        # print(stop-start)
        # print("intert finish")
        #self._humidity, self._temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 5)
        #print(self._temperature)
        # self.get_temperature()
        #sound = 331.3 + 0.606 * self._temperature
        sound = 331.3 + 0.606 * self._temperature
        distance =0.521 - ((stop-start)*sound/2)
        print('distance is:', distance)
        if distance > 0.3 and not self.sent:
            print("send FIFO")
            cmd = 'echo sendEmail > /home/pi/Documents/rpiWebServer/test_fifo'
            print(subprocess.check_output(cmd, shell=True))
            self.sent = True

        # else: signal = -1
        
        #     # execfile('send2.py')

        #     os.system("python ./send3.py")
           
        self.insertDB('RCWL1601', distance)

        return distance

    # def _update_dht(self):
    #         """Main function for DHT update thread, will grab new temp & humidity
    #         values every two seconds.
    #         """
    #     # Read the humidity and temperature from the DHT sensor.
    #     # self._humidity, self._temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 5)
    #     # print(self._temperature)
    #     # return self._temperature
    #     return 0

    def get_temperature(self):
        """Get the most recent humidity value (%)."""
        with self._lock:
            self._humidity, self._temperature = Adafruit_DHT.read_retry(11,5)
            return self._temperature

    def insertDB(self, sensor_name, data):
        # print("call insertDB")
        with self._lock:
            conn = sqlite3.connect('echo.db')
            c = conn.cursor()
            reading_time = time.ctime()
            # print(reading_time,"here")
            # reading_time = time.localtime()

            # print(reading_time)
            c.execute('INSERT INTO readings VALUES (?, ?, ?, ?)',
                            (self.id, reading_time, format(sensor_name), data))
            conn.commit()

            conn.close()
            self.id += 1





