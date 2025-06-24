from pymodbus.client.serial import ModbusSerialClient
import time

# === Modbus Configuration ===
client = ModbusSerialClient(
    port='/dev/ttyUSB1',
    baudrate=9600,
    bytesize=8,
    stopbits=1,
    parity='N',
    timeout=1
)

SLAVE_ID = 1

# === Utility Functions ===
def write_register(address, value, label=""):
    result = client.write_register(address=address, value=value, slave=SLAVE_ID)
    if result.isError():
        print(f"[❌] Failed to write {value} to Reg {address} ({label})")
    else:
        print(f"[✅] Wrote {value} to Reg {address} ({label})")

def read_register(address, label=""):
    result = client.read_holding_registers(address=address, count=1, slave=SLAVE_ID)
    if result.isError():
        print(f"[❌] Failed to read Reg {address} ({label})")
        return None
    else:
        val = result.registers[0]
        print(f"[📖] Reg {address} ({label}): {val}")
        return val

def command_menu():
    print("\n🧪 RMCS-3001 Modbus CLI Test Menu")
    print("Choose a command:")
    print(" 1. Set frequency to 400 Hz (Reg 6)")
    print(" 2. Set PWM to 3000 (Reg 4)")
    print(" 3. Start motor CW (Reg 2 = 257)")
    print(" 4. Brake motor (Reg 2 = 259)")
    print(" 5. Set direction to CCW (Reg 2 = 265)")
    print(" 6. Read speed feedback (Reg 7)")
    print(" 7. Read current feedback (Reg 10)")
    print(" 8. Stop motor (Reg 2 = 0)")
    print(" 9. Exit")
    print()

def main():
    if not client.connect():
        print("❌ Failed to connect to RMCS-3001")
        return

    print("✅ Connected to RMCS-3001 via /dev/ttyUSB1")

    while True:
        command_menu()
        choice = input(">> Enter command number: ").strip()

        if choice == "1":
            write_register(6, 40, "Set Frequency (Hz)")
        elif choice == "2":
            write_register(4, 1000, "Set PWM Output")
        elif choice == "3":
            write_register(2, 513, "Enable CW (Mode 1)")
        elif choice == "4":
            write_register(2, 515, "Brake (Mode 1)")
        elif choice == "5":
            write_register(2, 521, "Enable CCW (Mode 1)")
        elif choice == "6":
            read_register(8, "Speed Feedback (Hz)")
        elif choice == "7":
            read_register(10, "Current Feedback (A)")
        elif choice == "8":
            write_register(2, 512, "Disable")
        elif choice == "9":
            break
        else:
            print("⚠️ Invalid choice")

        time.sleep(0.5)

    client.close()
    print("🔌 Disconnected from RMCS-3001")

if __name__ == "__main__":
    main()

