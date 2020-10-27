import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("192.168.1.51", 1234))
    counter = int(1).to_bytes(4, byteorder="big")
    x = int(387).to_bytes(4, byteorder="big")
    y = int(1298).to_bytes(4, byteorder="big")
    data = bytes(counter + x + y)
    s.send(data)
