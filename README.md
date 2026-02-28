# bme280-oled
Display BME280 data on a 0.96" I2C display

Install required packages
```
sudo apt install -y python3-pip python3-smbus i2c-tools libjpeg-dev zlib1g-dev libopenjp2-7-dev libtiff5
```

Enter Python virtual enviroment
Then install pip packages
```
pip install smbus2 RPi.bme280 pytz pillow adafruit-circuitpython-ssd1306 adafruit-blinka
```

Start program

```
python main.py
```
