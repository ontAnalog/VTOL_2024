import time
import VL53L0X  # type: ignore

# Menginisialisasi sensor VL53L0X
tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)

def read_altitude_sensor():
    distance = tof.get_distance()
    # Konversi jarak ke meter jika diperlukan
    return distance / 1000.0
