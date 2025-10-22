 SpyLock – Unauthorized Access Detection System

SpyLock is a Python-based desktop security tool that monitors user activity and detects unauthorized access. If suspicious behavior is detected (e.g., keyboard/mouse activity), the system prompts for a password. After multiple failed attempts, it captures an image using the webcam, locks the system, and sends the photo to a predefined email address.

---

 Features

-  Monitors keyboard and mouse activity
-  Fullscreen password prompt after suspicious interaction
- 🖼 Animated GIF alert on screen
-  Captures webcam photo after failed password attempts
-  Sends captured image via Gmail SMTP
-  Automatically locks the computer


 Gmail SMTP Setup

> Gmail requires **2-Step Verification** and **App Passwords** for third-party access

 1. Enable 2FA:  
https://myaccount.google.com/security → Turn on **2-Step Verification**

 2. Generate App Password:  
https://myaccount.google.com/apppasswords  
→ Choose **Mail** > **Other (Custom Name)** > Enter `Python Script`  
→ Copy the 16-character App Password

IMAGES:
![image](https://github.com/user-attachments/assets/df17101a-05f2-4f3a-9ccd-df44feb7bbda)


![image](https://github.com/user-attachments/assets/16981c0d-183c-4a89-ad74-026622e2dc82)




 Setup Instructions
 1. Clone the Repo
```bash
git clone https://github.com/yashseth391/Spy_Lock.git
cd Spy_Lock
