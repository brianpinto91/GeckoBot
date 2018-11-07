#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 15:18:21 2018
@author: bianca
"""

import io
import socket
import struct
import time
try:
    from PIL import Image
except ImportError:
    print 'Cannot import PIL'
from subprocess import call


def start_server(ip='134.28.136.49'):
    cmd = 'ssh -i ~/.ssh/BBB_key pi@{} nohup python /home/pi/Git/GeckoBot/Code/Src/Visual/PiCamera/server.py &'.format(ip)
    call(cmd, shell=True)


class ClientSocket(object):
    def __init__(self, ip='134.28.136.49'):
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        self.client_socket = socket.socket()
        self.client_socket.connect((ip, 8000))

        # Make a file-like object out of the connection
        self.connection = self.client_socket.makefile('wb')

    def make_image(self, filename='test', folder='/home/pi/testimages/',
                   imgformat='.jpg'):
        self.client_socket.sendall('m{}'.format(folder+filename+imgformat))

    def make_video(self, filename):
        
        self.client_socket.sendall('v{}'.format(filename))

    def get_image(self, filename='test'):
        self.client_socket.sendall('getImage')
        try:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                IOError('Image length Issue')
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(self.connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            print('Image is %dx%d' % image.size)
            image.save('{}.jpg'.format(filename), 'JPEG')
        except:
            print 'transmission failed'

    def close(self):
        self.client_socket.sendall('Exit')
        self.connection.close()
        self.client_socket.close()


if __name__ == "__main__":
    sock = ClientSocket()
    for foo in range(3):
        sock.get_image('image{}'.format(foo))
        time.sleep(2)
        sock.close()
