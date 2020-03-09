# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from Adafruit_PCA9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

c = int(input("channel : "))

# Create a simple PCA9685 class instance.
pca = PCA9685()

# Set the PWM frequency to 60hz.
freq  = int(input("freq : "))
pca.set_pwm_freq(freq)

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

while(True):
	a = int(input("duty : "))
	pca.set_pwm(c, 0, a)
