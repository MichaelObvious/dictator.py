#!/usr/bin/python3
from sys import argv
import pygame

def slurp_file(path: str) -> str:
    content = ''
    with open(path) as f:
        content = f.read()
    return content

def fprogress(words: list[str], i: int) -> float:
    written = words[:i+1]
    return float(
        (len(''.join(written)) + len(written) - 1)) / float(len(''.join(words)) + len(words) - 1)

fonts = {}

def load_font(name: str, size: int, bold: bool, italic: bool):
    key = f"{name}-{size}-{bold}-{italic}"
    if fonts.get(key) != None:
        return fonts[key]
    fonts[key] = pygame.font.SysFont(name, size, bold, italic)
    return fonts[key]
    

if __name__ == '__main__':
    if len(argv) >= 2:
        filename = argv[1]
        words = list(
            filter(lambda s: len(s) > 0,
                sum(
                    map(lambda s: s.split(' '),
                    sum(
                        [[s, '\n'] for s in slurp_file(filename).split('\n')],
                    [])),
                [])))
    
        pygame.font.init()
        background_colour = (255,255,255)
        (width, height) = (800, 600)

        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption('dictator.py')
        screen.fill(background_colour)

        pygame.display.flip()

        i = 0

        running = True
        while running:
            w = screen.get_width()
            h = screen.get_height()
            screen.fill(background_colour)
            BLACK = (0, 0, 0)
            text = words[i]
            font = load_font("monospace", h//15, True, False)
            if text == '\n':
                text = "a capo"
                font = load_font("monospace", h//25, False, True)
            label = font.render(text, 10, BLACK)
            screen.blit(label, (w/2-label.get_width()/2, h/2-label.get_height()/2))
            p = fprogress(words, i)
            progress = f"{i+1}/{len(words)} ({p*100:.2f}%)"
            progress_label = load_font("monospace", h//50, False, False).render(progress, 10, BLACK)
            padding = h//15
            screen.blit(progress_label, (w/2-progress_label.get_width()/2,h-progress_label.get_height()-padding))
            bar_height = h//80
            pygame.draw.rect(screen, BLACK, (0, h-bar_height, w*p, bar_height))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_TAB:
                        i = (i+10) % len(words)
                    elif event.key == pygame.K_BACKSPACE:
                        i = (i-10) % len(words)
                    elif event.key == pygame.K_LEFT:
                        i = max(0, i-1)
                    elif event.key == pygame.K_0:
                        i = 0
                    elif event.key == pygame.K_1:
                        i = 0
                        while fprogress(words, i) < 0.1:
                            i+=1
                    elif event.key == pygame.K_2:
                        i = int(len(words)*0.1)
                        while fprogress(words, i) < 0.2:
                            i+=1
                    elif event.key == pygame.K_3:
                        i = int(len(words)*0.15)
                        while fprogress(words, i) < 0.3:
                            i+=1
                    elif event.key == pygame.K_4:
                        i = int(len(words)*0.2)
                        while fprogress(words, i) < 0.4:
                            i+=1
                    elif event.key == pygame.K_5:
                        i = int(len(words)*0.25)
                        while fprogress(words, i) < 0.5:
                            i+=1
                    elif event.key == pygame.K_6:
                        i = int(len(words)*0.35)
                        while fprogress(words, i) < 0.6:
                            i+=1
                    elif event.key == pygame.K_7:
                        i = int(len(words)*0.45)
                        while fprogress(words, i) < 0.7:
                            i+=1
                    elif event.key == pygame.K_8:
                        i = int(len(words)*0.55)
                        while fprogress(words, i) < 0.8:
                            i+=1
                    elif event.key == pygame.K_9:
                        i = int(len(words)*0.65)
                        while fprogress(words, i) < 0.9:
                            i+=1
                    else:
                        i = (i+1) % len(words)
                        if event.key == pygame.K_SPACE and i >= len(words):
                            running = False

    else:
        print("USAGE: dictator.py <filename>")