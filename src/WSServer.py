import asyncio
import time

import websockets
import threading
import json

from LeapFrame import LeapFrame


def read_file(name='../gestures/pinch-57fps.json'): return open(name, "r").read()


def read_json(data=read_file()): return json.loads(data)


def write_file(data, name='../gestures/pinch-57fps-copy.json'):
    with open(name, 'w') as outfile:
        outfile.write(data)
        outfile.close()


leap_data = read_json()
leap_data2 = read_json(read_file('../gestures/wave-120fps.json'))

# first record
metadata1 = leap_data['metadata']
print('loaded meta 1: ' + str(metadata1))
frames1 = leap_data['frames']
print('loaded frames 1: ' + str(frames1[1]))

# second record
metadata2 = leap_data2['metadata']
print('loaded meta 2: ' + str(metadata2))
frames2 = leap_data2['frames']
print('loaded frames 2: ' + str(frames2[1]))


class WSServer:

    def __init__(self):
        self.connected = False
        self.frames = None
        self.i_frame = 0
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(self.hello, 'localhost', 6437)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def next_track(self):
        self.i_frame = 0
        if self.frames is None or self.frames is frames2:
            self.frames = frames1
        else:
            self.frames = frames2

    def get_next_frame(self):
        if self.i_frame < len(self.frames) - 1:
            self.i_frame += 1
            return LeapFrame(json_data=self.frames[self.i_frame]).to_json()
        else:
            self.next_track()
            print("next track")
            return self.get_next_frame()

    async def hello(self, websocket, path):
        print("connecting")

        async def disconnect():
            self.next_track()
            websocket.close()
            print("disconnected")

        try:
            self.i_frame = 0
            self.frames = frames1
            await websocket.send('{"serviceVersion":"2.3.1+33747", "version":6}')
            await websocket.send('{"event": {"state": { "attached": true, "id": "NNNNNNNNNNN", "streaming": true,'
                                 '"type": "peripheral" },"type": "deviceEvent"}}')

            self.connected = True
            while self.connected:
                payload = self.get_next_frame()
                await websocket.send(payload)
                time.sleep(0.01)
                # print(payload)
        except websockets.exceptions.ConnectionClosed:
            await disconnect()


def create_in_new_thread():
    serv_thread = threading.Thread(target=WSServer)
    serv_thread.start()
