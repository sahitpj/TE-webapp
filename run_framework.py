from app import app_flask

import socket    
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)  

# app_flask.run(debug=True)
if __name__ == "__main__":
    app_flask.run(host=IPAddr)
