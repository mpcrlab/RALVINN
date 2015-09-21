########################################################
# ------------------------------------------------------#
#
# Machine Perception and Cognitive Robotics Laboratory
# Center for Complex Systems and Brain Sciences
#           Florida Atlantic University
#
# ------------------------------------------------------#
########################################################
# ------------------------------------------------------#
#
# Distributed ALVINN, See:
# Pomerleau, Dean A. Alvinn:
# An autonomous land vehicle in a neural network.
# No. AIP-77. Carnegie-Mellon Univ Pittsburgh Pa
# Artificial Intelligence And Psychology Project, 1989.
#
# ------------------------------------------------------#
########################################################

import pygame
from pygame.locals import *
from time import sleep
from datetime import date
from random import choice
from string import ascii_lowercase, ascii_uppercase
import threading
import cStringIO
import numpy as np
from scipy.misc import imresize
from scipy import ndimage as ndi
from af import *

from rover import Rover20


class roverShell(Rover20):
    def __init__(self):
        Rover20.__init__(self)
        self.quit = False
        self.lock = threading.Lock()

        self.treads = [0, 0]
        self.nn_treads = [0, 0]
        self.currentImage = None
        self.peripherals = {'lights': False, 'stealth': False, \
                            'detect': True, 'camera': 0}

        self.action_choice = 1
        self.action_labels = ['forward', 'backward', 'left', 'right']
        self.action_vectors_motor = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
        self.action_vectors_neuro = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        self.n1 = 32 * 24 * 3
        self.n2 = 50
        self.n3 = 4

        self.w1 = 0.0001 * np.random.random((self.n1 + 1, self.n2))
        self.w2 = 0.01 * np.random.random((self.n2 + 1, self.n3))

        self.dw1 = np.zeros(self.w1.shape)
        self.dw2 = np.zeros(self.w2.shape)

        self.L1 = 0.001
        self.L2 = 0.01
        self.M = .5  # new value

    # main loop
    def processVideo(self, jpegbytes, timestamp_10msec):
        self.lock.acquire()
        if self.peripherals['detect']:
            self.processImage(jpegbytes)
            self.currentImage = jpegbytes
        else:
            self.currentImage = jpegbytes
        self.lock.release()
        self.setTreads(self.treads[0], self.treads[1])
        self.setPeripherals()
        if self.quit:
            self.close()

    # openCV operations
    def processImage(self, jpegbytes):

        self.currentImage = imresize(
            pygame.surfarray.array3d(pygame.image.load(cStringIO.StringIO(jpegbytes), 'tmp.jpg').convert()), (32, 24))

        self.currentImage = ndi.gaussian_filter(self.currentImage, .5) - ndi.gaussian_filter(self.currentImage, 1)

        self.currentImage = self.currentImage / 255.0

        self.pattern = np.tile(np.reshape(self.currentImage, (32 * 24 * 3)), (64, 1))

        self.pattern = self.pattern + 0.001 * (1 - np.random.random((self.pattern.shape[0], self.pattern.shape[1])))

        self.bias = np.ones((self.pattern.shape[0], 1))

        self.pattern = np.concatenate((self.pattern, self.bias), axis=1)

        self.act1 = np.concatenate((np.squeeze(np.array(af(np.dot(self.pattern, self.w1)))), self.bias), axis=1)

        self.act2 = np.squeeze(np.array(af(np.dot(self.act1, self.w2))))

        self.act22 = 0 * self.act2

        for i in range(self.act2.shape[0]):
            self.act22[i, np.argmax(self.act2[i, :])] = 1

        self.nn_treads = self.action_vectors_motor[np.argmax(np.sum(self.act22, axis=0))]

        print self.nn_treads

        if np.sum(np.abs(self.treads)):

            for i in range(np.asarray(self.action_vectors_motor).shape[0]):
                if self.action_vectors_motor[i] == self.treads:
                    break

            self.category = np.tile(self.action_vectors_neuro[i], (self.pattern.shape[0], 1))

            self.error = self.category - self.act2

            self.sse = np.power(self.error, 2).sum

            self.delta_w2 = self.error * self.act2 * (1 - self.act2)

            self.delta_w1 = np.dot(self.delta_w2, self.w2.transpose()) * self.act1 * (1 - self.act1)

            self.delta_w1 = np.delete(self.delta_w1, -1, 1)

            self.dw1 = np.dot(self.L1, np.dot(self.pattern.transpose(), self.delta_w1)) + self.M * self.dw1
            self.dw2 = np.dot(self.L2, np.dot(self.act1.transpose(), self.delta_w2)) + self.M * self.dw2
            self.w1 = self.w1 + self.dw1
            self.w2 = self.w2 + self.dw2

            self.w1 = self.w1 + 0.0001 * (-0.5 + np.random.random((self.w1.shape[0], self.w1.shape[1]))) # increase random Value
            self.w2 = self.w2 + 0.0001 * (-0.5 + np.random.random((self.w2.shape[0], self.w2.shape[1]))) # increase random Value

    # camera features
    def setPeripherals(self):
        if self.peripherals['lights']:
            self.turnLightsOn()
        else:
            self.turnLightsOff()

        if self.peripherals['stealth']:
            self.turnStealthOn()
        else:
            self.turnStealthOff()

        if self.peripherals['camera'] in (-1, 0, 1):
            self.moveCameraVertical(self.peripherals['camera'])
        else:
            self.peripherals['camera'] = 0
