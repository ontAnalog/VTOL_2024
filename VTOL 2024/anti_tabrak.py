import time
import math
from pymavlink import mavutil
import board
import busio
import adafruit_vl53l1x

# Koneksi ke drone
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

# Inisialisasi sensor
i2c = busio.I2C(board.SCL, board.SDA)
vl53_altitude = adafruit_vl53l1x.VL53L1X(i2c)
vl53_front = adafruit_vl53l1x.VL53L1X(i2c, address=0x29)
vl53_back = adafruit_vl53l1x.VL53L1X(i2c, address=0x30)
vl53_right = adafruit_vl53l1x.VL53L1X(i2c, address=0x31)
vl53_left = adafruit_vl53l1x.VL53L1X(i2c, address=0x32)

vl53_altitude.start_ranging()
vl53_front.start_ranging()
vl53_back.start_ranging()
vl53_right.start_ranging()
vl53_left.start_ranging()

# Fungsi untuk mengambil data dari sensor
def get_sensor_data():
    altitude = vl53_altitude.distance / 1000.0
    front_distance = vl53_front.distance / 1000.0
    back_distance = vl53_back.distance / 1000.0
    right_distance = vl53_right.distance / 1000.0
    left_distance = vl53_left.distance / 1000.0
    return altitude, front_distance, back_distance, right_distance, left_distance

# Fungsi untuk mengirim perintah ke drone
def send_movement_command(vx, vy, vz, yaw_rate):
    master.mav.send(mavutil.mavlink.MAV_CMD_NAV_VELOCITY_GLOBAL_INT,
                    vx, vy, vz, yaw_rate, 0, 0, 0, 0, 0, 0)

# Loop utama
while True:
    altitude, front, back, right, left = get_sensor_data()
    
    if front < 1.0:
        # Terbang ke kiri jika ada obstacle di depan
        if left > 1.0:
            send_movement_command(0, -1, 0, 0)
        elif right > 1.0:
            send_movement_command(0, 1, 0, 0)
    elif altitude < 1.2:
        # Naikkan ketinggian jika ketinggian kurang dari 1.2m
        send_movement_command(0, 0, 1, 0)
    else:
        # Bergerak maju jika tidak ada obstacle di depan dan ketinggian cukup
        send_movement_command(1, 0, 0, 0)
    
    time.sleep(0.1)
