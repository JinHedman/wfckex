import pygame
import time
from pygame.locals import *
from tkinter import colorchooser
import numpy as np
from screeninfo import get_monitors


class draw_input:

    def __init__(self, size, resolution):
        self.size = size
        self.resolution = resolution
        self.color = 0
        self.colorlist = [(210,70,50),(120, 230,130),(230,130,230),(130,0,10),(130,10,230)]
        self.background_color = (12, 20, 40)
        self.colormarkingsize = 3
        self.output_structure = np.zeros( (self.size[0] * self.resolution[0], self.size[1] * self.resolution[1], 3), dtype=np.uint8)
        self.last_hover = [0,0]
        print("NOW")
        self.current_copy = np.zeros((self.resolution[0],self.resolution[1], 3))

    def Input(self):
        height = get_monitors()[0].height



        self.border = 10

        self.bsizey = int(height / self.size[1]) - int(300 / self.size[1])
        self.bsizex = int(self.bsizey * (self.resolution[0] / self.resolution[1]))
        self.bboxsizex = self.bsizex / self.resolution[0]
        self.bboxsizey = self.bsizey / self.resolution[1]

        self.colorsize = (60, min(((self.size[1] * self.bsizex) / len(self.colorlist)) - self.border - (20 / len(self.colorlist)), 80))

        self.toolbarsize = (100, self.size[1] * self.bsizex + self.border * 2)
        self.toolbarleft = self.size[0] * self.bsizex + self.border * 2 + (self.colorsize[0] + self.border * 2)

        #parametres for button: RECT tuple, text, callback, btn trigger once variable, Active
        self.buttons = []
        self.buttons.append([((self.border * 2 + self.bsizex * self.size[0], self.border * 1 + self.bsizex * self.size[1] - 20),(80, 20)),"Export", self.export_button_pygame, False, False])
        self.buttons.append([((self.toolbarleft, self.border),(80, 20)),"Copy", self.copy_button_pygame, False, False])

        pygame.init()
        self.screen = pygame.display.set_mode((self.size[0] * self.bsizex + self.border * 2 + (self.colorsize[0] + self.border * 2) + (self.toolbarsize[0] + self.border*2), self.size[1] * self.bsizey + self.border * 2))

        self.fill_background()
        self.drawfield()
        self.draw_colors()
        self.draw_grid_lines()
        self.PROGRAM_STATE = "DRAW"

        return self.mainloop()

    # draw background pattern
    def drawfield(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pygame.draw.rect(self.screen, ( (((x+y) % 2) * 20),  (((x+y) % 2) * 25), (((x+y) % 2) * 24)), ((x * self.bsizex + self.border, y * self.bsizey + self.border), (self.bsizex, self.bsizey)))

        pygame.display.update()

    # main program for handling inputs and user activities
    def mainloop(self):
        mousebuttondown = False
        clock = pygame.time.Clock()



        while True:
            # update frequency
            clock.tick(60)
            ev = pygame.event.get()
            (x, y) = pygame.mouse.get_pos()

            if self.PROGRAM_STATE == "DRAW":
                #user drawing
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousebuttondown = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        mousebuttondown = False
                        if x < self.border * 1 + self.bsizex * self.size[0] and x > self.border and y < self.border * 1 + self.bsizey * self.size[1] and y > self.border :
                            self.output_structure[int((x - self.border) / self.bboxsizex), int((y - self.border) / self.bboxsizey)] = np.array(self.colorlist[self.color])
                            pygame.draw.rect(self.screen, self.colorlist[self.color], (( x - (x - self.border) % (self.bsizex/self.resolution[0]), y - (y - self.border) % (self.bsizey/self.resolution[1])), (self.bsizex / self.resolution[0] + 1, self.bsizey / self.resolution[1] +1 )))
                        #switching color
                        if x > self.border * 2 + self.bsizex * self.size[0] and x < self.border * 2 + self.bsizex * self.size[0] + self.colorsize[0]:
                            if y < len(self.colorlist) * (self.colorsize[1] + self.border) + self.border:
                                color = int((y - self.border) / (self.colorsize[1] + self.border))
                                if color == self.color:
                                    self.colorlist[color] = colorchooser.askcolor()[0]
                                else:
                                    self.color = color
                                self.draw_colors()
                        pygame.display.update()

                    # Draw when holding mouse button
                if mousebuttondown:
                    if x < self.border * 1 + self.bsizex * self.size[0] and x > self.border and y < self.border * 1 + self.bsizey * self.size[1] and y > self.border :
                        self.output_structure[int((x-self.border) / self.bboxsizex), int((y-self.border) / self.bboxsizey)] = np.array(self.colorlist[self.color])
                        pygame.draw.rect(self.screen, self.colorlist[self.color], ((x - (x - self.border) % (self.bsizex / self.resolution[0]), y - (y - self.border) % (self.bsizey / self.resolution[1])),(self.bsizex / self.resolution[0] + 1,self.bsizey / self.resolution[1] + 1)))
                        self.draw_grid_lines()
                        pygame.display.update()

            if self.PROGRAM_STATE == "COPY":
                if x < self.border * 1 + self.bsizex * self.size[0] and x > self.border and y < self.border * 1 + self.bsizey * self.size[1] and y > self.border:
                    if int((x - self.border) / self.bsizex) != self.last_hover[0] or int((y - self.border) / self.bsizey) != self.last_hover[1]:
                        self.last_hover = [int((x - self.border) / self.bsizex), int((y - self.border) / self.bsizey)]
                        self.redraw_field(False)
                        pygame.draw.lines(self.screen, (255,255,230),True, [(x - (x - self.border) % (self.bsizex), y - (y - self.border) % (self.bsizey)),
                                                                            (x - (x - self.border) % (self.bsizex), y - (y - self.border) % (self.bsizey) + self.bsizey + 1),
                                                                            (x - (x - self.border) % (self.bsizex) + self.bsizex + 1, y - (y - self.border) % (self.bsizey) +self.bsizey + 1),
                                                                            (x - (x - self.border) % (self.bsizex) + self.bsizex + 1, y - (y - self.border) % (self.bsizey))])


                        if not (self.current_copy == np.array([0,0,0])).all():

                            for yy in range(self.resolution[1]):
                                for xx in range(self.resolution[0]):
                                    xx2 = xx + self.last_hover[0] * self.resolution[0]
                                    yy2 = yy + self.last_hover[1] * self.resolution[1]

                                    print(xx2, yy2)
                                    pygame.draw.rect(self.screen, tuple(self.current_copy[yy,xx]), (((xx2 * self.bsizex / self.resolution[0]) + self.border,
                                                                                               (yy2 * self.bsizey / self.resolution[1]) + self.border),
                                                                                               (self.bsizex / self.resolution[0] + 1,
                                                                                               self.bsizey / self.resolution[1] + 1)))

                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONUP:
                            if (self.current_copy == np.array([0, 0, 0])).all():
                                self.current_copy = self.output_structure.transpose((1,0,2))[self.last_hover[1]*self.resolution[1]:self.last_hover[1]*self.resolution[1]+self.resolution[1],self.last_hover[0]*self.resolution[0]:self.last_hover[0]*self.resolution[0]+self.resolution[0]]
                            else:
                                for yy in range(self.resolution[1]):
                                    for xx in range(self.resolution[0]):
                                        xx2 = xx + self.last_hover[0] * self.resolution[0]
                                        yy2 = yy + self.last_hover[1] * self.resolution[1]
                                        self.output_structure[xx2][yy2] = self.current_copy.transpose((1,0,2))[xx][yy]
                                pygame.display.update()

            for button in self.buttons:
                # export button
                if button[0][0][0] <= x <= button[0][0][0] + button[0][1][0] and button[0][0][1] <= y <= button[0][0][1] + button[0][1][1]:
                    pygame.draw.rect(self.screen, (255, 240, 240), [button[0][0][0], button[0][0][1], button[0][1][0], button[0][1][1]])
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONUP:
                            statement = button[2]()
                            if button[4]:
                                button[4] = False
                            else:
                                button[4] = True

                            if statement is not None:
                                return statement

                    smallfont = pygame.font.Font('Cocogoose Pro Light-trial.ttf', 11)
                    text = smallfont.render(button[1], True, (0, 0, 0))
                    self.screen.blit(text, (button[0][0][0] + 15, button[0][0][1] + 2))
                    if not button[3]:
                        pygame.display.update()
                        button[3] = True
                else:
                    # if button active (pressed down)
                    if button[4]:
                        pygame.draw.rect(self.screen, (120, 130, 220), [button[0][0][0], button[0][0][1], button[0][1][0], button[0][1][1]])
                        smallfont = pygame.font.Font('Cocogoose Pro Light-trial.ttf', 11)
                        text = smallfont.render(button[1], True, (0, 0, 0))
                        self.screen.blit(text, (button[0][0][0] + 15, button[0][0][1] + 2))

                    else:
                        pygame.draw.rect(self.screen, (220, 230, 220),[button[0][0][0], button[0][0][1], button[0][1][0], button[0][1][1]])
                        smallfont = pygame.font.Font('Cocogoose Pro Light-trial.ttf', 11)
                        text = smallfont.render(button[1], True, (0, 0, 0))
                        self.screen.blit(text, (button[0][0][0] + 15, button[0][0][1] + 2))

                    if button[3]:
                        pygame.display.update()
                        button[3] = False

            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return self.output_structure

            #print(self.PROGRAM_STATE)
            pygame.display.update()

    def redraw_field(self, DrawBG):
        self.drawfield()
        self.draw_grid_lines()
        self.draw_pixels(DrawBG)

    def draw_pixels(self, DrawBG):
        for x, row in enumerate(self.output_structure):
            for y, element in enumerate(row):
                if not DrawBG or (element != np.array([0,0,0])).all():
                    pygame.draw.rect(self.screen, tuple(element), ((x * (self.bsizex / self.resolution[0]) + self.border,
                                                                                y * (self.bsizey / self.resolution[1]) + self.border),
                                                                               (self.bsizex / self.resolution[0] + 1,
                                                                               self.bsizey / self.resolution[1] + 1)))
        pygame.display.update()
    def export_button_pygame(self):
        pygame.quit()
        return self.output_structure

    def copy_button_pygame(self):
        if self.PROGRAM_STATE == "COPY":
            self.PROGRAM_STATE = "DRAW"
            self.current_copy = np.zeros((self.resolution[0], self.resolution[1], 3))
            self.redraw_field(False)
        else:
            self.PROGRAM_STATE = "COPY"


    def fill_background(self):
        pygame.draw.rect(self.screen, self.background_color, ((0,0),(self.screen.get_width(), self.screen.get_height())))

    def draw_grid_lines(self):
        for y in range(self.size[0] + 1):
            pygame.draw.line(self.screen, (100,100,100), (self.border + self.bsizex * y, self.border) , (self.border + self.bsizex * y, self.border + self.bsizey * self.size[1]) )
        for x in range(self.size[1] +1):
            pygame.draw.line(self.screen, (100,100,100), (self.border, self.border + self.bsizey * x) , (self.border + self.bsizex * self.size[0], self.border + self.bsizey * x) )

    def draw_colors(self):
        # color display
        pygame.draw.rect(self.screen, self.background_color, ((self.border * 1 + self.bsizex * self.size[0], 0),(self.colorsize[0] + self.border*2, self.screen.get_height())))
        for i, color in enumerate(self.colorlist):

            if i == self.color:
                pygame.draw.rect(self.screen, (255, 255, 200), ((self.border * 2 + self.bsizex * self.size[0] - self.colormarkingsize, self.border + ((i * self.border) + i * self.colorsize[ 1]) - self.colormarkingsize),
                                                                (self.colorsize[0] + self.colormarkingsize*2, self.colorsize[1] + self.colormarkingsize*2)))

            pygame.draw.rect(self.screen, (color), ((self.border * 2 + self.bsizex * self.size[0], self.border + ((i * self.border) + i * self.colorsize[1])), self.colorsize))



