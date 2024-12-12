import socket
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def whois(query):
    try:
        response = get_whois(query).format(query)
        return response
    except Exception as e:
        logging.error(f"Error processing WHOIS query: {e}")
        return "Internal server error"

def main():
    host = '0.0.0.0'
    port = 43

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    logging.info(f"WHOIS Server Started, port: {port}")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            logging.info(f"Received connection from {addr}")

            try:
                with client_socket:
                    client_socket.settimeout(10.0)
                    
                    try:
                        data = client_socket.recv(1024).strip()
                        try:
                            decoded_data = data.decode('utf-8')
                        except UnicodeDecodeError:
                            logging.warning(f"Received invalid UTF-8 data from {addr}: {data}")
                            client_socket.sendall("Invalid request encoding".encode('utf-8'))
                            continue

                        logging.info(f"Request inquiry: {decoded_data}")
                        
                        if not decoded_data:
                            logging.warning("Empty request received")
                            continue

                        response = whois(decoded_data)
                        client_socket.sendall(response.encode('utf-8'))

                    except socket.timeout:
                        logging.warning("Connection timed out")
                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        client_socket.sendall("Internal server error".encode('utf-8'))

            except Exception as e:
                logging.error(f"Error handling client socket: {e}")

        except Exception as e:
            logging.error(f"Error accepting connection: {e}")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.critical(f"Critical error in main loop: {e}")
            import time
            time.sleep(1)
