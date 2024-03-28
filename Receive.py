import socket
import random
import time
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set the timeout and create a UDP socket
TimeOut = 10  # Increased timeout value to 10 seconds
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    ServerSocket.bind(('192.168.1.26', 6500))  # Updated IP address and port
except socket.error as e:
    logging.error("Error binding socket: %s", e)
    exit(1)
ServerSocket.settimeout(TimeOut)

# Define loss rate, buffer, and other variables for statistics
lossRate = 0
Buffer = []
data = bytearray()
NumberofTransmittedACKs = 0
NumberofTransmittedACKsBytes = 0
NumberofLostPackets = 0
NumberofReceivedBytes = 0
FileID = 0
file_name = None
file_size = None
addr = None  # Initialize addr variable

# Main loop for receiving and processing packets
while True:
    try:
        if file_name is None:
            file_info_bytes, addr = ServerSocket.recvfrom(500)
            file_info = file_info_bytes.split(b'\n')
            file_name = file_info[0].decode('utf-8')
            file_size = int(file_info[1])
            print(f"Received file info: Name - {file_name}, Size - {file_size} bytes")

        message, _ = ServerSocket.recvfrom(1024)  # Use _ for unused variable

        # Simulate packet loss based on loss rate
        lossFlag = random.uniform(0, 100)

        if lossFlag <= lossRate:
            message = False
            NumberofLostPackets += 1

        while message:
            packet_sequence = int.from_bytes(message[:4], byteorder='big', signed=False)
            packet_data = message[4:]

            if packet_sequence == FileID:
                Buffer.append(packet_data)
                FileID += 1
                NumberofReceivedBytes += len(packet_data)
                NumberofTransmittedACKs += 1
                NumberofTransmittedACKsBytes += 4

            while Buffer and Buffer[0]:
                data += Buffer.pop(0)

            ServerSocket.settimeout(TimeOut)
            message, _ = ServerSocket.recvfrom(1024)  # Use _ for unused variable
    except socket.timeout:
        if addr is not None:
            if Buffer:
                ServerSocket.sendto(bytes([FileID - 1]), addr)
            else:
                ServerSocket.sendto(bytes([FileID]), addr)
        else:
            logging.error("Timeout error: No data received.")
        if len(Buffer) == 0:
            break

# Save the received data to a file and print its content
if data and file_name:
    with open(file_name, 'wb') as file:
        file.write(data)
    logging.info("File received and saved successfully.")
    with open(file_name, 'r') as file:
        print("File content:")
        print(file.read())
else:
    logging.error("No data received or file name not specified.")

# Print statistics
logging.info("Number of lost packets: %d", NumberofLostPackets)
logging.info("Number of received bytes: %d", NumberofReceivedBytes)
logging.info("Number of transmitted ACKs: %d", NumberofTransmittedACKs)
logging.info("Number of transmitted ACKs bytes: %d", NumberofTransmittedACKsBytes)
