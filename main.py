import matplotlib.pyplot as plt
from array import array
import numpy as np
import pygame
from pygame.mixer import Sound, get_init, pre_init
import random


class Note(Sound):

    def __init__(self, frequency, volume=.05):
        self.frequency = frequency
        Sound.__init__(self, self.__build_samples(frequency))
        self.set_volume(volume)

    def stop(self):
        Sound.stop(self)

    def plays(self, f):
        self.__init__(f)
        self.play(-1)

    @staticmethod
    def __build_samples(freq):
        period = int(round(get_init()[0] / freq))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


class List:
    def __init__(self, arr=None, size=-1):
        if arr is None and size == -1:
            size = 50
        pre_init(44100, -16, 1, 1024)
        pygame.init()
        self.sound = Note(440)
        self.frequency_ofs = 300
        self.frequency_range = 600

        if size < 1:
            self.list = arr
        else:
            self.list = np.linspace(0, size-1, num=size)

        plt.ion()
        plt.rcParams['toolbar'] = 'None'

        self.fig = plt.figure()
        self.max = max(self.list)
        self.max_line = int(round(self.max*1.1))
        self.min = min(self.list)
        self.range = self.max - self.min
        self.ax = ax = self.fig.add_subplot()
        plt.xticks([])
        plt.yticks([])
        self.rects = ax.bar(range(len(self.list)), self.list)
        self.line = plt.plot([0, 0], [0, self.max_line], color='k', linestyle='-', linewidth=2)

        plt.xlabel("")
        plt.ylabel("")
        plt.title("Sorting...")
        if arr is None:
            self.shuffle()

    def __len__(self):
        return len(self.list)

    def __str__(self):
        return str(self.list)

    def __getitem__(self, item):
        # self.__draw_line(item)
        return self.list[item]

    def __setitem__(self, key, value):
        self.__draw_line(key)
        self.list[key] = value
        self.rects[key].set_height(value)

    def swap(self, index1, index2):
        temp = self.list[index1]
        self[index1] = self.list[index2]
        self[index2] = temp

    def check(self):
        for i in range(len(self)):
            self.__draw_line(i)

    def shuffle(self):
        plt.title("Shuffling...")
        plt.draw()
        for i in range(len(self.list)):
            self.swap(i, random.randint(0, len(self.list)-1))
        plt.title("Sorting...")
        plt.draw()

    def __draw_line(self, pos):
        self.line.pop(0).remove()
        self.line = plt.plot([pos, pos], [0, self.max_line], color='k', linestyle='-', linewidth=2)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.sound.stop()
        self.sound.plays(((self.list[pos] - self.min) / self.range) * self.frequency_range + self.frequency_ofs)
