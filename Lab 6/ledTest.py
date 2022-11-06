from __future__ import print_function
import qwiic_led_stick
import time
import sys

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 3")
    my_stick = qwiic_led_stick.QwiicLEDStick()

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    # Initialize LEDs as a rainbow followed by 1 white pixel
    red_list = [255, 255, 170, 0, 0, 0, 0, 170, 255, 255]
    green_list = [0, 170, 255, 255, 255, 170, 0, 0, 0, 255]
    blue_list = [0, 0, 0, 0, 170, 255, 255, 255, 170, 255]

    # Turn on the LED Stick according to the 3 arrays
    my_stick.set_all_LED_unique_color(red_list, green_list, blue_list, 10)

    while True:

        # This will step through each available brightness setting
        # Brightness values can be from 0 - 31
        for i in range(0, 32):
            my_stick.set_all_LED_brightness(i)

            print("\nBrightness level: " + str(i))
            time.sleep(1)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 4")
        sys.exit(0)