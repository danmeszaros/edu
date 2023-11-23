#!/usr/bin/python3

import pygame
import random
import time
pygame.init()

screen = pygame.display.set_mode([1920, 1080])
font = pygame.font.Font('freesansbold.ttf', 64)
crash_sound = pygame.mixer.Sound("wav/error.wav")
ok_sound = []
#ok_sound.append(pygame.mixer.Sound("wav/ok1.wav"))
ok_sound.append(pygame.mixer.Sound("wav/ok2.wav"))
ok_sound.append(pygame.mixer.Sound("wav/ok3.wav"))
ok_sound.append(pygame.mixer.Sound("wav/ok4.wav"))
ok_sound.append(pygame.mixer.Sound("wav/ok5.wav"))

running = True
RECT = 100

red = (255, 128, 128)
green = (128, 255, 128)

class Generator:
    def __init__(self, y):
        self.x = 1
        self.y = y

    def getNext(self):
        res = (self.x, self.y)

        self.x = self.x + 1

        if self.x == 11:
            self.y = self.y + 1
            self.x = 1

        return res

generator = Generator(2)

class Digit:
    def __init__(self, x, y, bgcolor, value, shown):
        self.x = x
        self.y = y
        self.value = value
        self.shown = shown
        self.bgcolor = bgcolor

        self.text = font.render(str(self.value), False, (0,0,0))

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgcolor, pygame.Rect(self.x, self.y, RECT, RECT),  3)
        if self.shown:
            screen.blit(self.text, (self.x + RECT / 3, self.y + RECT / 3))

def getx(n):
    return 100 + n * 110

def num_to_digits(num, pos, y, color, shown):
    res = []

    dgs = []
    while num > 0:
        dgs.append(num % 10)
        num = int(num / 10)

    dgs.reverse()

    for d in dgs:
        res.append(Digit(getx(pos), y, color, d, shown))
        pos = pos + 1

    return res

def gen_digits(num1, op, num2):
    res = []

    res.extend(num_to_digits(num1, len(res), 100, red, True))
    res.append(Digit(getx(len(res)), 100, red, op, True))
    res.extend(num_to_digits(num2, len(res), 100, red, True))
    res.append(Digit(getx(len(res)), 100, red, "=", True))

    return res

def gen_test():
    return (num_to_digits(12345, 0, 100, red, True), 0)

def gen_add3():
    res = []

    a1 = random.randrange(0, 90)
    a2 = random.randrange(0, 90)
    
    a3 = a1 + a2

    res = gen_digits(a1, "+", a2)
    idx = len(res)
    res.extend(num_to_digits(a3, idx, 100, green, False))

    return (res, idx)

def gen_div():
    a1 = random.randrange(1, 11)
    a2 = random.randrange(1, 11)

    a3 = a1 * a2

    res = []
    res = gen_digits(a3, ":", a1)
    idx = len(res)

    res.extend(num_to_digits(a2, idx, 100, green, False))

    return (res, idx)

def gen_add1():
    res = []
    a1 = random.randrange(1, 10)
    a2 = random.randrange(0, 9)

    b1 = random.randrange(1, 10 - a2)
    a = a1 * 10 + a2

    res = gen_digits(a, "+", b1)
    idx = len(res)

    res.extend(num_to_digits(a + b1, idx, 100, green, False))
    
    return (res, idx)

def gen_add2():
    res = []
    a1 = random.randrange(1, 9)
    a2 = random.randrange(3, 9)

    b1 = random.randrange(10 - a2, 10)

    s = a1 * 10 + a2 + b1

    res.append(Digit(getx(0), 150, red, a1, True))
    res.append(Digit(getx(1), 150, red, a2, True))
    res.append(Digit(getx(2), 150, red, "+", True))
    res.append(Digit(getx(3), 150, red, b1, True))
    res.append(Digit(getx(4), 150, red, "=", True))

    x1 = 10 - a2
    x2 = b1 - x1

    res.append(Digit(getx(1), 40, green, x1, False))
    res.append(Digit(getx(3), 40, green, x2, False))

    res.append(Digit(getx(5), 150, green, int(s / 10), False))
    res.append(Digit(getx(6), 150, green, s % 10, False))

    return (res, 5)


def gen_mult():
    res = []
    #a = random.randrange(1, 10)
    #b = random.randrange(1, 10)

    (a,b) = generator.getNext()

    res = gen_digits(a, ".", b)

    prod = a * b

    idx = len(res)
    res.extend(num_to_digits(prod, idx, 100, green, False))

    return (res, idx)

def gen():
    return gen_mult()
    # return gen_div()

    x = random.randrange(2, 4)

    if x == 0:
        return gen_add2()
    if x == 1:
        return gen_add1()
    if x == 2:
        return gen_mult()
    if x == 3:
        return gen_div()

def getKey(keys):
    i = pygame.K_0
    while i <= pygame.K_9:
        if keys[i]:
            return i - pygame.K_0

        i = i + 1

    i = pygame.K_KP0
    while i <= pygame.K_KP9:
        if keys[i]:
            return i - pygame.K_KP0

        i = i + 1

    return None

def getScoreText(font, caption, val):
    return font.render("%s: %d" %(caption, val), False, (0,0,0))

(digits, idx) = gen()

pkey = None
key = None

correct = 0
incorrect = 0

correctText = getScoreText(font, "correct", 0)
incorrectText = getScoreText(font, "incorrect", 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()

            pkey = getKey(keys)

        if event.type == pygame.KEYUP and pkey != None:
            key = pkey
            pkey = None

    if key != None:
        # print("%d %d" %(idx, key))
        if digits[idx].value == key:
            digits[idx].shown = True
            idx = idx + 1
        else:
            pygame.mixer.Sound.play(crash_sound)
            incorrect = incorrect + 1
            incorrectText = getScoreText(font, "incorrect", incorrect)

        key = None

    screen.fill((255, 255, 255))

    for digit in digits:
        digit.draw(screen)

    if idx >= len(digits):
        correct = correct + 1
        correctText = getScoreText(font, "correct", correct)

    screen.blit(correctText, (100, 300)) 
    screen.blit(incorrectText, (100, 400))


    pygame.display.flip()

    if idx >= len(digits):
        pygame.mixer.Sound.play(ok_sound[random.randrange(0, len(ok_sound))])
        time.sleep(1)
        (digits, idx) = gen()


pygame.quit()
