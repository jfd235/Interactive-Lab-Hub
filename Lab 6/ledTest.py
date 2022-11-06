from __future__ import print_function
import qwiic_led_stick
import math
import time
import sys

def walking_rainbow(LED_stick, rainbow_length, LED_length, delay):
    red_array = [None] * LED_length
    blue_array = [None] * LED_length
    green_array = [None] * LED_length

    for j in range(0, rainbow_length):

        for i in range(0, LED_length):
            # There are n colors generated for the rainbow
            # The value of n determins which color is generated at each pixel
            n = i + 1 - j

            # Loop n so that it is always between 1 and rainbow_length
            if n <= 0:
                n = n + rainbow_length

            # The nth color is between red and yellow
            if n <= math.floor(rainbow_length / 6):
                red_array[i] = 255
                green_array[i] = int(math.floor(6 * 255 / rainbow_length * n))
                blue_array[i] = 0
            
            # The nth color is between yellow and green
            elif n <= math.floor(rainbow_length / 3):
                red_array[i] = int(math.floor(510 - 6 * 255 / rainbow_length * n))
                green_array[i] = 255
                blue_array[i] = 0
            
            # The nth color is between green and cyan
            elif n <= math.floor(rainbow_length / 2):
                red_array[i] = 0
                green_array[i] = 255
                blue_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 510))
            
            # The nth color is between blue and magenta
            elif n <= math.floor(5 * rainbow_length / 6):
                red_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 1020))
                green_array[i] = 0
                blue_array[i] = 255
            
            # The nth color is between magenta and red
            else:
                red_array[i] = 255
                green_array[i] = 0
                blue_array[i] = int(math.floor(1530 - (6 *255 / rainbow_length * n)))

        # Set all the LEDs to the color values accordig to the arrays
        LED_stick.set_all_LED_unique_color(red_array, green_array, blue_array, LED_length)
        time.sleep(delay)

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 1")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    while True:
        walking_rainbow(my_stick, 20, 10, 0.3)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 8")
        sys.exit(0)