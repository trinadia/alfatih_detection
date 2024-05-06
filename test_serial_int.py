import serial
import time

# Define serial port and baud rate
serial_port = '/dev/ttyTHS1'  # Serial port for UART on Jetson (TX pin: pin 8, RX pin: pin 10)
baud_rate = 9600  # Baud rate must match between both devices

# Open serial port
ser = serial.Serial(serial_port, baud_rate, timeout=2)

try:
    # Send integer data to Arduino
    int_data = -42
    ser.write(str(int_data).encode())
    print("Sent integer data:", int_data)

    # Close serial port
    ser.close()

except Exception as e:
    print("Error:", str(e))
