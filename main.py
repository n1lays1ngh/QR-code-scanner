import cv2
import numpy as np
from pyzbar.pyzbar import decode
import threading

def decoder(image):
    
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcode = decode(gray_img)
    
    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))

        
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = f"Data: {barcodeData} | Type: {barcodeType}"

        
        cv2.putText(image, string, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        print(f"Barcode: {barcodeData} | Type: {barcodeType}")

def scan_from_webcam():
   
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        decoder(frame)
        cv2.imshow("Barcode/QR Code Scanner", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def scan_from_image():
    
    img_path = input("Enter Image Path: ")
    img = cv2.imread(img_path)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        print(f"QRCode Encoded Data: {data}")
    else:
        print("No QR code found.")

    decoder(img)
    cv2.imshow("Scanned Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("1. Scan via Image")
    print("2. Scan via Webcam")

    choice = int(input("Choice: "))

    if choice == 2:
        threading.Thread(target=scan_from_webcam).start()
    elif choice == 1:
        scan_from_image()

