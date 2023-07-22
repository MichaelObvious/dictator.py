#!/usr/bin/python3
from sys import argv
import pygame

FPS = 20
MIN_TOKEN_LENGTH = 5

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
    

if __name__ == '__main__':
    if len(argv) >= 2:
        filename = argv[1]
        tokens = load_tokens(filename)

        # pygame init
        clock = pygame.time.Clock()
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
            # screen
            w = screen.get_width()
            h = screen.get_height()
            screen.fill(background_colour)
            BLACK = (0, 0, 0)
            # drawing text
            text = tokens[i]
            font = load_font("monospace", h//15, True, False)
            if text == '\n':
                text = "a capo"
                font = load_font("monospace", h//25, False, True)
            label = font.render(text, 10, BLACK)
            screen.blit(label, (w/2-label.get_width()/2, h/2-label.get_height()/2))
            # writing progress
            p = fprogress(tokens, i)
            progress = f"{i+1}/{len(tokens)} ({p*100:.2f}%)"
            progress_label = load_font("monospace", h//50, False, False).render(progress, 10, BLACK)
            padding = h//15
            screen.blit(progress_label, (w/2-progress_label.get_width()/2,h-progress_label.get_height()-padding))
            # drawing progress bar
            bar_height = h//80
            pygame.draw.rect(screen, BLACK, (0, h-bar_height, w*p, bar_height))

            pygame.display.update()

            # handling events/keystrokes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_r:
                        tokens = load_tokens(filename)
                        i = min(i, len(tokens)-1)
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
            clock.tick(FPS)

    else:
        print("USAGE: dictator.py <filename>")