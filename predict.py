import serial
import time
import re
import pickle
import numpy as np

# Load pre-trained Isolation Forest model
with open('iso_forest.pkl', 'rb') as f:
    model = pickle.load(f)
    print("🔍 Model type:", type(model))
# Connect to Arduino
try:
    ser = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)  # wait for Arduino to reset
    print("✅ Connected to COM6")
except Exception as e:
    print("❌ Failed to connect to COM6:", e)
    exit()

# Read and analyze data
while True:
    try:
        line = ser.readline().decode('utf-8').strip()

        if "Temperature" in line:
            temp_line = line
            hum_line = ser.readline().decode('utf-8').strip()

            temp_match = re.search(r"([-+]?\d*\.\d+|\d+)", temp_line)
            hum_match = re.search(r"([-+]?\d*\.\d+|\d+)", hum_line)

            if temp_match and hum_match:
                temperature = float(temp_match.group(1))
                humidity = float(hum_match.group(1))

                prediction = model.predict([[temperature, humidity]])

                if prediction[0] == -1:
                    print(f"⚠️ Anomaly Detected! Temp={temperature}, Hum={humidity}")
                else:
                    print(f"✅ Normal: Temp={temperature}, Hum={humidity}")
    except Exception as e:
        print("⚠️ Error reading serial:", e)