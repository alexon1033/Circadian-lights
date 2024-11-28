import gpiozero as gz
import rgbwc

red_pin = 2
green_pin = 3
blue_pin = 4
white_pin = 5

class rgbw_controller():
  def __init__(self, red, green, blue, white):
    self.red = gz.PWMLED(red)
    self.green = gz.PWMLED(green)
    self.blue = gz.PWMLED(blue)
    self.white = gz.PWMLED(white)

  def update_rgbw(self, rgbw):
    self.red.value = rgbw[0]/255
    self.green.value = rgbw[1]/255
    self.blue.value = rgbw[2]/255
    self.white.value = rgbw[3]/255
