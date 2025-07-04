import serial

# Cambia 'COM3' por el puerto de tu Arduino.
# En Linux probablemente sea '/dev/ttyUSB0' o '/dev/ttyACM0'
puerto = '/dev/ttyUSB0'
baudrate = 9600

# Abre la conexión serial
ser = serial.Serial(puerto, baudrate, timeout=1)

print("Escuchando datos del Arduino...")

try:
    while True:
        # Lee una línea del puerto serial
        linea = ser.readline().decode('utf-8').strip()
        if linea:
            print(f"Arduino dice: {linea}")
except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
finally:
    ser.close()
