import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("192.168.1.51", 1234))
    s.listen()
    conn, addr = s.accept()
    with conn:
        # while True:
        data = conn.recv(3*4)
        print("New data!")
        counter = int.from_bytes(data[:4], byteorder="big")
        x = int.from_bytes(data[4:8], byteorder="big")
        y = int.from_bytes(data[8:12], byteorder="big")
        print(counter)
        print(x)
        print(y)
