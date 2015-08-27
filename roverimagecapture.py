import numpy as np
import scipy
import scipy.io as sio
import StringIO
import cv2
import matplotlib.pyplot as plt
import time
from string import ascii_lowercase, ascii_uppercase
from datetime import date
from random import choice

from rover import Rover20


class MPCR_Rover_Image(Rover20):
    def __init__(self):
        Rover20.__init__(self)
        self.currentImage = None
        self.quit = False
        self.action_choice = 1
        self.action_labels = ['left', 'forward', 'right', 'backward']
        self.action_vectors = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        self.data = np.ones(240 * 320 + 4)

    def mleft(self):
        self.setTreads(-1, 1)
        time.sleep(.1)
        self.setTreads(0, 0)

    def mforward(self):
        self.setTreads(1, 1)
        time.sleep(.1)
        self.setTreads(0, 0)

    def mright(self):
        self.setTreads(1, -1)
        time.sleep(.1)
        self.setTreads(0, 0)

    def mbackward(self):
        self.setTreads(-1, -1)
        time.sleep(.1)
        self.setTreads(0, 0)

    # called by Rover20, acts as main loop
    def processVideo(self, jpegbytes, timestamp_10msec):
        # 240,320

        self.currentImage = cv2.imdecode(np.asarray(bytearray(jpegbytes), dtype=np.uint8), 0)

        self.pattern = np.reshape(self.currentImage, (240 * 320))

        self.action_choice = input("Enter 1 for left, 2 for forward, 3 for right, 4 for reverse, 5 for save and quit)")

        self.action_choice = self.action_choice - 1

        if self.action_choice == 4:
            datasave = {}
            datasave['data'] = self.data
            uniqueKey = ''.join(choice(ascii_lowercase + ascii_uppercase) for _ in range(5))
            uniqueKey = 'test'
            sio.savemat('MPCR_Rover_Images_' + uniqueKey + '.mat', datasave)
            print 'File Saved: MPCR_Rover_Images_' + uniqueKey + '_.mat'
            self.quit = True
            return

        action_pixel = np.zeros(4)

        action_pixel[self.action_choice] = 1

        self.pattern = np.concatenate((self.pattern, action_pixel))

        self.data = np.column_stack((self.data, self.pattern))

        print np.asarray(self.data).shape[1]

        if self.action_choice == 0:
            self.mleft()
        elif self.action_choice == 1:
            self.mforward()
        elif self.action_choice == 2:
            self.mright()
        elif self.action_choice == 3:
            self.mbackward()


def main():
    rover = MPCR_Rover_Image()

    while not rover.quit:
        pass

    rover.close()


if __name__ == '__main__':
    main()
