import socket
import random
import http

HOST = "127.0.0.1"
PORT = random.randint(10000, 20000)

with socket.socket() as serv_socket:
    print(f"Connecting to {HOST}:{PORT}")
    serv_socket.bind((HOST, PORT))
    serv_socket.listen()

    while True:
        print("Waiting request...")
        connection, address = serv_socket.accept()
        print("Connection from", address)

        data = connection.recv(1024)
        print(f"Received data: \n{data}\n")
        data = data.decode().strip()

        status_value = 200
        status_phrase = "OK"
        try:
            status = data.split()[1].split("/?status=")
            if len(status) == 2:
                status_code = int(status[1].split()[0])
                status = http.HTTPStatus(status_code)
                status_value = status_code
                status_phrase = status.phrase
        except (ValueError, IndexError):
            pass

        status_line = f"{data.split()[2]} {status_value} {status_phrase}"
        response = "\r\n".join(data.split("\r\n")[1:])

        connection.send(f"{status_line}\r\n\r\n"
                        f"\nRequest Method: {data.split()[0]}"
                        f"\nRequest Source: {address}"
                        f"\nResponse Status: {status_value} {status_phrase}\r\n"
                        f"\n{response}".encode())
        connection.close()
