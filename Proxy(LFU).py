import socket
import ssl
import requests
import threading
from Caching import LRUCache, LFUCache
import sys

def handle_client_request(client_socket, cache):
    # Receive the request from the client
    request = client_socket.recv(4096)
    method = None
    url = None
    protocol = None
    url_parts = None
    # Parse the request
    try:
        method, url, protocol = request.split(b' ', 2)
        url_parts = url.split(b'://', 1)
    
    # Check that the URL is properly formatted
        if len(url_parts) < 2:
            client_socket.close()
            return
        scheme = url_parts[0]
        path = url_parts[1]
        
        if path in cache:
            print(path, ' ( FOUND IN LFU CACHE )')
            print('\n')
            response = cache.__getitem__(path)
        else:

    # Send the request using the Requests library
            print(path, ' ( REQUESTING FROM ORIGINAL SERVER )')
            print('\n')
            response = requests.request(method.decode(), f"{scheme.decode()}://{path.decode()}")
            cache.__setitem__(path, response)
        response_bytes = response.content
        client_socket.sendall(response_bytes)
            
            
    # Forward the response to the client
    except Exception as e:
        pass

    # Close the client socket
    client_socket.close()





def proxy_server(proxyhost, proxyport, cache):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a specific address and port
    server_socket.bind((proxyhost, proxyport))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Proxy server listening on {proxyhost}:{proxyport}...")

    while True:
        # Wait for a client connection
        client_socket, client_address = server_socket.accept()

        # Create a new thread to handle the client request
        t = threading.Thread(target=handle_client_request, args=(client_socket, cache))
        t.start()


if __name__ == '__main__':
    proxyhost = 'localhost'
    proxyport = int(sys.argv[1])
    cache = LFUCache(1000)
    proxy_server(proxyhost, proxyport, cache)
