# -*- coding: utf-8 -*-
"""
A MicroPython library for the AS5600 magnetic rotary position sensor.
"""
from microbit import i2c, Image, sleep

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
