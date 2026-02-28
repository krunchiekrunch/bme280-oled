import smbus2
import bme280
import time
import pytz
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

address = 0x76

bus = smbus2.SMBus(1)

calibration_params = bme280.load_calibration_params(bus, address)

i2c = busio.I2C(board.SCL, board.SDA)

disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

desired_timezone = pytz.timezone('Europe/London')

try:
    while True:
        data = bme280.sample(bus, address, calibration_params)

        temperature_celsius = data.temperature
        humidity = data.humidity
        pressure = data.pressure
        timestamp = data.timestamp

        # convert timestamp to chosen timezone
        timestamp_tz = timestamp.replace(tzinfo=pytz.utc).astimezone(desired_timezone)

        # format
        time_only_str = timestamp_tz.strftime('%H:%M:%S')
        date_only_str = timestamp_tz.strftime('%d/%m/%Y')
        temp_str = f"Temp: {temperature_celsius:.1f}C"
        hum_str = f"Humidity: {humidity:.1f}%"
        pres_str = f"Pressure: {pressure:.2f} hPa"

        # console log
        print(f"{time_only_str} {date_only_str} {temp_str}, {hum_str}, {pres_str}")

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # time on left, date to right
        draw.text((0, 0), time_only_str, font=font, fill=255)
        date_bbox = font.getbbox(date_only_str)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((width - date_width, 0), date_only_str, font=font, fill=255)

        draw.text((0, 16), temp_str, font=font, fill=255)
        draw.text((0, 32), hum_str, font=font, fill=255)
        draw.text((0, 48), pres_str, font=font, fill=255)

        disp.image(image)
        disp.show()

        # update interval
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by user.")
    disp.fill(0)
    disp.show()

except Exception as e:
    print("An unexpected error occurred:", e)
    disp.fill(0)
    disp.show()
