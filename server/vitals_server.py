from flask import Flask, jsonify
from threading import Thread
import time
import json
import random
import select

# Initial values centered around typical baby vitals
initial_bpm = 120
initial_temp = 98
breathe_state = "Breathe in"

current_bpm = initial_bpm
current_temp = initial_temp

vitals = []
start_time = time.time()

app = Flask(__name__)
#data = {"value": 0}

def update_data():
    while True:
        #print(vitals)
        global current_bpm, current_temp, breathe_state
        # Randomize BPM by +-3 beats, keeping it within a realistic range
        current_bpm = max(100, min(160, initial_bpm + random.randint(-3, 3)))
        
        # Randomize temperature by +-0.05 degrees, keeping it within a realistic range
        current_temp = max(60, min(140, initial_temp + random.uniform(-15, 15)))
        
        # Switch breathing state
        breathe_state = "Breathe out" if breathe_state == "Breathe in" else "Breathe in"

        if random.randint(0, 9) == 0:
            vitals.append([round(time.time() - start_time), current_bpm, current_temp, current_bpm])
        else:
            vitals.append([round(time.time() - start_time), current_bpm, current_temp, None])
        time.sleep(1)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(vitals)

if __name__ == '__main__':
    # Start the data update thread
    updater = Thread(target=update_data)
    updater.daemon = True
    updater.start()
    
    # Start the Flask server
    app.run(port=9999)