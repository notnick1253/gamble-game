import random
import pygame
from update import update_check

update_check()

pygame.init()

coins = 10

window_x = 600
window_y = 400

zahlen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]

screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Gamba Gamba V.2")

clock = pygame.time.Clock()

schrift = pygame.font.Font(None, 100)
hdhjs = pygame.font.Font(None, 35)
creator = pygame.font.Font(None, 20)
switch_font = pygame.font.Font(None, 43)

lever_x = window_x / 2 + 170

lever_top = window_y / 2 - 70
lever_bottom = window_y / 2 + 100

knob_y = lever_top

dragging = False
returning = False

knob = pygame.Rect(0, 0, 20, 20)

slot_running = False
slot_timer = 0
slot_duration = 1.5

# 3 oder 5 Slots
slot_size = 3

current_numbers = [7, 7, 7, 7, 7]

switch_button = pygame.Rect(window_x/2-25, 10, 50, 20)


def handle(slots):

    global knob

    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (
            window_x / 2 + 160 + slots,
            0,
            window_x - (window_x / 2 + 145) + slots,
            window_y
        )
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (window_x / 2 + 155 + slots, window_y / 2 - 25),
        (window_x / 2 + 185 + slots, window_y / 2 - 25),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (window_x / 2 + 155 + slots, window_y / 2 + 25),
        (window_x / 2 + 185 + slots, window_y / 2 + 25),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (window_x / 2 + 185 + slots, window_y / 2 - 25),
        (window_x / 2 + 185 + slots, window_y / 2 + 25),
        2
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (lever_x + slots, knob_y),
        (lever_x + slots, window_y / 2),
        6
    )

    knob = pygame.draw.circle(
        screen,
        (255, 255, 255),
        (lever_x + slots, knob_y),
        10
    )


def wahrscheinlichkeiten():

    global wahrscheinlichkeiten1
    global wahrscheinlichkeiten2
    global wahrscheinlichkeiten3

    wahrscheinlichkeiten1 = []
    wahrscheinlichkeiten2 = []
    wahrscheinlichkeiten3 = []

    for _ in range(12):

        wahrscheinlichkeiten1.append(
            random.choice(zahlen)
        )

        wahrscheinlichkeiten2.append(
            random.choice(zahlen)
        )

        wahrscheinlichkeiten3.append(
            random.choice(zahlen)
        )


def coin_reback(*werte):

    global coins

    counts = {}

    for wert in werte:

        if wert in counts:
            counts[wert] += 1
        else:
            counts[wert] = 1

    höchstes_ergebnis = max(counts.values())

    if höchstes_ergebnis == 5:
        coins += 100

    elif höchstes_ergebnis == 4:
        coins += 25

    elif höchstes_ergebnis == 3:
        coins += 10

    elif höchstes_ergebnis == 2:
        coins += 4


def zahlen_bestimmen():

    global current_numbers

    current_numbers = [
        random.choice(wahrscheinlichkeiten1),
        random.choice(wahrscheinlichkeiten2),
        random.choice(wahrscheinlichkeiten3),
        random.choice(wahrscheinlichkeiten1),
        random.choice(wahrscheinlichkeiten2)
    ]


def start_slot():

    global coins
    global slot_running
    global slot_timer

    if coins < 2:
        return

    if slot_running:
        return

    coins -= 2

    wahrscheinlichkeiten()

    zahlen_bestimmen()

    slot_timer = 0
    slot_running = True


def update_slot(dt):

    global slot_timer
    global slot_running
    global current_numbers

    if not slot_running:
        return

    slot_timer += dt

    if slot_timer < slot_duration:

        # Animation

        zahlen_bestimmen()

    else:

        # Letzte Zahlen

        zahlen_bestimmen()

        # Gewinn berechnen

        coin_reback(*current_numbers)

        slot_running = False


def build_slot(size):

    global slots

    if size == 3:

        slots = 0

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 115,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 35,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 + 45,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 130,
                window_y / 2 - 60,
                260,
                130
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 155,
                window_y / 2 - 85,
                310,
                155
            ),
            1
        )

    elif size == 5:

        slots = 80

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 195,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 115,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 35,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 + 45,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255, 255),
            (
                window_x / 2 + 125,
                window_y / 2 - 45,
                70,
                100
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 210,
                window_y / 2 - 60,
                420,
                130
            ),
            1
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                window_x / 2 - 235,
                window_y / 2 - 85,
                470,
                155
            ),
            1
        )


def switch():
    if slot_size == 5:
        left = (255, 255, 255)
        right = (0, 0, 0)
        block = (window_x/2+4, 14, 22, 25)

    elif slot_size == 3:
        left = (0, 0, 0)
        right = (255, 255, 255)
        block = (window_x/2-26, 14, 22, 25)

        
    screen.fill((0,0,0), (window_x/2-30, 10, 60, 33))
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (window_x/2-30, 10, 60, 33),
        1
    )
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        block,
    )
    
    die_drei = switch_font.render(
        "3",
        True,
        left
    )
    drei_x = die_drei.get_width()
    
    die_fünf = switch_font.render(
        "5",
        True,
        right
    )
    fünf_x = die_fünf.get_width()
     
    screen.blit(
        die_drei,
        (int(window_x/2-15-drei_x/2), 13)
        )
    screen.blit(
        die_fünf,
        (int(window_x/2+15-fünf_x/2), 13)
        )
    

running = True

while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if knob.collidepoint(event.pos):

                    if not slot_running:

                        dragging = True
                        returning = False

                if switch_button.collidepoint(event.pos):
                    if slot_size == 3:
                        slot_size = 5
                    elif slot_size == 5:
                        slot_size = 3

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                if dragging:

                    dragging = False
                    returning = True

                    start_slot()

    if dragging:

        mouse_y = pygame.mouse.get_pos()[1]

        knob_y = mouse_y

        if knob_y > lever_bottom:
            knob_y = lever_bottom

        if knob_y < lever_top:
            knob_y = lever_top

    if returning and not dragging:

        speed = 225

        knob_y -= speed * dt

        if knob_y <= lever_top:

            knob_y = lever_top
            returning = False

    update_slot(dt)

    screen.fill((0, 0, 0))

    # Hier stellst du 3 oder 5 Slots ein
    build_slot(slot_size)
    
    
    switch()

    creator_schrift = creator.render(
        "- created by not.nick -",
        True,
        (150, 150, 150)
    )

    creator_x = creator_schrift.get_width()

    zahl1 = schrift.render(
        str(current_numbers[0]),
        True,
        (255, 255, 255)
    )

    zahl2 = schrift.render(
        str(current_numbers[1]),
        True,
        (255, 255, 255)
    )

    zahl3 = schrift.render(
        str(current_numbers[2]),
        True,
        (255, 255, 255)
    )

    screen.blit(
        zahl1,
        (window_x / 2 - 100, window_y / 2 - 30)
    )

    screen.blit(
        zahl2,
        (window_x / 2 - 20, window_y / 2 - 30)
    )

    screen.blit(
        zahl3,
        (window_x / 2 + 60, window_y / 2 - 30)
    )

    if slot_size == 5:

        zahl4 = schrift.render(
            str(current_numbers[3]),
            True,
            (255, 255, 255)
        )

        zahl5 = schrift.render(
            str(current_numbers[4]),
            True,
            (255, 255, 255)
        )

        screen.blit(
            zahl4,
            (window_x / 2 - 180, window_y / 2 - 30)
        )

        screen.blit(
            zahl1,
            (window_x / 2 - 100, window_y / 2 - 30)
        )

        screen.blit(
            zahl2,
            (window_x / 2 - 20, window_y / 2 - 30)
        )

        screen.blit(
            zahl3,
            (window_x / 2 + 60, window_y / 2 - 30)
        )

        screen.blit(
            zahl5,
            (window_x / 2 + 140, window_y / 2 - 30)
        )

    creator_x = creator_schrift.get_width()

    screen.blit(
        creator_schrift,
        (window_x / 2 - creator_x / 2, window_y - 20)
    )

    coin_count = hdhjs.render(
        f"coins: {coins}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        coin_count,
        (10, 10)
    )

    handle(slots)

    pygame.display.update()


pygame.quit()