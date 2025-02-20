import time
import can

bustype = 'socketcan'
channel = 'vcan0'

def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    for i in range(10):
        msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], is_extended_id=True)
        bus.send(msg)

    time.sleep(1)

producer(10)

"""
tetra@debian:~/Github/GachaconSensorDispaly/for_systemd$ python ./test_python_can_send.py 
/home/tetra/Github/GachaconSensorDispaly/for_systemd/./test_python_can_send.py:9: DeprecationWarning: The 'bustype' argument is deprecated since python-can v4.2.0, and scheduled for removal in python-can v5.0.0. Use 'interface' instead.
  bus = can.interface.Bus(channel=channel, bustype=bustype)
SocketcanBus was not properly shut down
"""


