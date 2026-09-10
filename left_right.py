import requests
import keyboard
import time

# ESP32 Default SoftAP Address
ESP32_URL = "http://192.168.4.1/command"

# Cooldown delay prevents crashing the ESP32 by sending hundreds of commands per second
COOLDOWN = 1.0  
last_press = 0

def send_command(direction):
    print(f"\n[DEBUG] Sending command -> '{direction}'")
    try:
        # Timeout set to 2 seconds to catch disconnected Wi-Fi
        response = requests.get(ESP32_URL, params={'cmd': direction}, timeout=2)
        print(f"[SUCCESS] ESP32 Response: {response.text}")
    except requests.exceptions.Timeout:
        print("[ERROR] Timeout: ESP32 took too long to reply.")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection refused. Check if you are connected to 'ESP32_Control' Wi-Fi.")
    except Exception as e:
        print(f"[ERROR] Unexpected issue: {e}")

print("=========================================")
print("      WIRELESS STEPPER CONTROLLER        ")
print("=========================================")
print(" [RIGHT ARROW] -> Spin Clockwise")
print(" [LEFT ARROW]  -> Spin Anti-Clockwise")
print(" [ESC]         -> Quit Script")
print("=========================================\n")

while True:
    now = time.time()
    
    if keyboard.is_pressed('right') and (now - last_press > COOLDOWN):
        send_command('cw')
        last_press = now
        
    elif keyboard.is_pressed('left') and (now - last_press > COOLDOWN):
        send_command('ccw')
        last_press = now
        
    elif keyboard.is_pressed('esc'):
        print("\n[EXIT] Closing controller...")
        break
        
    time.sleep(0.05) # Keeps CPU usage low
