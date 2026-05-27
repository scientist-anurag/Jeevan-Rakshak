import cv2
import serial
import time
import numpy as np

# ==================== CONFIGURATION ====================
ARDUINO_PORT = 'COM5'  # Change to your Arduino port
BAUD_RATE = 9600
SERIAL_TIMEOUT = 1

MIN_CONTOUR_AREA = 500     # Lower area threshold for high sensitivity
ALERT_COOLDOWN = 1.0       # Seconds between alerts

CAMERA_INDEX = 0            # Default webcam
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ==================== INITIALIZATION ====================
print("=== Smart Motion Tracker ===")

# Initialize camera
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
if not cap.isOpened():
    print("ERROR: Cannot access camera!")
    exit()
print("Camera initialized")

# Initialize serial to Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
    time.sleep(2)  # Allow Arduino to reset
    print(f"Connected to Arduino on {ARDUINO_PORT}")
except Exception as e:
    print(f"ERROR: Cannot connect to Arduino - {e}")
    cap.release()
    exit()

# ==================== VARIABLES ====================
prev_frame = None
last_alert_time = 0
alert_count = 0
tracked_objects = []

# ==================== FUNCTION ====================
def track_motion(contours, frame):
    global tracked_objects
    boxes = []

    for contour in contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            (x, y, w, h) = cv2.boundingRect(contour)
            boxes.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "MOTION DETECTED", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    tracked_objects = boxes
    return len(boxes) > 0

# ==================== MAIN LOOP ====================
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read frame")
            break

        display_frame = frame.copy()
        detected = False

        # --- MOTION DETECTION ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        frame_diff = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_diff, 15, 255, cv2.THRESH_BINARY)[1]  # more sensitive
        thresh = cv2.dilate(thresh, None, iterations=3)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected = track_motion(contours, display_frame)

        prev_frame = gray

        # --- SEND ALERT TO ARDUINO ---
        current_time = time.time()
        if detected and (current_time - last_alert_time) >= ALERT_COOLDOWN:
            try:
                arduino.write(b'ALERT\n')
                alert_count += 1
                last_alert_time = current_time
                print(f"[{time.strftime('%H:%M:%S')}] Alert #{alert_count} sent")
            except Exception as e:
                print(f"ERROR sending to Arduino: {e}")

        # --- DISPLAY FRAME ---
        status_color = (0, 255, 0) if not detected else (0, 0, 255)
        status_text = "MONITORING" if not detected else "TRACKING OBJECT"
        cv2.putText(display_frame, status_text, (10, FRAME_HEIGHT - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(display_frame, f"Alerts: {alert_count}", (10, FRAME_HEIGHT - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('Smart Motion Tracker', display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Shutting down system...")
            break

except KeyboardInterrupt:
    print("Detection interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    print(f"System shutdown complete. Total alerts sent: {alert_count}")
import cv2
import serial
import time
import numpy as np

# ==================== CONFIGURATION ====================
ARDUINO_PORT = 'COM5'  # Change to your Arduino port
BAUD_RATE = 9600
SERIAL_TIMEOUT = 1

MIN_CONTOUR_AREA = 500     # Lower area threshold for high sensitivity
ALERT_COOLDOWN = 1.0       # Seconds between alerts

CAMERA_INDEX = 0            # Default webcam
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ==================== INITIALIZATION ====================
print("=== Smart Motion Tracker ===")

# Initialize camera
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
if not cap.isOpened():
    print("ERROR: Cannot access camera!")
    exit()
print("Camera initialized")

# Initialize serial to Arduino
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
    time.sleep(2)  # Allow Arduino to reset
    print(f"Connected to Arduino on {ARDUINO_PORT}")
except Exception as e:
    print(f"ERROR: Cannot connect to Arduino - {e}")
    cap.release()
    exit()

# ==================== VARIABLES ====================
prev_frame = None
last_alert_time = 0
alert_count = 0
tracked_objects = []

# ==================== FUNCTION ====================
def track_motion(contours, frame):
    global tracked_objects
    boxes = []

    for contour in contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            (x, y, w, h) = cv2.boundingRect(contour)
            boxes.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "MOTION DETECTED", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    tracked_objects = boxes
    return len(boxes) > 0

# ==================== MAIN LOOP ====================
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Failed to read frame")
            break

        display_frame = frame.copy()
        detected = False

        # --- MOTION DETECTION ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        frame_diff = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_diff, 15, 255, cv2.THRESH_BINARY)[1]  # more sensitive
        thresh = cv2.dilate(thresh, None, iterations=3)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detected = track_motion(contours, display_frame)

        prev_frame = gray

        # --- SEND ALERT TO ARDUINO ---
        current_time = time.time()
        if detected and (current_time - last_alert_time) >= ALERT_COOLDOWN:
            try:
                arduino.write(b'ALERT\n')
                alert_count += 1
                last_alert_time = current_time
                print(f"[{time.strftime('%H:%M:%S')}] Alert #{alert_count} sent")
            except Exception as e:
                print(f"ERROR sending to Arduino: {e}")

        # --- DISPLAY FRAME ---
        status_color = (0, 255, 0) if not detected else (0, 0, 255)
        status_text = "MONITORING" if not detected else "TRACKING OBJECT"
        cv2.putText(display_frame, status_text, (10, FRAME_HEIGHT - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(display_frame, f"Alerts: {alert_count}", (10, FRAME_HEIGHT - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('Smart Motion Tracker', display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Shutting down system...")
            break

except KeyboardInterrupt:
    print("Detection interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    print(f"System shutdown complete. Total alerts sent: {alert_count}")
