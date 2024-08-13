import time
import board
import busio
import adafruit_vl53l1x

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l1x.VL53L1X(i2c)

# Inisialisasi sensor
vl53.start_ranging()

def read_distance():
    return vl53.distance

# Contoh membaca data jarak
while True:
    distance = read_distance()
    print(f"Distance: {distance} mm")
    time.sleep(1)
