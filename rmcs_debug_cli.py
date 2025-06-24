# import minimalmodbus
# import serial

# print("[INFO] Trying to restore RMCS-3001 Modbus ID to 1 via broadcast (ID 0)...")

# instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 0)  # ID 0 = broadcast
# instrument.serial.baudrate = 9600
# instrument.serial.timeout = 1
# instrument.serial.parity = serial.PARITY_NONE
# instrument.serial.stopbits = 1
# instrument.serial.bytesize = 8
# instrument.mode = minimalmodbus.MODE_RTU

# try:
#     # Write 0x01FF = 511 to register 0 (40001)
#     instrument.write_register(0, 511)
    
#     print("[✅] Write success: device should now be at ID 1")
#     print("⚠️ Power cycle the driver now, then talk to ID 1")
# except Exception as e:
#     print("[❌] Broadcast write failed:", e)

###################
# Uncomment the following code to use the RMCS-3001 motor control script
# Note: This part is commented out to avoid accidental execution.
# If you want to run the motor control script, please uncomment it.

# # RMCS-3001 Motor Control Script


# import minimalmodbus
# import time

# # Configuration
# PORT = '/dev/ttyUSB0'
# SLAVE_ID = 1
# BAUDRATE = 9600

# # Connect to RMCS-3001
# instrument = minimalmodbus.Instrument(PORT, SLAVE_ID)
# instrument.serial.baudrate = BAUDRATE
# instrument.serial.timeout = 1
# instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
# instrument.serial.stopbits = 1
# instrument.serial.bytesize = 8
# instrument.mode = minimalmodbus.MODE_RTU

# def debug(msg):
#     print(f"[DEBUG] {msg}")

# def safe_write(register, value, delay=0.5):
#     try:
#         instrument.write_register(register, value)
#         debug(f"✅ Wrote {value} to register {register}")
#         time.sleep(delay)
#     except Exception as e:
#         print(f"[❌] Failed to write {value} to register {register}: {e}")
#         exit(1)

# def read_feedback():
#     try:
#         freq = instrument.read_register(7)  # Speed Feedback (Hz)
#         current = instrument.read_register(10)  # Current (Amps)
#         print(f"[INFO] Speed: {freq} Hz (~{freq*60//2} RPM), Current: {current} A")
#     except Exception as e:
#         print(f"[❌] Failed to read feedback: {e}")

# def main():
#     print("📡 Starting RMCS-3001 motor (Mode 1, Digital Closed Loop)...")

#     # Step 1: Disable motor
#     safe_write(1, 256)  # 0x0100 = Mode 1, disabled

#     # Step 2: Set frequency (e.g. 10 Hz)
#     safe_write(6, 10)   # Reg 40007 = 10 Hz

#     # Step 3: Enable motor CW
#     safe_write(1, 257)  # 0x0101 = Mode 1, CW enabled

#     # Step 4: Read speed and current
#     time.sleep(2)
#     read_feedback()

# if __name__ == "__main__":
#     main()


############
# RMCS-3001 Debug CLI
# This script is used to restore the RMCS-3001 Modbus ID to 1
# and read the register 0 (40001) to verify the connection.
# It uses the minimalmodbus library to communicate with the device.
# Uncomment the following lines to restore the RMCS-3001 Modbus ID to 1
# and read the register 0.


import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

try:
    val = instrument.read_register(0)  # 40001
    print("[✅] Read register 0:", val)
except Exception as e:
    print("[❌] Read failed:", e)
