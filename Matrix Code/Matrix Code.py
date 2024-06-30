import pygame #Modules
import numpy
import random
import os
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Color Constants
GREEN = (34, 255, 0)
BLACK = (10, 10, 10)

pygame.init() #Initaization and clock and game loop condition
info = pygame.display.Info()
clock = pygame.time.Clock()
run = True

#Screen
size = (info.current_w, info.current_h)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Matrix Code')
h = screen.get_height()
w = screen.get_width()

#Text
characters = 'Z123457890123457890~!#$%^&*()_+-=[]\\{}|;\':\",./<>?@@@@@@@'
characters = list(characters.strip(' '))
font = pygame.font.Font(r'DATA\matrix code nfi.ttf', 25)
strings = []

#Time stuff
time_interval = 100
next_time = 0
current_time = pygame.time.get_ticks()

def duplicate(A):
    newlist = []
    newlist.append(A[0])
    for i, element in enumerate(A):
        if i > 0 and A[i - 1] != element:
            newlist.append(element)
    return newlist

class Text:
    def __init__(self, x_pos):
        self.char = numpy.array([])
        self.char = numpy.random.choice(characters, random.randint(10, 30))
        self.char = duplicate(self.char)
        self.length = len(self.char)
        self.offset = random.randint(0, 15)*22
        self.x_pos = x_pos
        self.speed = random.choice([2,3,3,4,4])
        self.queue = [pygame.Rect(self.x_pos+5, 0, 25, self.length*22),
                      pygame.Rect(self.x_pos+5, -h, 25, self.length*22),
                      pygame.Rect(self.x_pos+5, -h*2, 25, self.length*22)]

    def draw(self):
        for i in range(self.length):
            for j in self.queue:
                screen.blit(font.render(self.char[i], True, GREEN), [j.x, j.y+(i*22)+self.offset])

    def append_and_pop(self):
        if self.queue[0].top >= h:
            self.queue.append(pygame.Rect(self.x_pos+5, -h*2, 25, self.length*22))
            del self.queue[0]

    def scroll(self):
        for i in self.queue:
            i.y += self.speed

    def change(self):
        self.char[random.randint(0, self.length-1)] = random.choice(characters)

for i in range(w//25):
    strings.append(Text(i*25))

while run: #Game loop
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get(): #Event loop
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            run = False

    screen.fill(BLACK)
    for i in strings:
        i.draw()
        i.scroll()
        i.append_and_pop()
        current_time = pygame.time.get_ticks()

    if current_time > next_time:
        next_time += time_interval
        for i in strings:
            i.change()
            i.change()

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()
