import argparse
from math import sin, cos, radians, sqrt
import threading
import collections
import time

from pythonosc import dispatcher
from pythonosc import osc_server

accelerations = collections.deque(maxlen=100)
current_acceleration = 0
cancel = False

def receive_values(unused_addr, *args):
     global accelerations
     x, y, z = gravity_compensate(args[14:18], args[0:3])
     #print(x, y, z)
     accelerations.append({x, y, z})

def gravity_compensate(q, acc):
     g = [0.0, 0.0, 0.0]
     
     # get expected direction of gravity
     g[0] = 2 * (q[1] * q[3] - q[0] * q[2])
     g[1] = 2 * (q[0] * q[1] + q[2] * q[3])
     g[2] = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]
     
     # compensate accelerometer readings with the expected direction of gravity
     return (acc[0] - g[0])*9.8, (acc[1] - g[1])*9.8, (acc[2] - g[2])*9.8

def filter_acceleration():
     global cancel
     global current_acceleration
     global accelerations
     while(not cancel):
          current_acceleration = 0
          for acc in accelerations:
               aux_acc = 0
               for acc_coord in acc:
                    aux_acc += acc_coord**2
               current_acceleration += sqrt(aux_acc) / 100
          print('Acc: ', current_acceleration)

if __name__ == "__main__":
     try:
          parser = argparse.ArgumentParser()
          parser.add_argument("--ip", default="192.168.1.100", help="The ip to listen on")
          parser.add_argument("--port", type=int, default=8888, help="The port to listen on")
          args = parser.parse_args()

          dispatcher = dispatcher.Dispatcher()
          dispatcher.map("/*/raw", receive_values)

          current_acceleration = 0

          x = threading.Thread(target=filter_acceleration)
          x.start()

          server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
          print("Serving on {}".format(server.server_address))
          server.serve_forever()
     except KeyboardInterrupt:
          cancel = 1
          quit()