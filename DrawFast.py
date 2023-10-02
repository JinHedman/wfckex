import pygame
import time
from pygame.locals import *

from screeninfo import get_monitors


class DrawFast:
    def __init__(self, field):

        self.field = field
        self.shape = self.field.shape

        monitor = get_monitors()[0]
        acc_monitor_field = (monitor.width * 0.8, monitor.height * 0.8)
        

        draw_ratio = float(self.shape[1]) / float(self.shape[0])
        screen_ratio = float(acc_monitor_field[1]) / float(acc_monitor_field[0])
        print(draw_ratio)

        self.direction = "left"

        # if x draw size is largest
        if draw_ratio > screen_ratio:
            print("1körs")
            self.height = acc_monitor_field[1] 
            self.width = int(acc_monitor_field[1] / draw_ratio) 
            self.direction = "top"
        else:
            self.width = acc_monitor_field[0]
            self.height = int(acc_monitor_field[0] / draw_ratio) 
            self.direction = "left"

        self.border = 0

        if self.direction == "left" :
            self.bsize = int((self.width / field.shape[0]))
        else:
            print("2körs")
            self.bsize = int((self.height / field.shape[1]))


        pygame.init()
        self.screen = pygame.display.set_mode((self.shape[0] * self.bsize + self.border * 2, self.shape[1] * self.bsize + self.border * 2))


    def update(self, field):
        self.field = field
        self.screen.fill((10,16,10))

        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                if type(self.field) is int:
                    pygame.draw.rect(self.screen, self.get_color(self.field[x, y]), ((x * self.bsize + self.border, y * self.bsize + self.border),(self.bsize, self.bsize)))
                else:
                    pygame.draw.rect(self.screen, tuple(self.field[x, y]) , ((x * self.bsize + self.border, y * self.bsize + self.border),(self.bsize, self.bsize)))


        pygame.display.update()
        clock = pygame.time.Clock()
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return

    def draw_once(self, field):
        self.field = field
        self.screen.fill((10, 16, 10))

        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                if type(self.field) is int:
                    pygame.draw.rect(self.screen, self.get_color(self.field[x, y]), (
                    (x * self.bsize + self.border, y * self.bsize + self.border), (self.bsize, self.bsize)))
                else:
                    pygame.draw.rect(self.screen, tuple(self.field[x, y]), (
                    (x * self.bsize + self.border, y * self.bsize + self.border), (self.bsize, self.bsize)))

        pygame.display.update()
        clock = pygame.time.Clock()
        while True:
            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.QUIT:

                    pygame.display.quit()
                    pygame.quit()
                    return
    def wait(self):
        time.sleep(2)

    def get_color(self, num):
        return (int(0 + num * 200), int( 200 - num*200), int( 100  + num*100))
