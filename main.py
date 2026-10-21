import random
import pygame
import json
import requests
import base64
from urllib.parse import quote
from update import update_check

update_check()

pygame.init()

token = "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"


window_x_sign = 400
window_y_sign = 300

username_input = "username"
password_input = "password"

visibility = False
typing_password = False
typing_user = False
acc_not_found = False
default_password = True
default_user = True
error = False


username_box_rect = pygame.rect.Rect(window_x_sign/2-100,window_y_sign/2, 200, 35)
password_box_rect = pygame.rect.Rect(window_x_sign/2-100,window_y_sign/2+40, 200, 35)

screen_sign = pygame.display.set_mode((window_x_sign, window_y_sign))
clock = pygame.time.Clock()
pygame.display.set_caption("Sign In")

title = pygame.font.Font(None, 50)
inputt = pygame.font.Font(None, 30)
error_font = pygame.font.Font(None, 20)

error_message_surface = error_font.render(
    "password or username is wrong. Please try again", True, (255, 0, 0)
)

coins = int(open("asssets/coins.txt").readline())


def coins_on_file(anzahl):
    try:
        with open("asssets/coins.txt", "x", encoding="utf-8") as datei:
            datei.write(str(coins))
    except FileExistsError:
        with open("asssets/coins.txt", "w", encoding="utf-8") as datei:
            datei.write(str(coins))

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
authorized = False

knob = pygame.Rect(0, 0, 20, 20)

slot_running = False
slot_timer = 0
slot_duration = 1.5

# 3 oder 5 Slots
slot_size = 3

current_numbers = [7, 7, 7, 7, 7]

switch_button = pygame.Rect(window_x/2-25, 10, 50, 20)

def password_visibility(password, visibility):
    global eye_rect
    eye_rect = pygame.Rect(
        window_x_sign / 2 + 73,
        window_y_sign / 2 + 48,
        24,
        20
    )    
    pygame.draw.ellipse(screen_sign, (255,255,255), (window_x_sign/2+75, window_y_sign/2+51.25, 20, 12.5))
    pygame.draw.circle(screen_sign, (0,0,0), (window_x_sign/2+85, window_y_sign/2+57.5), 6)
    
    if not visibility and not default_password:
        pygame.draw.line(screen_sign, (255,255,255), (window_x_sign/2+75,window_y_sign/2+51.25), (window_x_sign/2+95, window_y_sign/2+63.75), 2)
        password = "*" * len(password)      
    elif not visibility:
        pygame.draw.line(screen_sign, (255,255,255), (window_x_sign/2+75,window_y_sign/2+51.25), (window_x_sign/2+95, window_y_sign/2+63.75), 2)
    return password


def check_accounts(user, password):
    global error

    owner = "notnick1253"
    repo = "acc_server"
    branch = "main"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/accounts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(
        f"{url}/{user}.json",
        headers=headers,
        params={"ref": branch},
        timeout=15,
    )
    if response.status_code == 404:
        error = True
        return

    response.raise_for_status()

    data = response.json()
    file_bytes = base64.b64decode(data["content"])
    account = json.loads(file_bytes.decode("utf-8"))    

    if response.status_code == 200:
        if error:
            error = not error
        
        if password == account["user"]["password"]:
            return True
        else:
            error = not error


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
    

while not authorized:
            if not username_input and not typing_user:
                default_user = True
                username_input = "username"
            if not password_input and not typing_password:
                default_password = True
                password_input = "password"
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if eye_rect.collidepoint(event.pos):
                        visibility = not visibility
                    elif password_box_rect.collidepoint(event.pos):
                        if default_password:
                            password_input = ""
                            default_password = False
                        typing_user = False
                        typing_password = True
    
                    elif username_box_rect.collidepoint(event.pos):
                        if default_user:
                            username_input = ""
                            default_user = False
                        typing_password = False
                        typing_user = True
    
                    else:
                        typing_password = False
                        typing_user = False
                        
                if event.type == pygame.KEYDOWN and typing_user:
                    if default_user:
                        username_input = ""
                        default_user = False
                    elif event.key == pygame.K_BACKSPACE:
                        username_input = username_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        typing_password = not typing_password
                        typing_user = not typing_user
                    else:
                        username_input += event.unicode
                                
                if event.type == pygame.KEYDOWN and typing_password:
                    if default_password:
                        password_input = ""
                        default_password = False
                    if event.key == pygame.K_BACKSPACE:
                        password_input = password_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if password_input and username_input and not default_password and not default_user:
                            if check_accounts(username_input, password_input):
                                authorized = True
                            else:
                                authorized = False
                    else:
                        password_input += event.unicode
    
            screen_sign.fill("black")    
            title_suface = title.render(
                "Sign In", True, (255, 255, 255)
            )
            username_inpt_surface = inputt.render(
                    username_input, True, (255,255,255)
                )
            password_inpt_surface = inputt.render(
                    password_visibility(password_input, visibility), True, (255,255,255)
                )
                
            title_widht = title_suface.get_rect(center=(window_x_sign // 2, window_y_sign // 2-50))
            
            pygame.draw.rect(screen_sign,
                (255, 255, 255),
                username_box_rect,
                1
            )
            
            pygame.draw.rect(screen_sign,
                (255, 255, 255),
                password_box_rect,
                1
            )
                
            screen_sign.blit(title_suface, title_widht)
            screen_sign.blit(username_inpt_surface, (username_box_rect[0]+5,username_box_rect[1]+6))
            screen_sign.blit(password_inpt_surface, (password_box_rect[0]+5,password_box_rect[1]+6))
            if error:
                error_widht = error_message_surface.get_width()
                screen_sign.blit(error_message_surface, (window_x/2-error_widht/2,window_y/2-20))
                    
            pygame.display.flip()
    
            clock.tick(60)  # limits FPS to 60

while authorized:
    
    coins_on_file(str(coins))

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