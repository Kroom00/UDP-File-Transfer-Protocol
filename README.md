# UDP File Transfer Protocol

## 1. Introduction

This report details the design and implementation of a UDP-based file transfer protocol. The protocol facilitates reliable and efficient transmission of files between two hosts using the User Datagram Protocol (UDP). The report covers protocol design, message format, network setup, testing procedures, operational manual, technical challenges, and resources utilized during development.

## 2. Protocol Design Explanation

The protocol employs a simple design with key elements:
- Sequence Numbers: Unique sequence numbers for packet ordering.
- Acknowledgments (ACKs): Confirmation of successful packet receipt to enable retransmission in case of loss.

## 3. Message Format Description

Messages have the following format:
- File Information Packet: Contains filename and size.
- Data Packets: Header with sequence number and data size, followed by payload.
- Acknowledgment Packet: Single-byte ACK with sequence number of the last received packet.

## 4. User Manual

### Prerequisites:
- Python installed on the host machine.

### Running the Program:
1. **Receiver Side:**
   - Update `ServerSocket.bind` with receiver's IP address and port in the receiver code.
   - Run receiver script: `python receiver_script.py`

![image](https://github.com/Kroom00/UDP-File-Transfer-Protocol/assets/88386673/7421d6c1-bf84-465e-9326-cfd1e199e7f1)

2. **Sender Side:**
   - Update `receiver_ip` and `file_path` in the sender code.
   - Run sender script: `python sender_script.py`

![image](https://github.com/Kroom00/UDP-File-Transfer-Protocol/assets/88386673/a7d3fbb7-8059-4147-a085-7c3ed1d055b7)

3. **Sender and Receiver output:**

![image](https://github.com/Kroom00/UDP-File-Transfer-Protocol/assets/88386673/e68b047b-e5ba-41bf-bd6c-03dbdf22ea0d)


## 5. Network Setup and Testing

- Both sender and receiver run on the same machine.
- Tested on a local network to simulate real-world conditions.
- Various scenarios, including packet loss and reordering, were simulated for protocol validation.

## 6. Technical Challenges and Solutions

- **Packet Loss Handling:**
  - Challenge: Accurate packet loss simulation.
  - Solution: Introduce random drop probability in sender code and detect lost packets by sequence numbers in receiver code.

- **Timeout and Retransmission:**
  - Challenge: Implement reliable timeout mechanism.
  - Solution: Sender retransmits packets if acknowledgments are not received within specified time.

- **Packet Fragmentation and Reassembly:**
  - Challenge: Handle large files fragmentation and reassembly.
  - Solution: Sender splits files into manageable packets; receiver reassembles packets by sequence numbers.

- **Network Congestion and Flow Control:**
  - Challenge: Prevent network congestion and sender overwhelming receiver.
  - Solution: Implement flow control where sender waits for acknowledgment before sending next packet.

## 7. Conclusion

The UDP file transfer protocol offers a reliable and efficient solution for file transmission over local networks. Overcoming challenges related to packet loss, reordering, fragmentation, and flow control, the protocol provides robust data transmission. The simplicity of design, combined with effective error handling, makes it suitable for lightweight yet reliable file transfers. Its adaptability to varying network conditions enhances its versatility and applicability in diverse environments.
