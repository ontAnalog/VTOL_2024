
from dronekit import connect, VehicleMode
#from module_serial import SerialCommunicator
import time


class PixhawkData:
    def _init_(self, vehicle):
        self.vehicle = vehicle

    def get_gps_data(self):
        gps_data = self.vehicle.location.global_frame
        return {
            'latitude': gps_data.lat,
            'longitude': gps_data.lon,
            'altitude': gps_data.alt
        }

    def get_attitude_data(self):
        attitude = self.vehicle.attitude
        return {
            'roll': attitude.roll,
            'pitch': attitude.pitch,
            'yaw': attitude.yaw
        }

    def get_velocity_data(self):
        velocity = self.vehicle.velocity
        return {
            'north': velocity[0],
            'east': velocity[1],
            'down': velocity[2]
        }

    def get_battery_data(self):
        battery = self.vehicle.battery
        return {
            'voltage': battery.voltage,
            'current': battery.current,
            'level': battery.level
        }

    def get_mode(self):
        return self.vehicle.mode.name

    def get_compass_data(self):
        return {'heading': self.vehicle.heading}

    def get_barometer_data(self):
        return {'altitude': self.vehicle.location.global_relative_frame.alt}


def connect_pixhawk():
    port_pixhawk = "/dev/ttyACM0"
    baudrate_pixhawk = 921600
    try:
        print("Connecting to Pixhawk")
        vehicle = connect(port_pixhawk, baud=baudrate_pixhawk, wait_ready=True)
        return vehicle
    except Exception as e:
        print(f"Failed to connect to Pixhawk: {e}")
        return None


# def connect_arduino():
#     port_arduino = "/dev/ttyACM1"
#     baudrate_arduino = 57600
#     serial_comm = SerialCommunicator(
#         port=port_arduino, baudrate=baudrate_arduino)
#     while not serial_comm.is_connected:
#         try:
#             serial_comm.begin()
#             if serial_comm.is_connected:
#                 print(f"Port {port_arduino} is successfully opened.")
#             else:
#                 raise Exception("Port is not available")
#         except Exception as e:
#             print(f"Failed to open port {port_arduino}: {e}")
#             print("Retrying in 5 seconds...")
#             time.sleep(5)
#     return serial_comm


def retrieve_data_from_pixhawk(vehicle):
    pixhawk_data = PixhawkData(vehicle)
    global mode_data
    gps_data = pixhawk_data.get_gps_data()
    attitude_data = pixhawk_data.get_attitude_data()
    velocity_data = pixhawk_data.get_velocity_data()
    battery_data = pixhawk_data.get_battery_data()
    mode_data = pixhawk_data.get_mode()
    compass_data = pixhawk_data.get_compass_data()
    barometer_data = pixhawk_data.get_barometer_data()

    print(f"GPS Data: {gps_data}")
    print(f"Attitude Data: {attitude_data}")
    print(f"Velocity Data: {velocity_data}")
    print(f"Battery Data: {battery_data}")
    print(f"Mode: {mode_data}")
    print(f"Compass Data: {compass_data}")
    print(f"Barometer Data: {barometer_data}")


# def retrieve_data_from_arduino():
#     serial_comm.flush()
#     response = serial_comm.parsing(",", 5, 500)

#     if isinstance(response, list) and len(response) == 5:
#         sensor_depan, sensor_belakang, sensor_kanan, sensor_kiri, sensor_bawah = response
#     else:
#         sensor_depan = sensor_belakang = sensor_kanan = sensor_kiri = sensor_bawah = "N/A"

#     print(f"Sensor Depan: {sensor_depan}")
#     print(f"Sensor Belakang: {sensor_belakang}")
#     print(f"Sensor Kanan: {sensor_kanan}")
#     print(f"Sensor Kiri: {sensor_kiri}")
#     print(f"Sensor Bawah: {sensor_bawah}")


def arm_drone(vehicle):
    print("Checking pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    # vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Motors are armed!")


def disarm_drone(vehicle):
    print("Disarming motors")
    vehicle.armed = False

    while vehicle.armed:
        print(" Waiting for disarming...")
        time.sleep(1)

    print("Motors are disarmed!")


def takeoff_drone(vehicle, altitude):
    print(f"Taking off to {altitude} meters...")

    if vehicle.armed:
        vehicle.simple_takeoff(altitude)

        # Wait until the vehicle reaches the target altitude
        while True:
            current_altitude = vehicle.location.global_relative_frame.alt
            print(f"Current altitude: {current_altitude} meters")
            if current_altitude >= altitude * 0.95:  # Check if within 5% of target altitude
                print("Reached target altitude.")
                break
            time.sleep(1)
    else:
        print("Cannot take off, drone is not armed!")


def land_drone(vehicle):
    print("Landing...")

    if vehicle.armed:
        # vehicle.mode = VehicleMode("LAND")

        # Wait until the vehicle is landed
        while vehicle.location.global_relative_frame.alt > 0.1:
            print(
                f"Current altitude: {vehicle.location.global_relative_frame.alt} meters")
            time.sleep(1)

        print("Landed successfully!")
        disarm_drone(vehicle)
    else:
        print("Cannot land, drone is not armed!")


def main():
    # global serial_comm

    vehicle = connect_pixhawk()
    if vehicle is None:
        return

    # serial_comm = connect_arduino()

    try:
        # Ambil data dari Pixhawk dan Arduino
        retrieve_data_from_pixhawk(vehicle)
        # retrieve_data_from_arduino()

        # LOGIKA TERBANG
        if mode_data == "GUIDED" :
            arm_drone(vehicle)
            print("Arm")
        
        else :
            disarm_drone(vehicle)
            print("disarm")

    except KeyboardInterrupt:
        print("Terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        vehicle.close()
        # serial_comm.end()
        print("Connections closed")


if __name__ == "__main__":
    main()