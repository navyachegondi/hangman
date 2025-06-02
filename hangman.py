import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Word list
words = ['PYTHON', 'COMPUTER', 'PYGAME', 'PROGRAMMING', 'DEVELOPER']
word = random.choice(words)
guessed = []

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400

for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(65 + i), True])  # 65 = ASCII 'A'

# Game status
hangman_status = 0

def draw_hangman(status):
    # Draw gallows
    pygame.draw.line(win, BLACK, (150, 450), (150, 100), 5)  # vertical
    pygame.draw.line(win, BLACK, (150, 100), (300, 100), 5)  # top bar
    pygame.draw.line(win, BLACK, (300, 100), (300, 150), 5)  # rope

    # Draw parts based on status
    if status > 0:
        pygame.draw.circle(win, BLACK, (300, 180), 30, 3)  # head
    if status > 1:
        pygame.draw.line(win, BLACK, (300, 210), (300, 300), 3)  # body
    if status > 2:
        pygame.draw.line(win, BLACK, (300, 240), (250, 270), 3)  # left arm
    if status > 3:
        pygame.draw.line(win, BLACK, (300, 240), (350, 270), 3)  # right arm
    if status > 4:
        pygame.draw.line(win, BLACK, (300, 300), (250, 350), 3)  # left leg
    if status > 5:
        pygame.draw.line(win, BLACK, (300, 300), (350, 350), 3)  # right leg

def draw():
    win.fill(WHITE)

    # Title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Word display
    display_word = ''
    for letter in word:
        display_word += letter + ' ' if letter in guessed else '_ '
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # Letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Hangman drawing
    draw_hangman(hangman_status)

    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

# Main game loop
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dist = ((x - m_x)**2 + (y - m_y)**2)**0.5
                    if dist < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1

    won = all(letter in guessed for letter in word)
    if won:
        display_message("YOU WON!")
        break

    if hangman_status == 6:
        display_message(f"YOU LOST! The word was {word}")
        break

pygame.quit()
