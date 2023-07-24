#!/usr/bin/python3
import math
from sys import argv
import random
import time
import pygame

FPS = 30
MIN_TOKEN_LENGTH = 5

AUTOPLAY_SPEED = 75 / 60 # chars per sec
AUTOPLAY_NL_PAUSE = 3 #  sec
AUTOPLAY_START_DELAY = 5 #sec

BACKGROUND_COLOR = (255, 255, 255)
FOREGROUND_COLOR = (0, 0, 0)

PARTICLE_COUNT = 100
PARTICLE_SIZE = (10, 15) # px
PARTICLE_VELOCITY = (500, 2000) # px per second
PARTICLE_FADE = 0.85

def slurp_file(path: str) -> str:
    content = ''
    with open(path) as f:
        content = f.read()
    return content

# gives a floating point number from 0 to 1 expressing the progress
def fprogress(tokens: list[str], i: int) -> float:
    written = tokens[:i+1]
    return float(
        (len(''.join(written)) + len(written) - 1)) / float(len(''.join(tokens)) + len(tokens) - 1)

#loading fonts with caching
fonts = {}
def load_font(name: str, size: int, bold: bool, italic: bool):
    key = f"{name}-{size}-{bold}-{italic}"
    if fonts.get(key) != None:
        return fonts[key]
    fonts[key] = pygame.font.SysFont(name, size, bold, italic)
    return fonts[key]

def load_tokens(filepath: str) -> list[str]:
    # get all the 'words' in a file (splits text by spaces and newlines)
    words = list(
            filter(lambda s: len(s) > 0,
                sum(
                    map(lambda s: s.split(' '),
                    sum(
                        [[s, '\n'] for s in slurp_file(filepath).split('\n')],
                    [])),
                [])))
    
    # create a list of tokens, so that each token is at least MIN_TOKEN_LENGTH charachters long
    j = 0
    tokens = []
    current_token = ""
    while j < len(words):
        first = True
        while j < len(words) and words[j] != '\n' and len(current_token) < MIN_TOKEN_LENGTH:
            if first:
                first = False
            else:
                current_token += ' '
            current_token += words[j]
            j += 1
        tokens.append(current_token)
        current_token = ""
        while j < len(words) and words[j] == '\n':
            tokens.append(words[j])
            j += 1
    
    return tokens

class Particle:
    def __init__(self, px, py, vx, vy, s, f) -> None:
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.s = s
        self.fade = f
        self.awake = False
    
    def render(self, screen: pygame.Surface, c):
        if self.awake:
            pygame.draw.rect(screen, c, (self.px - self.s/2.0, self.py - self.s/2.0, self.s, self.s))
    
    def update(self, w: int, h: int):
        self.awake = self.s >= 1 or 0 < self.px < w and 0 < self.py < h
        if self.awake:
            self.s *= self.fade
            self.px += self.vx * 1.0/FPS
            self.py += self.vy * 1.0/FPS

def new_particles(px: int, py: int) -> list[Particle]:
    ps = []
    for _ in range(PARTICLE_COUNT):
        v = random.random() * (PARTICLE_VELOCITY[1]-PARTICLE_VELOCITY[0]) + PARTICLE_VELOCITY[0]
        a = random.random() * math.pi * 2
        vx = v * math.cos(a)
        vy = v * math.sin(a)
        s = random.random() * (PARTICLE_SIZE[1]-PARTICLE_SIZE[0]) + PARTICLE_SIZE[0]
        ps.append(Particle(px, py, vx, vy, s, PARTICLE_FADE))
    return ps

def autoplay_calculate_time(x: str) -> float:
    return (len(x) + 2) / AUTOPLAY_SPEED

if __name__ == '__main__':
    if len(argv) >= 2:
        filename = argv[1]
        tokens = load_tokens(filename)

        # pygame init
        clock = pygame.time.Clock()
        pygame.font.init()
        bg, fg = BACKGROUND_COLOR, FOREGROUND_COLOR
        (width, height) = (800, 600)
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption('dictator.py')
        screen.fill(bg)

        pygame.display.flip()

        i = 0
        autoplay = False
        ap_last_time = time.time()
        ap_wait_time = AUTOPLAY_START_DELAY + autoplay_calculate_time(tokens[i])
        particles = []

        running = True
        while running:
            # screen
            w = screen.get_width()
            h = screen.get_height()
            screen.fill(bg)
            # drawing text
            for p in particles:
                p.render(screen, fg)
                p.update(w, h)
            
            text = tokens[i]
            font = load_font("monospace", h//15, True, False)
            if text == '\n':
                text = "a capo"
                font = load_font("monospace", h//25, False, True)
            label = font.render(text, 10, fg)
            screen.blit(label, (w/2-label.get_width()/2, h/2-label.get_height()/2))
            # writing progress
            p = fprogress(tokens, i)
            progress = f"{i+1}/{len(tokens)} ({p*100:.2f}%)"
            progress_label = load_font("monospace", h//50, False, False).render(progress, 10, fg)
            padding = h//15
            screen.blit(progress_label, (w/2-progress_label.get_width()/2,h-progress_label.get_height()-padding))
            # drawing progress bar
            bar_height = h//80
            pygame.draw.rect(screen, fg, (0, h-bar_height, w*p, bar_height))
            # drawing autoplay marker
            if autoplay:
                autoplay_label = load_font("monospace", h//50, False, False).render("autoplay", 10, fg)
                screen.blit(autoplay_label, (w/2-autoplay_label.get_width()/2,padding))

            pygame.display.update()

            # handling events/keystrokes
            prev_i = i
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        tokens = load_tokens(filename)
                        i = min(i, len(tokens)-1)
                    elif event.key == pygame.K_p:
                        autoplay = not autoplay
                        ap_last_time = time.time()
                        ap_wait_time = AUTOPLAY_START_DELAY + autoplay_calculate_time(tokens[i])
                    elif event.key == pygame.K_TAB:
                        i = (i+10) % len(tokens)
                    elif event.key == pygame.K_BACKSPACE:
                        i = (i-10) % len(tokens)
                    elif event.key == pygame.K_LEFT:
                        i = max(0, i-1)
                    elif event.key == pygame.K_0:
                        i = 0
                    elif event.key == pygame.K_1:
                        i = 0
                        while fprogress(tokens, i) < 0.1:
                            i+=1
                    elif event.key == pygame.K_2:
                        i = int(len(tokens)*0.1)
                        while fprogress(tokens, i) < 0.2:
                            i+=1
                    elif event.key == pygame.K_3:
                        i = int(len(tokens)*0.15)
                        while fprogress(tokens, i) < 0.3:
                            i+=1
                    elif event.key == pygame.K_4:
                        i = int(len(tokens)*0.2)
                        while fprogress(tokens, i) < 0.4:
                            i+=1
                    elif event.key == pygame.K_5:
                        i = int(len(tokens)*0.25)
                        while fprogress(tokens, i) < 0.5:
                            i+=1
                    elif event.key == pygame.K_6:
                        i = int(len(tokens)*0.35)
                        while fprogress(tokens, i) < 0.6:
                            i+=1
                    elif event.key == pygame.K_7:
                        i = int(len(tokens)*0.45)
                        while fprogress(tokens, i) < 0.7:
                            i+=1
                    elif event.key == pygame.K_8:
                        i = int(len(tokens)*0.55)
                        while fprogress(tokens, i) < 0.8:
                            i+=1
                    elif event.key == pygame.K_9:
                        i = int(len(tokens)*0.65)
                        while fprogress(tokens, i) < 0.9:
                            i+=1
                    else:
                        i = (i+1) % len(tokens)
                        if event.key == pygame.K_SPACE and i >= len(tokens):
                            running = False
            
            if autoplay:
                elapsed_time = time.time() - ap_last_time
                if elapsed_time <= 1.0/AUTOPLAY_SPEED:
                    fg, bg = BACKGROUND_COLOR, FOREGROUND_COLOR
                else:
                    fg, bg = FOREGROUND_COLOR, BACKGROUND_COLOR
                if elapsed_time >= ap_wait_time or prev_i != i:
                    if i < len(tokens) - 1:
                        i += 1
                        if tokens[i] == '\n':
                            ap_wait_time = AUTOPLAY_NL_PAUSE
                        else:
                            ap_wait_time = autoplay_calculate_time(tokens[i])
                        ap_last_time = time.time()
                    else:
                        autoplay = False
            else:
                fg, bg = FOREGROUND_COLOR, BACKGROUND_COLOR

            if prev_i != i and tokens[i] == '\n':
                particles.clear()
                particles = new_particles(w//2, h//2)
            
            clock.tick(FPS)

    else:
        print("USAGE: dictator.py <filename>")