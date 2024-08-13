from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connnect to the vehicle
import argparse
parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect

print("Connection on the vehicle on %s"%connection_string)
vehicle = connect(connection_string, wait_ready=True)

# Fungsi untuk melakukan arm dan takeoff ke ketinggian tertentu
def arm_and_takeoff(vehicle, target_altitude):
    print("Persiapan untuk arm motor")
    while not vehicle.is_armable:
        print("Menunggu drone siap untuk di-arm... Status: ", vehicle.system_status.state)
        time.sleep(1)
    
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    print("Arming motor")
    
    # while not vehicle.mode.name == 'GUIDED':
    #     print("Menunggu mode GUIDED... Mode saat ini: ", vehicle.mode.name)
    #     time.sleep(1)
    # vehicle.armed = True

    while not vehicle.armed:
        print("Menunggu motor di-arm...")
        time.sleep(1)

    print("Takeoff!")
    vehicle.simple_takeoff(target_altitude)

    # Tunggu sampai drone mencapai ketinggian target
    while True:
        print("Ketinggian saat ini: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude - 1:
            print("Mencapai ketinggian target")
            break
        time.sleep(1)

# Fungsi untuk mendaratkan drone
def land_drone(vehicle):
    print("Landing...")
    vehicle.mode = VehicleMode("LAND")
    while vehicle.armed:
        print("Menunggu drone mendarat...")
        time.sleep(1)
    print("Drone telah mendarat")

# Fungsi utama
def main():
    connection_string = '127.0.0.1:14551'  # Ubah sesuai dengan koneksi drone Anda
    vehicle = connect(connection_string)

    try:
        # Terbang ke ketinggian 10 meter
        arm_and_takeoff(vehicle, 10)
        time.sleep(5)  # Biarkan drone berada di ketinggian 10 meter selama 5 detik

        # Mendaratkan drone
        land_drone(vehicle)

    finally:
        # Menutup koneksi ke drone
        print("Menutup koneksi ke drone")
        vehicle.close()

if __name__ == "__main__":
    main()
