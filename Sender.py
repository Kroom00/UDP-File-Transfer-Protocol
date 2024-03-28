import socket
import time
import os
import random

# Set the timeout and create a UDP socket
TimeOut = 4
SenderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SenderSocket.settimeout(TimeOut)

# Define maximum segment size
MAX_SEGMENT_SIZE = 500

# Update the receiver IP and file path
receiver_ip = "192.168.1.26"  # Updated IP address
receiver_port = 6500  # Specify the receiver port
file_path = r"C:\Users\ginta\OneDrive\Desktop\projectphase2\www.txt.txt"  # Updated file path

# Get file information
file_size = os.path.getsize(file_path)
file_name = os.path.basename(file_path)

# Split the file into segments
segments = []
with open(file_path, "rb") as file:
    while True:
        data = file.read(MAX_SEGMENT_SIZE)
        if not data:
            break
        segments.append(data)

# Send file information (file name and size) to the receiver
info_packet = file_name.encode('utf-8') + b'\n' + str(file_size).encode('utf-8')
SenderSocket.sendto(info_packet, (receiver_ip, receiver_port))

# Initialize sequence number
sequence_number = 0

# Initialize statistics variables
number_of_sent_packets = 0
number_of_retransmissions = 0
start_time = time.time()

# Function to simulate unreliable channel and packet loss
def simulate_unreliable_channel(packet, drop_probability):
    if random.random() < drop_probability:
        # Drop the packet
        print("Packet dropped!")
        return None
    else:
        # Send the packet
        return packet

# Main loop for sending packets
while sequence_number < len(segments):
    data = segments[sequence_number]

    # Prepare packet with header (sequence number + data size + data)
    packet = sequence_number.to_bytes(4, byteorder='big') + len(data).to_bytes(4, byteorder='big') + data

    # Simulate unreliable channel with packet loss probability of 0.3
    packet = simulate_unreliable_channel(packet, 0.3)

    if packet is not None:
        # Send packet to receiver
        SenderSocket.sendto(packet, (receiver_ip, receiver_port))
        number_of_sent_packets += 1

    try:
        # Wait for acknowledgment
        ack_packet, _ = SenderSocket.recvfrom(4)
        
        try:
            ack_sequence_number = int.from_bytes(ack_packet, byteorder='big')
            
            if ack_sequence_number == sequence_number:
                # Acknowledgment received, move to the next sequence number
                sequence_number += 1
            else:
                # Retransmit the current packet
                number_of_retransmissions += 1
                
        except ValueError:
            print("Received invalid acknowledgment packet:", ack_packet)
            continue  # Skip to the next iteration of the loop
            
    except socket.timeout:
        # Retransmit the current packet
        number_of_retransmissions += 1


# Calculate statistics
end_time = time.time()
elapsed_time = end_time - start_time
throughput = file_size / elapsed_time if number_of_sent_packets > 0 else 0
average_delay = elapsed_time / number_of_sent_packets if number_of_sent_packets > 0 else 0


# Print statistics
print("------------------------------------------------")
print(f"Number of Sent Packets: {number_of_sent_packets}")
print(f"Number of Retransmissions: {number_of_retransmissions}")
print(f"Throughput: {throughput} bytes/second")
print(f"Average Delay: {average_delay} seconds")
print("------------------------------------------------")

# Close the socket
SenderSocket.close()
