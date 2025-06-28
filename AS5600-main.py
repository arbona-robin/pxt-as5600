# -*- coding: utf-8 -*-
"""
This script reads the angle from an AS5600 magnetic rotary position sensor
and displays the direction on the micro:bit's LED matrix.
"""
from microbit import i2c, display, Image, sleep
from as5600 import AS5600

# --- Display Logic ---

ARROW_IMAGES = [
    Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE,
    Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW
]

def display_direction(degrees):
    """Displays an arrow on the micro:bit corresponding to the given angle."""
    if degrees is None:
        return
    # Map the angle (0-360) to an index (0-7) for the ARROW_IMAGES list
    direction_index = round(degrees / 45) % 8
    display.show(ARROW_IMAGES[direction_index])

# --- Main Application ---

def main():
    """Main function to initialize the sensor and run the main loop."""
    i2c.init()
    sensor = AS5600(i2c)

    while True:
        sensor.clear_status_cache() # Force status update on each loop iteration

        if not sensor.is_connected():
            print("Sensor not detected")
            display.show(Image.SKULL)
        elif sensor.magnet_too_strong:
            print("Magnet too strong")
            display.show(Image.ANGRY)
        elif sensor.magnet_too_weak:
            print("Magnet too weak")
            display.show(Image.NO)
        elif sensor.magnet_detected:
            current_angle = sensor.angle
            if current_angle is not None:
                print("Angle: {:.2f}".format(current_angle))
                display_direction(current_angle)
            else:
                # Handle I2C read error for angle
                display.show(Image.CONFUSED)
        else:
            print("No magnet detected")
            display.show(Image.SAD)

        sleep(200)

if __name__ == "__main__":
    main()
