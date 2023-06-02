import requests

from threading import Thread

from http.server import BaseHTTPRequestHandler, HTTPServer

import time

import signal


session = requests.Session()

host_name = "localhost"
server_port = 8080

stop = 0



# sources: https://pythonbasics.org/webserver/ and https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7 
class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode('utf-8') # <--- Gets the data itself
        post_data = post_data.split("&")

        temp = {}

        for pair in post_data:
            key, value = pair.split("=")
            temp[key] = value
        
        post_data = temp
        print(post_data)

    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            # Clean-up server (close socket, etc.)
            self.server_close()

# initialize web server
web_server = HTTPServer((host_name, server_port), MyServer)

# Arduino waits for signal from the server
def receive_loop():
    print("Sensor started at http://%s:%s" % (host_name, server_port))

    web_server.serve_forever()

# Arduino sends data to server
def send_loop():
    while not (stop):
        tds = 12
        cond = 34
        pH = 56

        post_data = {'tds' : tds, 'cond' : cond, 'pH' : pH}

        # sensor POST request
        session.post('http://localhost:8000/sensor', data=post_data)
        print("sensor reading sent")
        time.sleep(5)    

if __name__ == "__main__":        

    username = 'serge'
    password = '123'
    port = server_port

    post_data = {'username': username, 'password' : password, 'port' : port}

    # sign in POST request
    session.post('http://localhost:8000/signin', data=post_data)

    send_thread = Thread(target=send_loop)
    rcv_thread = Thread(target=receive_loop)

    try:
        send_thread.start()
        rcv_thread.start()
        while True:
            pass
    except KeyboardInterrupt:
        pass

    stop = 1 # Set stop signal
    web_server.shutdown() # Shut down server

    send_thread.join()
    rcv_thread.join()
    print("program terminated")