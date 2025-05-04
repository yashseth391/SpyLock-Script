import cv2
import time
from send_email import send_email
CAMERA_INDEX = 0  # Default camera index
# Function to capture a photo from the webcam
sender_email = "yashseth391@gmail.com"  # Replace with your email
sender_password = "snsj dqqw qtdu oilc"  # Replace with your email password
recipient_email = "yashseth391@gmail.com"  # Replace with the recipient's email
subject = "Unauthorized Access Detected"  # Subject of the email
body = "An unauthorized access attempt was detected. See the attached photo."  # Body of the email

def capture_photo():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Unable to access the camera")
        return False
    ret, frame = cap.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        photo_path = f"unauthorized_{timestamp}.jpg"
        cv2.imwrite(photo_path, frame)
        print(f"✅ Photo saved to {photo_path}")
        
        send_email(sender_email, sender_password, recipient_email, subject, body, photo_path)
    cap.release()
    return ret
