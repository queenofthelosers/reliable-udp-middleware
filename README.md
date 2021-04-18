# Reliable UDP Middleware

A simple application layer middleware protocol written in Python that implements reliable communication over UDP. The implementation of the protocol has been tested using a simple file transfer client and server application that supports a variety of file formats. The Netem tool was used to simulate various network conditions and the performance of the protocol was evaluated.



## Instructions for use
Run the server and the client on separate terminals. The file is transferred from the server directory to the client directory. Provide the file name as a command-line argument to the server program. The client program takes as command-line arguments, the network condition and the value by which its altered.

    cd server && python3 server.py <filename>

    cd client && python3 client.py <param> <val>



## Changes made to the original protocol


|                |Phase 1|Phase 2|
|----------------|-------------------------------|-----------------------------|
|1|Sender and Receiver window were assumed to be of the same size as the buffer (for in-order delivery).           |The Buffer size is taken to be of smaller size (than sender/receiver window) since we are transferring only the correct inorder packet (only 1 packet) to the application.            |
|2|Data was assumed to be sent as chunks of size 16 bits.            |Data is sent as chunks of 2048 bytes.      |
|3|FIN control bit was used.|FIN control bit was not used in the implementation.|
|4|CHK control bit was intended to be used to identify if the checksum was only for the header or both header and data            |CHK control bit was used to identify if the packet received is a data / SYN segment or a ACK/NAK/KAL segment.         |
|5|The packet structure for various types of segments were assumed to be different.            |The packet structure remains the same for all different segment types and redundant header fields are dropped from the packet structure.         |
|6|The connection establishment parameters are passed through the SYN segment to the server.            |The connection establishment parameters are assumed to be known to both the client and the server before the file transfer.         |

