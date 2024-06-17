import socket
from datetime import datetime
import re
from http import HTTPStatus


def handler(connection, address):
    with connection:
        print("Got connection:", connection, address)
        while True:
            data = connection.recv(1024)
            print("Got data:", data)
            if not data:
                break
            if '\r\n\r\n'.encode() in data:
                break

        if data:
            request_data = data.decode().strip().split('\r\n')

            request_method_and_status = [item for item in request_data[0].split()]
            request_status = re.search(r'status=(\d+)', request_method_and_status[1])
            if request_status:
                if len(request_status.group(1)) == 3:
                    for status in list(HTTPStatus):
                        if int(request_status.group(1)) == status.value:
                            response_status = f'{status.value} {status.phrase}'
                        elif int(request_status.group(1)) not in [status.value for status in list(HTTPStatus)]:
                            response_status = f'{HTTPStatus.OK} {HTTPStatus.OK.phrase}'
                else:
                    response_status = f'{HTTPStatus.OK} {HTTPStatus.OK.phrase}'
            else:
                response_status = f'{HTTPStatus.OK} {HTTPStatus.OK.phrase}'

            response_head = (
                f"HTTP/1.1 {response_status}\r\n"
                f"Server: EchoServer\r\n"
                f"Date: {datetime.today().isoformat('-', 'seconds')}\r\n"
                f"Content-Type: text/html; charset=UTF-8\r\n"
                f"\r\n"
            )
            response_body = (
                    f'Request Method: {request_method_and_status[0]}\r\n'
                    f'Request Source: {connection.getpeername()}\r\n'
                    f'Response Status: {response_status}\r\n'
                    '\r\n'
                    'Request headers:</h4>\r\n' + '\r\n'.join([f"{item}" for item in request_data])
            )
            connection.send(
                ''.join(response_head).encode()
                + response_body.encode()
                + f'\r\n'.encode()
            )


with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen()
    while True:
        connection_1, address_1 = server_socket.accept()
        handler(connection_1, address_1)
