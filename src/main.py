from flask import *
from threading import Thread
import os
from streamer import streamer


# Create flask app and global pi 'thing' object.
app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG', True)

# def streamer():
#     from flask_opencv_streamer.streamer import Streamer
#     import cv2
#
#     port = 3030
#     require_login = False
#     streamer = Streamer(port, require_login)
#
#     # Open video device 0
#     video_capture = cv2.VideoCapture(0)
#
#     while True:
#         _, frame = video_capture.read()
#
#         streamer.update_frame(frame)
#
#         if not streamer.is_streaming:
#             print("Start streaming")
#             streamer.start_streaming()
#
#             from pprint import pprint
#             pprint(streamer)
#
#         cv2.waitKey(30)
#
#     # import socket
#     # # A TCP based echo server
#     # echoSocket = socket.socket();
#     # # Bind the IP address and the port number
#     # echoSocket.bind(("127.0.0.1", 3030));
#     # # Listen for incoming connections
#     # echoSocket.listen();
#     # # Start accepting client connections
#     # while(True):
#     #     (clientSocket, clientAddress) = echoSocket.accept();
#     #     # Handle one request from client
#     #     while(True):
#     #         data = clientSocket.recv(1024);
#     #         print("At Server: %s"%data);
#     #         if(data!=b''):
#     #             # Send back what you received
#     #             clientSocket.send(data);
#     #             break;

# Define app routes.
# Index route renders the main HTML page.
@app.route("/")
def index():
    return render_template('home.html')

@app.route("/v1/<path:service>", methods=['GET'])
def view(service):
    if service == 'state/battery':
        BatteryState = getBatteryState()
        return (BatteryState, 200)
    elif service == 'face_recognition/start':


        print('sas')
        # thread = Thread(target=streamer, args=(duration,))
        thread2 = Thread(target=streamer)
        thread2.daemon = True
        thread2.start()
        return jsonify({'thread_name': str(thread2.name),
                    'started': True})
        # streamer()
        # return "True"
    elif service == 'face_recognition/start':
        return "False"
    elif service == 'driver/mobile':
        return render_template('driver-mobile.html', switch=switch)
    else:
        return ('Unknow request', 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8089, debug=True, threaded=True)
    # app.run(host='0.0.0.0', port=8089, debug=False, threaded=True)
