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
    print("\n RMCS-3001 Modbus CLI Test Menu")
    print("Choose a command:")
    print(" 1. Set Reg 0 to default ID - 511")
    print(" 2. Read Reg 0 (40001) to verify ID")
    print(" 3. Exit")
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
            write_register(0, 511, "Set ID (1)")
        elif choice == "2":
            read_register(0, "ID", "Read Device ID")
        else:
            print("⚠️ Invalid choice")

        time.sleep(0.5)

    client.close()
    print("🔌 Disconnected from RMCS-3001")

if __name__ == "__main__":
    main()
