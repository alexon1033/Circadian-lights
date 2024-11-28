import gpiozero as gz
import rgbwc
import datetime

red_pin = 2
green_pin = 3
blue_pin = 4
white_pin = 5

class rgbw_controller():
  def __init__(self, red, green, blue, white):
    self.red_pin = gz.PWMLED(red)
    self.green_pin = gz.PWMLED(green)
    self.blue_pin = gz.PWMLED(blue)
    self.white_pin = gz.PWMLED(white)
    
  def update_rgbw(self):
    self.red_pin.value = self.rgbw[0]/255
    self.green_pin.value = self.rgbw[1]/255
    self.blue_pin.value = self.rgbw[2]/255
    self.white_pin.value = self.rgbw[3]/255

  def update_time(self):
    time = datetime.datetime.now().time()
    self.temperature = time_to_kelvin(time)
    self.rgbw = rgbwc.kelvin_to_rgbw(temperature) 
    self.update_rgbw()

  def time_to_kelvin(time):
    @static
    return 6500

