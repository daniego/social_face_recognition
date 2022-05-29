from flask import *
from threading import Thread
import os
from streamer import streamer


# Create flask app and global pi 'thing' object.
app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG', True)

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
        # thread = Thread(target=streamer, args=(duration,))
        thread = Thread(target=streamer)
        thread.daemon = True
        thread.start()
        return jsonify({'thread_name': str(thread.name),
                    'started': True})

    elif service == 'face_recognition/start':
        return "False"
    elif service == 'driver/mobile':
        return render_template('driver-mobile.html', switch=switch)
    else:
        return ('Unknow request', 400)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8089, debug=True, threaded=True)
    # app.run(host='0.0.0.0', port=8089, debug=False, threaded=True)
