from flask import Flask, jsonify
from flask_cors import CORS
import random
import socket
import json
import time
import select
import requests

app = Flask(__name__)
CORS(app)
client = None

'''vitals = {
    'time': [],
    'heartbeat': [],
    'temperature': [],
    'breathing': [],
    'heartbeat_minmax': [0, 0],
    'temperature_minmax': [0, 0],
    'breathing_minmax': [0, 0]
}'''

@app.route('/data')
def get_data():
    # Generate some random data for the line chart
    #data = []

    response = requests.get('http://localhost:9999/data')
    #print(response.json())
    #vitals = json.loads(response.json())
    vitals = response.json()
    # if response.status_code == 200:
    #     print(response.json())
    # else:
    #     print('Failed to fetch data')



    data = [["Time", "BPM", "Temperature", "Point"]] + [
        #[float(vitals['time'][i]), float(vitals['heartbeat'][i], float(vitals['temperature'][i]))] for i in len(range(vitals['time']))
        [float(vital[0]), float(vital[1]), float(vital[2]), None if vital[3] == None else float(vital[3])] for vital in vitals
    ]
    #print(data)
    return jsonify(data)
    #return data

def irregularity(vitals, vital):
    state = False
    if vitals[vital][-1] > vitals[vital + '_minmax'][0] + 10 or vitals[vital][-1] < vitals[vital + '_minmax'][1] - 10:
        state = True
    if vitals[vital + '_minmax'] == [0, 0]:
        state = False
        vitals[vital + '_minmax'] = [vitals[vital][-1]] * 2
    elif vitals[vital][-1] > vitals[vital + '_minmax'][1]: vitals[vital + '_minmax'][1] = vitals[vital][-1]
    elif vitals[vital][-1] < vitals[vital + '_minmax'][0]: vitals[vital + '_minmax'][0] = vitals[vital][-1]
    return state


    #start_time = time.time()

    
'''
    try:
        while True:
            ready = select.select([client], [], [], 5)
            response = None
            if ready[0]:
                response = client.recv(4096)
            if not response:
                break
            report = json.loads(response.decode('utf-8'))
            vitals['time'].append(time.time() - start_time)
            vitals['heartbeat'].append(float(report['BPM']))
            vitals['temperature'].append(float(report['Temperature']))
            vitals['breathing'].append(float(report['Breathing']))
            #irregularity('heartbeat')
            #irregularity('temperature')
            #irregularity('breathing')

            print(time.time() - start_time, {
                'heartbeat': irregularity('heartbeat'),
                'temperature': irregularity('temperature'),
                'breathing': irregularity('breathing')
            })
            #print(response.decode('utf-8'))
            #print(json.dumps(vitals), time.time() - start_time)
    finally:
        client.close()'''


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    #while input():
        #print(json.loads(get_data()))
    #    print(get_data())
    app.run(debug=True, port=1601)