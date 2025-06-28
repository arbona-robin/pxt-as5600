# -*- coding: utf-8 -*-
"""
This script reads the angle from an AS5600 magnetic rotary position sensor
and displays the direction on the micro:bit's LED matrix using an OOP approach.
"""
from microbit import i2c, display, Image, sleep

class AS5600:
    """A class to interact with the AS5600 magnetic rotary position sensor."""

    # I2C and Register constants
    DEFAULT_ADDRESS = 0x36
    STATUS_REGISTER = b'\x0b'
    ANGLE_REGISTER = b'\x0e'
    RAW_ANGLE_MAX = 4096
    DEGREES_PER_RAW_UNIT = 360 / RAW_ANGLE_MAX

    def __init__(self, i2c_bus, address=DEFAULT_ADDRESS):
        """
        Initializes the sensor object.

        Args:
            i2c_bus: The initialized I2C bus object from the microbit module.
            address (int): The I2C address of the sensor.
        """
        self._i2c = i2c_bus
        self.address = address
        self._status_cache = 0
        self._status_updated = False

    def is_connected(self):
        """Checks if the sensor is connected and responsive."""
        return self.address in self._i2c.scan()

    def _update_status(self):
        """Reads the status register and caches its value."""
        try:
            self._i2c.write(self.address, self.STATUS_REGISTER)
            self._status_cache = self._i2c.read(self.address, 1)[0]
            self._status_updated = True
        except OSError:
            self._status_cache = 0
            self._status_updated = False

    @property
    def magnet_detected(self):
        """Returns True if a magnet is detected."""
        if not self._status_updated:
            self._update_status()
        return (self._status_cache >> 5) & 1 == 1

    @property
    def magnet_too_weak(self):
        """Returns True if the magnet is too far away."""
        if not self._status_updated:
            self._update_status()
        return (self._status_cache >> 4) & 1 == 1

    @property
    def magnet_too_strong(self):
        """Returns True if the magnet is too close."""
        if not self._status_updated:
            self._update_status()
        return (self._status_cache >> 3) & 1 == 1

    @property
    def angle(self):
        """
        Reads the raw angle from the sensor and converts it to degrees.

        Returns:
            The angle in degrees (0-360), or None if an error occurs.
        """
        try:
            self._i2c.write(self.address, self.ANGLE_REGISTER)
            data = self._i2c.read(self.address, 2)
            raw_angle = (data[0] << 8) | data[1]
            return raw_angle * self.DEGREES_PER_RAW_UNIT
        except OSError:
            return None

    def clear_status_cache(self):
        """Clears the status cache to force a fresh read on the next property access."""
        self._status_updated = False

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