import cv2
import numpy as np

# Fungsi untuk melakukan nothing
def nothing(x):
    pass

# Inisialisasi kamera
cap = cv2.VideoCapture(1) #webcam external
#cap = cv2.VideoCapture(0) #webcam internal

# Membuat jendela untuk trackbars
cv2.namedWindow('Trackbars')

# Membuat trackbars untuk mengatur batas bawah dan atas warna
cv2.createTrackbar('LH', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('LS', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('LV', 'Trackbars', 100, 255, nothing)
cv2.createTrackbar('UH', 'Trackbars', 25, 255, nothing)
cv2.createTrackbar('US', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('UV', 'Trackbars', 255, 255, nothing)

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()
    
    if not ret:
        break

    # Mengubah frame ke HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mendapatkan nilai trackbars
    l_h = cv2.getTrackbarPos('LH', 'Trackbars')
    l_s = cv2.getTrackbarPos('LS', 'Trackbars')
    l_v = cv2.getTrackbarPos('LV', 'Trackbars')
    u_h = cv2.getTrackbarPos('UH', 'Trackbars')
    u_s = cv2.getTrackbarPos('US', 'Trackbars')
    u_v = cv2.getTrackbarPos('UV', 'Trackbars')

    # Mendefinisikan range warna oren
    lower_orange = np.array([l_h, l_s, l_v])
    upper_orange = np.array([u_h, u_s, u_v])

    # Membuat mask untuk warna oren
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Menghasilkan hasil dari bitwise operation antara frame asli dan mask
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Menampilkan hasil
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membersihkan setelah selesai
cap.release()
cv2.destroyAllWindows()
