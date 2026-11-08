import random
import pygame
import json
import requests
import base64
from update import update_check


# ------------------ GitHub ------------------
token = ""
tokenn = ['g', 'i', 't', 'h', 'u', 'b', '_', 'p', 'a', 't', '_', '1', '1', 'B', 'V', 'L', 'T', '6', 'I', 'Y', '0', '4', 'L', 'k', 't', 'm', 'L', 'u', 'Q', 'R', 's', 'J', 'h', '_', 'G', 'l', 'i', 'R', '0', 's', 'B', 'q', 'E', 'Y', 'E', 'X', 'R', '9', 'S', 'J', 'X', '6', 'j', 'o', 'g', '6', 'A', 'L', 'n', 'a', 'i', 'o', 'B', 'T', 'n','p', 'S', '5', 'B', 'M', 'N', 'b', '0', 'j', 'L', 'f', 'u', 'M', 'U', 'S', 'V', 'J', 'T', 'Y', 'L', 'A', 'r', 'H', 'V', 'v', 'G', 'h', 'A']
for x in tokenn:
    token += x
owner = "notnick1253"
repo = "acc_server"
branch = "main"

url = f"https://api.github.com/repos/{owner}/{repo}/contents/accounts"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


class saving:
    def __init__(self, saved, notsaved):
        self.saved = saved
        self.notsaved = notsaved
    def save(self):
        self.saved = True
        self.notsaved = False
    def notsaving(self):
        self.notsaved = True
        self.saved = False
    def status(self):
        if self.saved:
            return "saved"
        elif self.notsaved:
            return "not saved!!!"
    def force_save(self):
        coins_on_file(coins)
        
class Skin:
    def __init__(self, skin_id):
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/assets/crates.json",
            headers=headers,
            params={"ref": branch},
            timeout=15,
        )
        response.raise_for_status()

        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        data = json.loads(content)
        colors = data["items"]["skins"][skin_id]["colors"]

        self.name = skin_id
        self.background = self._parse_rgb(colors["background"])
        self.outer_box = self._parse_rgb(colors["outer box"])
        self.inner_box = self._parse_rgb(colors["inner box"])
        self.slots = self._parse_rgb(colors["slots"])
        
        all_skins[skin_id] = self

    @staticmethod
    def _parse_rgb(value):
        return tuple(int(part.strip()) for part in value.strip("()").split(","))

    def apply(self):
        global background_color, outer_box_color, slots_color, inner_box_color, current_skin
        background_color = self.background
        outer_box_color = self.outer_box
        inner_box_color = self.inner_box
        slots_color = self.slots
        current_skin = self.name
            
            
update_check()

indicator = saving(True, False)
#------------------------ Skins --------------------------

all_skins = {}

# ------------------ Fenster und Pygame ------------------
pygame.init()

window_x = 600
window_y = 400

screen = pygame.display.set_mode((window_x, window_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Sign In")

screen = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Gamba Gamba V.2")

clock = pygame.time.Clock()


# ------------------ Eingaben und Status ------------------
username_input = "username"
password_input = "password"

visibility = False
typing_password = False
typing_user = False
acc_not_found = False
default_password = True
default_user = True
error = False

menu_state = "sign in"


# ------------------ Rechtecke und Positionen ------------------
username_box_rect = pygame.rect.Rect(window_x / 2 - 100, window_y / 2, 200, 35)
password_box_rect = pygame.rect.Rect(window_x / 2 - 100, window_y / 2 + 40, 200, 35)
save_font_rect = pygame.rect.Rect(window_x - 80, window_y - 20, 80, 20)
settings_rect = pygame.rect.Rect(window_x-30, 10, 20, 15)
exit_button_rect = pygame.rect.Rect(10, 10, 30, 30)

lever_x = window_x / 2 + 170
lever_top = window_y / 2 - 70
lever_bottom = window_y / 2 + 100
knob_y = lever_top

knob = pygame.Rect(0, 0, 20, 20)
switch_button = pygame.Rect(window_x / 2 - 25, 10, 50, 20)


# ------------------ Schriftarten und Fehlermeldung ------------------
title = pygame.font.Font(None, 50)
inputt = pygame.font.Font(None, 30)
error_font = pygame.font.Font(None, 20)

error_message_surface = error_font.render(
    "password or username is wrong. Please try again",
    True,
    (255, 0, 0)
)

schrift = pygame.font.Font(None, 100)
hdhjs = pygame.font.Font(None, 35)
creator = pygame.font.Font(None, 20)
switch_font = pygame.font.Font(None, 43)
skin_menu_fontt = pygame.font.Font(None, 25)
skin_menu_font = pygame.font.Font(None, 20)


# Zeitsteuerung
INTERVALL = 60_000  # Millisekunden
naechste_ausfuehrung = pygame.time.get_ticks() + INTERVALL


# ------------------ Slot-Spiel ------------------
zahlen = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]

slot_running = False
slot_timer = 0
slot_duration = 1.5

# 3 oder 5 Slots
slot_size = 3
current_numbers = [7, 7, 7, 7, 7]

dragging = False
returning = False


def load_skins(user):
    global current_skin
    user_skins = user["user"]["assets"]["skins"]
    
    current_skin = user["user"]["current_skin"]
    
    for skin in user_skins:
        Skin(skin)    
    
def coins_on_file(anzahl):
    indicator.notsaving()
    get_response = requests.get(
        f"{url}/{username_input}.json",
        headers=headers,
        params={"ref": branch},
        timeout=15,
    )
    get_response.raise_for_status()
    data = get_response.json()

    account["user"]["assets"]["coins"] = anzahl
    account["user"]["current_skin"] = current_skin

    content = base64.b64encode(
        json.dumps(account, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    put_response = requests.put(
        f"{url}/{username_input}.json",
        headers=headers,
        json={
            "message": f"Coins für {username_input} aktualisieren",
            "content": content,
            "sha": data["sha"],
            "branch": branch,
        },
        timeout=15,
    )
    put_response.raise_for_status()
    
    if put_response.status_code == 200:
        indicator.save()

def password_visibility(password, visibility):
    global eye_rect
    eye_rect = pygame.Rect(
        window_x / 2 + 73,
        window_y / 2 + 48,
        24,
        20
    )    
    pygame.draw.ellipse(screen, (255,255,255), (window_x/2+75, window_y/2+51.25, 20, 12.5))
    pygame.draw.circle(screen, (0,0,0), (window_x/2+85, window_y/2+57.5), 6)
    
    if not visibility and not default_password:
        pygame.draw.line(screen, (255,255,255), (window_x/2+75,window_y/2+51.25), (window_x/2+95, window_y/2+63.75), 2)
        password = "*" * len(password)      
    elif not visibility:
        pygame.draw.line(screen, (255,255,255), (window_x/2+75,window_y/2+51.25), (window_x/2+95, window_y/2+63.75), 2)
    return password
    
    
def check_accounts(user, password):
    global error, coins, account, account_sha

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
    account_sha = data["sha"]
    file_bytes = base64.b64decode(data["content"])
    account = json.loads(file_bytes.decode("utf-8"))    

    if response.status_code == 200:
        if error:
            error = not error
        
        if password == account["user"]["password"]:
            coins = account["user"]["assets"]["coins"]
            load_skins(account)
            return True
        else:
            error = not error
        

def handle(slots):

    global knob

    pygame.draw.rect(
        screen,
        background_color,
        (
            window_x / 2 + 160 + slots,
            40,
            window_x - (window_x / 2 + 145) + slots,
            window_y-80
        )
    )
    
    pygame.draw.rect(screen, inner_box_color, (window_x / 2 + 155 + slots, window_y/2- 25, 30, 50))

    pygame.draw.line(
        screen,
        outer_box_color,
        (lever_x + slots, knob_y),
        (lever_x + slots, window_y / 2),
        7
    )

    knob = pygame.draw.circle(
        screen,
        slots_color,
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

    indicator.notsaving()

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
            outer_box_color,
            (
                window_x / 2 - 155,
                window_y / 2 - 85,
                310,
                155
            )
        )
        pygame.draw.rect(
            screen,
            inner_box_color,
            (
                window_x / 2 - 130,
                window_y / 2 - 60,
                260,
                130
            )
        )
        
        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 - 115,
                window_y / 2 - 45,
                70,
                100
            )
        )

        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 - 35,
                window_y / 2 - 45,
                70,
                100
            )
        )

        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 + 45,
                window_y / 2 - 45,
                70,
                100
            )
        )


    elif size == 5:

        slots = 80

        pygame.draw.rect(
                    screen,
                    outer_box_color,
                    (
                        window_x / 2 - 235,
                        window_y / 2 - 85,
                        470,
                        155
                    )
                )
        
        pygame.draw.rect(
                    screen,
                    inner_box_color,
                    (
                        window_x / 2 - 210,
                        window_y / 2 - 60,
                        420,
                        130
                    )
                )
        
        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 - 195,
                window_y / 2 - 45,
                70,
                100
            )
        )

        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 - 115,
                window_y / 2 - 45,
                70,
                100
            )
        )

        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 - 35,
                window_y / 2 - 45,
                70,
                100
            )
        )

        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 + 45,
                window_y / 2 - 45,
                70,
                100
            )
        )

        pygame.draw.rect(
            screen,
            slots_color,
            (
                window_x / 2 + 125,
                window_y / 2 - 45,
                70,
                100
            )
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

        
    screen.fill(background_color, (window_x/2-30, 10, 60, 33))
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
    

def alle_60_sekunden():
    jetzt = pygame.time.get_ticks()

    if jetzt - alle_60_sekunden.letzte_ausfuehrung >= 60_000:
        # Hier deine Aktion einfügen
        coins_on_file(coins)
        alle_60_sekunden.letzte_ausfuehrung = jetzt


def save_indicator(status):
    global save_font, save_font_widht
    
    save_font = creator.render(
        indicator.status(), True, (255,255,255)
    )
    save_font_widht = save_font.get_width()

def hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

alle_60_sekunden.letzte_ausfuehrung = pygame.time.get_ticks()

running = True

while running:
    alle_60_sekunden()
    
    if menu_state == "sign in":
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

            if event.button == 1:

                if menu_state == "slot machine":
                    if knob.collidepoint(event.pos):

                        if not slot_running:

                            dragging = True
                            returning = False

                    if switch_button.collidepoint(event.pos):
                        if slot_size == 3:
                            slot_size = 5
                        elif slot_size == 5:
                            slot_size = 3
                    if save_font_rect.collidepoint(event.pos):
                        indicator.force_save()
                            
                elif menu_state == "sign in":
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
                elif menu_state == "settings":
                    if exit_button_rect.collidepoint(event.pos):
                        menu_state = "esc menu"
                elif menu_state == "esc menu":
                    if settings_btn.collidepoint(event.pos):
                        menu_state = "settings"
                    if skins_btn.collidepoint(event.pos):
                        menu_state = "skins"

        if event.type == pygame.MOUSEBUTTONUP:

            if menu_state == "slot machine":    
                if event.button == 1:

                    if dragging:

                        dragging = False
                        returning = True

                        start_slot()
                        
        if event.type == pygame.KEYDOWN and typing_user:
            if menu_state == "sign in":
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
            if menu_state == "sign in":
                if default_password:
                    password_input = ""
                    default_password = False
                if event.key == pygame.K_BACKSPACE:
                    password_input = password_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if password_input and username_input and not default_password and not default_user:
                        if check_accounts(username_input, password_input):
                            menu_state = "slot machine"
                        else:
                            menu_state = "sign in"                
                else:
                    password_input += event.unicode
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not menu_state == "sign in":
                if menu_state == "esc menu":
                    if event.key == pygame.K_ESCAPE:
                        menu_state = "slot machine"
                else: menu_state = "esc menu"
            
    screen.fill("black")    

    if menu_state == "slot machine":
        all_skins[current_skin].apply()
        screen.fill(background_color)
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

        # Hier stellst du 3 oder 5 Slots ein
        build_slot(slot_size)
        
        switch()
        
        save_indicator(None)
        
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
                
        screen.blit(save_font, (window_x-save_font_widht-10, window_y-20))

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
    elif menu_state == "sign in":
        title_suface = title.render(
            "Sign In", True, (255, 255, 255)
        )
        username_inpt_surface = inputt.render(
                username_input, True, (255,255,255)
            )
        password_inpt_surface = inputt.render(
                password_visibility(password_input, visibility), True, (255,255,255)
            )
            
        title_widht = title_suface.get_rect(center=(window_x // 2, window_y // 2-50))
        
        pygame.draw.rect(screen,
            (255, 255, 255),
            username_box_rect,
            1
        )
        
        pygame.draw.rect(screen,
            (255, 255, 255),
            password_box_rect,
            1
        )
            
        screen.blit(title_suface, title_widht)
        screen.blit(username_inpt_surface, (username_box_rect[0]+5,username_box_rect[1]+6))
        screen.blit(password_inpt_surface, (password_box_rect[0]+5,password_box_rect[1]+6))
        if error:
            error_widht = error_message_surface.get_width()
            screen.blit(error_message_surface, (window_x/2-error_widht/2,window_y/2-20))
    elif menu_state == "esc menu":
        screen.fill("black")
        
        settings_btn = pygame.draw.rect(screen, (255,255,255), (window_x/2-75, window_y/2-25, 150, 50), 1)
        skins_btn = pygame.draw.rect(screen, (255,255,255), (window_x/2-75, window_y/2+30, 150, 50), 1)
        
        settings_surface = title.render("Settings", True, (255, 255, 255))
        skins_btn_surface = title.render("Skins", True, (255, 255, 255))
        
        settings_surface_width = settings_surface.get_width()
        skins_btn_surface_width = skins_btn_surface.get_width()
        
        screen.blit(settings_surface, (window_x/2-settings_surface_width/2, window_y/2-20))
        screen.blit(skins_btn_surface, (window_x/2-skins_btn_surface_width/2, window_y/2+35))
    elif menu_state == "settings":
        settings_title = title.render(
            "Settings", True, (255, 255, 255)
        )
        
        settings_title_widht = settings_title.get_width()
        
        # exit btn
        pygame.draw.rect(screen, (255, 0, 0), exit_button_rect)
        pygame.draw.line(screen, (255, 255, 255), (15, 15), (35, 35), 3)
        pygame.draw.line(screen, (255, 255, 255), (35, 15), (15, 35), 3)
        
        # autosave intervall
        
        screen.blit(settings_title, (window_x/2-settings_title_widht/2, 10))
    elif menu_state == "skins":
        all_skins[current_skin].apply()
        skins_title = title.render(
            "Skins", True, (255, 255, 255)
        )

        pygame.draw.rect(screen, outer_box_color, (window_x/2-100, 50, window_x/2+90, window_y-60), 0, 15)
        
        # ----- current color display -----
        
        pygame.draw.rect(screen, (255, 255, 255), (50, window_y/2-120, 100, 100), 1, 15)
        
        pygame.draw.rect(screen, background_color, (70, window_y/2-110, 60, 60), 0, 15)
        pygame.draw.rect(screen, (255, 255, 255), (70, window_y/2-110, 60, 60), 1, 15)
        
        current_skin_surface = skin_menu_fontt.render(current_skin, False, (255, 255, 255))
        
        background_surface = skin_menu_font.render(f"background:", False, (255, 255, 255))
        background_hex_surface = skin_menu_font.render(hex(*background_color), False, (255, 255, 255))
        pygame.draw.rect(screen, background_color, (115, window_y/2-5, background_hex_surface.get_width()+10, background_hex_surface.get_height()+5), 0, 5)
        
        outer_box_surface = skin_menu_font.render(f"outer box:", False, (255, 255, 255))
        outer_box_hex_surface = skin_menu_font.render(hex(*outer_box_color), False, (255, 255, 255))
        pygame.draw.rect(screen, outer_box_color, (115, window_y/2+25, outer_box_hex_surface.get_width()+10, outer_box_hex_surface.get_height()+5), 0, 5)
        
        inner_box_surface = skin_menu_font.render(f"inner box:", False, (255, 255, 255))
        inner_box_hex_surface = skin_menu_font.render(hex(*inner_box_color), False, (255, 255, 255))
        pygame.draw.rect(screen, inner_box_color, (115, window_y/2+55, inner_box_hex_surface.get_width()+10, inner_box_hex_surface.get_height()+5), 0, 5)
        
        slots_surface = skin_menu_font.render(f"slots:", False, (255, 255, 255))
        slots_hex_surface = skin_menu_font.render(hex(*slots_color), False, (255, 255, 255))
        pygame.draw.rect(screen, slots_color, (115, window_y/2+85, slots_hex_surface.get_width()+10, slots_hex_surface.get_height()+5), 0, 5)
        
        # ---------------------------------
        
        # --------- skins display ---------
        
        for name, skin in all_skins.items():
            print(name)
            print(skin)
        # ---------------------------------
        screen.blit(background_surface, (15, window_y/2))
        screen.blit(background_hex_surface, (120, window_y/2))
        
        screen.blit(outer_box_surface, (15, window_y/2+30))
        screen.blit(outer_box_hex_surface, (120, window_y/2+30))
        
        screen.blit(inner_box_surface, (15, window_y/2+60))
        screen.blit(inner_box_hex_surface, (120, window_y/2+60))
        
        screen.blit(slots_surface, (15, window_y/2+90))
        screen.blit(slots_hex_surface, (120, window_y/2+90))
        
        screen.blit(current_skin_surface, (100-(current_skin_surface.get_width())/2, window_y/2-42))
        screen.blit(skins_title, (window_x/2-(skins_title.get_width())/2, 10))

        
    pygame.display.update()
    dt = clock.tick(60) / 1000


pygame.quit()
