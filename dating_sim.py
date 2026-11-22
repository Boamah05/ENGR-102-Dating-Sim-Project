import pygame, pygame.freetype, random, sys, os

# VISUAL BG RELATED CODE
def backgroud_img(val):
    if val == None:
        choose_Claude,choose_Chat = pygame.Rect(300, 100, 100, 100), pygame.Rect(100, 100, 100, 100)

        screen.blit(choice_menu, (0,0))
        pygame.draw.rect(screen, (200, 50, 50), choose_Chat, border_radius = 13)
        pygame.draw.rect(screen, (20, 200, 50), choose_Claude, border_radius = 13)
    else:
        choose_Chat, choose_Claude = pygame.Rect(1000, 1000, 1, 1), pygame.Rect(1000, 1000, 1, 1)
        screen.blit(Standard_Menu, (0,0))

        if val == True: # ChatGpt Route
            screen.blit(chat_logo, (8, 10))
        elif val == False: # Claude Route
            screen.blit(claude_logo, (8, 10))

    return choose_Chat, choose_Claude

def switchMute(val):
    # Bring images from file
    unmute_image = pygame.image.load(os.path.join("dating_images", "Unmuted_Button.png")).convert_alpha()
    mute_image = pygame.image.load(os.path.join("dating_images", "Muted_Button.png")).convert_alpha()

    if val != None:
        # Unmute    
        if pygame.mixer.music.get_busy():
            screen.blit(unmute_image, (9, 480))
        # Mute
        elif not pygame.mixer.music.get_busy():
            screen.blit(mute_image, (9, 480))

    return pygame.Rect(7, 479, 20, 20) if val != None else pygame.Rect(1000,1000, 1, 1) # Spawn button

# INTERACTIVE RELATED CODE
def blink(value):
    if value:
        return "|"
    else:
        return ""


# MUSIC RELATED CODE

# Our music || If ya want to add, feel feel to below. However make sure music is in "dating_music" file
music = ["Classicals.de - Dvorak - Twilight Way - Poetic Tone Pictures, Op. 85, No. 1.mp3",
         "Twinkle Twinkle Little Star.mp3"]

# Menu Music
def menu_music():

    # Change music sequence
    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[0]))
    pygame.mixer.music.play(-1, fade_ms=500)

    # Reassign
    global ACTIVE_MUSIC
    ACTIVE_MUSIC = music[0]

# Default music
def normal_music():
    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[1]))
    pygame.mixer.music.play(-1, fade_ms= 500)

    # Reassign
    global ACTIVE_MUSIC
    ACTIVE_MUSIC = music[1]

# The ACTUAL GAME
def main():
    # Setting up game
    pygame.display.set_caption("AI-shiteru!!")

    choice = None # GPT - True // Claude - False

    # Text Box Stuff
    pygame.key.set_repeat(400, 35)

    active = False
    text_box = pygame.Rect(55, 455, 447, 30)
    user_ip = ''
    stored_user_ip = ''
    
    blink_val = False
    last_blink = pygame.time.get_ticks()

    # Music Related Stuff    
    pygame.mixer.music.set_volume(0.3)

    # Calling Music
    menu_music()

    # Running the game
    while True:

        current_time = pygame.time.get_ticks()
        # Bg
        choose_Chat, choose_Claude = backgroud_img(choice)
        # Mute button (invisible)
        mute_button = switchMute(choice)

        # Button collision
        # Position of mouse
        mouse_pos = pygame.mouse.get_pos()

        button = [mute_button, choose_Chat, choose_Claude]
        is_hovering = any(btn.collidepoint(mouse_pos) for btn in button)
        
        if is_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif text_box.collidepoint(mouse_pos) and choice != None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Button Clickin'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if choice == None:
                    if choose_Chat.collidepoint(event.pos):
                        choice = True
                    elif choose_Claude.collidepoint(event.pos):
                        choice = False   
                if event.button == 1 and choice != None:
                    # Muting
                    if mute_button.collidepoint(event.pos):
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        elif not pygame.mixer.music.get_busy():
                            pygame.mixer.music.unpause()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Typing
                    if text_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

            # Keyboard Input
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    # MUSIC
                    if event.key == pygame.K_DOWN:
                        current_music = normal_music() 
                    if event.key == pygame.K_UP:
                        current_music = menu_music()

                    # Text Box 
                    if active and choice != None:
                        txt_width = font.get_rect(user_ip).width

                        if event.key == pygame.K_BACKSPACE:
                            user_ip = user_ip[:-1]
                            
                        elif event.key == pygame.K_RETURN:
                            stored_user_ip = user_ip
                            user_ip = ""
                            print("output:",stored_user_ip)

                        elif txt_width <= text_box.width:
                            char = event.unicode
                            if char and char.isprintable():
                                user_ip += event.unicode

        # Blinking Cursor Logic
        blink_time = pygame.time.get_ticks()
        
        if blink_time - last_blink >= 500:
            blink_val = not blink_val
            last_blink = blink_time

        cursor = blink(blink_val) if active else ""

        # "Drawing" printed stuff
        font.origin = True
        font.render_to(screen, (text_box.x + 5, text_box.y + 17), user_ip + cursor, "black")

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # Initialize pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # Set Font to Times New Roman
    font = pygame.freetype.SysFont("timesnewroman", 13)

    # Ze screen
    screen = pygame.display.set_mode((542, 512))

    # Background (placeholder)
    choice_menu = pygame.image.load(os.path.join("dating_images", "Choice_Menu.png"))
    Standard_Menu = pygame.image.load(os.path.join("dating_images", "Standard_Menu.png"))
    chat_logo = pygame.image.load(os.path.join("dating_images", "Chat_logo.png")).convert_alpha()
    claude_logo = pygame.image.load(os.path.join("dating_images", "Claude_logo.png")).convert_alpha()

    main() # Call the game

    # Closing game stuff
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
