import numpy as np

def rgb_to_rgbw(target, backlight):
    residual = target - backlight
    imin = np.argmin(residual)
    white = 1 - abs(residual[imin]/backlight[imin])

    adjusted = target - white * backlight

    return np.array([round(adjusted[0]), round(adjusted[1]), round(adjusted[2]), round(white*255)])


def kelvin_to_rgb(temperature):
    """
    Converts a color temperature in Kelvin to an RGB array.
    
    Args:
        temperature (float): The color temperature in Kelvin (1000 to 40000).
        
    Returns:
        np.ndarray: An array of RGB values [R, G, B], rounded to the nearest integer.
    """
    temperature = temperature / 100.0
    
    # Calculate Red
    if temperature <= 66:
        red = 255
    else:
        red = 329.698727446 * ((temperature - 60) ** -0.1332047592)
        red = np.clip(red, 0, 255)
    
    # Calculate Green
    if temperature <= 66:
        green = 99.4708025861 * np.log(temperature) - 161.1195681661
    else:
        green = 288.1221695283 * ((temperature - 60) ** -0.0755148492)
    green = np.clip(green, 0, 255)
    
    # Calculate Blue
    if temperature >= 66:
        blue = 255
    elif temperature <= 19:
        blue = 0
    else:
        blue = 138.5177312231 * np.log(temperature - 10) - 305.0447927307
        blue = np.clip(blue, 0, 255)
    
    # Return RGB as a NumPy array
    return np.round([red, green, blue]).astype(int)

def kelvin_to_rgbw(temperature, backlight_temp):
    target = kelvin_to_rgb(temperature)
    backlight = kelvin_to_rgb(backlight_temp)

    return rgb_to_rgbw(target, backlight)

if __name__=='__main__':
    import sys

    colour = int(sys.argv[1])

    print(kelvin_to_rgbw(colour, 4000))



