import cv2
from pyzbar.pyzbar import decode
import os
from PyQt5.QtCore import pyqtSignal


CURRENT_DIR= os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
cap.set(cv2.CAP_PROP_EXPOSURE,-5)
def scanLoop(scanSignal:pyqtSignal):
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Scan barcodes
        barcodes = decode(frame)

        for barcode in barcodes:
            data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            scanSignal.emit(str(data))
            # Draw rectangle around barcode
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        frame = cv2.resize(frame,(640,480))
        cv2.imshow("Barcode Scanner", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()