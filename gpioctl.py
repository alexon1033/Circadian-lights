# Import necessary libraries
import gpiozero as gz  # For controlling GPIO pins on a Raspberry Pi
import rgbwCalculations as rgbwc  # Custom or external library for RGBW color temperature calculations
import datetime  # To work with the current date and time

# Define GPIO pins for each color channel
red_pin = 2
green_pin = 3
blue_pin = 4
white_pin = 5

# Define a class to control RGBW LED strips
class rgbw_controller():
    def __init__(self, red, green, blue, white):
        # Initialize PWM (Pulse Width Modulation) control for each color channel
        self.red_pin = gz.PWMLED(red)
        self.green_pin = gz.PWMLED(green)
        self.blue_pin = gz.PWMLED(blue)
        self.white_pin = gz.PWMLED(white)
    
    # Update the LED brightness values based on the RGBW values
    def update_rgbw(self):
        # Normalize RGBW values (0-255 range) to a 0-1 range for PWM control
        self.red_pin.value = self.rgbw[0] / 255
        self.green_pin.value = self.rgbw[1] / 255
        self.blue_pin.value = self.rgbw[2] / 255
        self.white_pin.value = self.rgbw[3] / 255

    # Update the LED color temperature based on the current time
    def update(self):
        # Get the current time
        time = datetime.datetime.now().time()
        # Convert the time to a corresponding Kelvin temperature
        self.temperature, self.illuminance = rgbwc.time_to_kelvin_and_illuminance(time)
        # Convert the Kelvin temperature to RGBW values
        self.rgbw = rgbwc.kelvin_to_rgbw(self.temperature)
        # Apply illuminance scaling factor
        self.rgbw = self.rgbw * self.illuminance
        # Update the LED strip with the new RGBW values
        self.update_rgbw()


if __name__ == '__main__':
    leds = rgbw_controller(red_pin, green_pin, blue_pin, white_pin)

    try:
        while True:
            leds.update()
            print(f"Debug: Lighting updated to ( {leds.temperature}k, {leds.illuminance} )\n
                RGBW[{leds.red_pin.value}, {leds.green_pin.value}, {leds.blue_pin.value}, {leds.white_pin.value}]")
            datetime.sleep(60)

    except KeyboardInterrupt:
            break
            
