import cv2
import pytesseract

def recognize_numbers(image_path):
    # Lade das Bild mit OpenCV
    image = cv2.imread("C:\\Users\\skill\\OneDrive\\AIN\\Semester 8\\2D-ComputerVision\\Projekt\\untitled.png")
    
    # Konvertiere das Bild in Graustufen, um die Zahlenerkennung zu erleichtern
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Verbessere den Kontrast des Bildes (optional)
    gray = cv2.equalizeHist(gray)
    
    # Wende eine Kantenerkennung an, um die Zahlen besser hervorzuheben (optional)
    edges = cv2.Canny(gray, 50, 150)
    
    # Verwende Tesseract zur Texterkennung
    numbers = pytesseract.image_to_string(edges, config='--psm 6')
    
    # Filtere erkannte Zeichen und behalte nur Zahlen
    recognized_numbers = ''.join(filter(str.isdigit, numbers))
    
    return recognized_numbers

print(recognize_numbers(1))