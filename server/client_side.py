import socket
import json
import time

vitals = {
    'heartbeat': [],
    'temperature': [],
    'breathing': [],
    'heartbeat_minmax': [0, 0],
    'temperature_minmax': [0, 0],
    'breathing_minmax': [0, 0]
}

def irregularity(vital):
    state = False
    if vitals[vital][-1] > vitals[vital + '_minmax'][0] + 10 or vitals[vital][-1] < vitals[vital + '_minmax'][1] - 10:
        state = True
    if vitals[vital + '_minmax'] == [0, 0]:
        state = False
        vitals[vital + '_minmax'] = [vitals[vital][-1]] * 2
    elif vitals[vital][-1] > vitals[vital + '_minmax'][1]: vitals[vital + '_minmax'][1] = vitals[vital][-1]
    elif vitals[vital][-1] < vitals[vital + '_minmax'][0]: vitals[vital + '_minmax'][0] = vitals[vital][-1]
    return state

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    start_time = time.time()

    try:
        while True:
            response = client.recv(4096)
            if not response:
                break
            report = json.loads(response.decode('utf-8'))
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
        client.close()

if __name__ == "__main__":
    main()
