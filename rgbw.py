import numpy as np
import datetime

def time_to_kelvin_and_illuminance(current_time, current_date=None):
    """
    Convert the current time to a Kelvin temperature and relative illuminance to mimic daylight.
    
    Args:
    - current_time (datetime.time): The current time.
    - current_date (datetime.date, optional): The current date. Defaults to today's date.
    
    Returns:
    - kelvin (int): The corresponding color temperature in Kelvin.
    - illuminance (float): Relative illuminance (0.0 to 1.0).
    """
    # Default to today's date if no date is provided
    if current_date is None:
        current_date = datetime.date.today()
    
    # Determine if it's a weekend
    is_weekend = current_date.weekday() >= 5  # Saturday (5) or Sunday (6)
    
    # Set sunrise and sunset times (in minutes from midnight)
    sunrise = 6 * 60 if not is_weekend else 8 * 60 + 30  # 6:00 AM on weekdays, 8:30 AM on weekends
    sunset = 18 * 60  # 6:00 PM for both weekdays and weekends
    
    # Convert current time to minutes since midnight
    current_minutes = current_time.hour * 60 + current_time.minute
    
    # Define the range of Kelvin temperatures for daylight
    min_kelvin = 2000  # Warm light at sunrise/sunset
    max_kelvin = 6500  # Cool light at midday
    
    # Before sunrise or after sunset, return the warmest light and no illuminance
    if current_minutes < sunrise:
        return min_kelvin, 0.0  # Lights are off before sunrise
    elif current_minutes > sunset:
        return min_kelvin, 0.0  # Lights are off after sunset
    
    # Calculate the midpoint of the day (noon)
    midday = (sunrise + sunset) / 2
    
    # Scale time to a 0-π range for smooth transitions
    x = (current_minutes - sunrise) / (sunset - sunrise) * np.pi
    
    # Use a sine wave to model the transition in color temperature
    kelvin = min_kelvin + (max_kelvin - min_kelvin) * np.sin(x)
    
    # Calculate relative illuminance:
    # Linearly fade in from sunrise to midday (0 to 1), then fade out from midday to sunset
    if current_minutes <= midday:
        # Fade in: Map [sunrise, midday] to [0, 1]
        illuminance = (current_minutes - sunrise) / (midday - sunrise)
    else:
        # Fade out: Map [midday, sunset] to [1, 0]
        illuminance = (sunset - current_minutes) / (sunset - midday)
    
    return int(kelvin), float(illuminance)


def rgb_to_rgbw(target, backlight):
    """
    Converts RGB array to a RGBW array. Ultilizes the W channel as much as possible.

    Args:
        target (np.ndarray): The target colour spectrum to be approximated as RGB.
        backlight (np.ndarray): Apprximate colour of the white channel as an RGB array.

    Returns:
        np.ndarray: An array of RGBW values to appoximate target colour. Rounded to the nearest integer. (0-255)
    """
    # Subtract backlight components
    residual = target - backlight

    # Use minimum component to find white channel value
    imin = np.argmin(residual)
    white = 1 - abs(residual[imin]/backlight[imin])

    # Apply white channel sclalar to obtain new RGB values
    adjusted = target - white * backlight

    # Return RGBW as numpy array
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



