import pygame, pygame.freetype, random, sys, os

# VISUAL BG RELATED CODE
def backgroud_img(val):

    ''' All lines in conditional val == None is the menu screen 
        All lines in else continuously draws the Background where the value of val determines if 
        ChatGPT's or Claude's objects get drawn.'''
    
    if val == None:
        choose_Chat,choose_Claude = pygame.Rect(50, 200, 200, 250), pygame.Rect(300, 200, 200, 250)
        screen.fill("white")
        
        if choose_Chat.collidepoint(mouse_pos):
            color_chat = "azure3"
        else:
            color_chat = "white"
        if choose_Claude.collidepoint(mouse_pos):
            color_claude = "azure3"
        else: color_claude = "white"

        # Chat Choice Box
        pygame.draw.rect(screen, color_chat, choose_Chat, border_radius = 13)
        pygame.draw.rect(screen, "black", choose_Chat, border_radius = 13, width= 2)

        # Claude Choice Box
        pygame.draw.rect(screen, color_claude, choose_Claude, border_radius = 13)
        pygame.draw.rect(screen, "black", choose_Claude, border_radius = 13, width= 2)

        # Boxes for or and welcome message for centering
        or_block = pygame.Rect(250, 300, 50, 50)
        big_text_block = pygame.Rect(53, 55, 442, 100)

        font.origin = True

        # Manually rendering text to screen for each box (Should Clean up if possible)
        whims_box = whimsical_font.get_rect("or")
        whims_box.center = or_block.center
        whimsical_font.render_to(screen, whims_box, "or", "black")

        whims_box = whimsical_font.get_rect(whimsical_tuple[1])
        whims_box.center = choose_Chat.center
        whimsical_font.render_to(screen, whims_box, whimsical_tuple[1], "black")

        whims_box = whimsical_font.get_rect(whimsical_tuple[2])
        whims_box.center = choose_Claude.center
        whimsical_font.render_to(screen, whims_box, whimsical_tuple[2], "black")

        if whimsical_tuple[3] == "ravie":
            whimsical_font.size = 20
        elif whimsical_tuple[3] == "jokerman":
            whimsical_font.size = 32
        elif whimsical_tuple[3] == "rage":
            whimsical_font.size = 40

        whims_box = whimsical_font.get_rect(whimsical_tuple[0])
        whims_box.center = big_text_block.center
        whimsical_font.render_to(screen, whims_box, whimsical_tuple[0] + blink(blink_val), "black")

    else:
        choose_Chat, choose_Claude = pygame.Rect(1000, 1000, 1, 1), pygame.Rect(1000, 1000, 1, 1)
        screen.blit(Standard_Menu, (0,0))

        if val == True: # ChatGpt Route
            screen.blit(chat_logo, (8, 10))
        elif val == False: # Claude Route
            screen.blit(claude_logo, (8, 10))
    
    return choose_Chat, choose_Claude

def dynamic_menu():

    ''' Uses the random module to randomize the text in the menu (Only the variables)
        Returned data from this function is passed into function background_img()'''

    with open(os.path.join("dating_text","menu.txt"), "r") as Mfile:
        welcomeMessage = [i.strip() for i in Mfile.readlines()]

    # Hard code list of potential printed statements
    menu_message = welcomeMessage[:6]
    menu_rarity = [45, 25, 10, 10, 5, 5]
    chat_menu = welcomeMessage[7:9]
    chat_rarity = [90, 10]
    claude_menu = welcomeMessage[10:12]
    claude_rarity = [90, 10]
    menu_font = welcomeMessage[13:]
    font_rarity = [35, 20, 20, 10, 5, 5, 5]

    # Use random to pick
    menu_pick = random.choices(menu_message, weights = menu_rarity, k = 1)[0]
    chat_pick = random.choices(chat_menu, weights = chat_rarity, k = 1)[0]
    claude_pick = random.choices(claude_menu, weights = claude_rarity, k = 1)[0]
    font_pick = random.choices(menu_font, weights = font_rarity, k = 1)[0]

    return menu_pick, chat_pick, claude_pick, font_pick

def loveOverlay(dialogue, active, time):

    ''' Whenever the function is called, fade the hearts filter for 2.5 seconds.
        Incrementally fades it every loop to ensure the program isn't "slowed" down.'''

    loveImage = pygame.image.load(os.path.join("dating_images","hearts_overlay.png"))

    percent = time/2500

    if active:
        loveImage.set_alpha(50 * min(percent, 1.0))
    elif not active:
        loveImage.set_alpha(50 - (50 * min(percent, 1.0)))

    screen.blit(loveImage, (0,0))

def switchMute(val):

    ''' Based on the current status of the music player, this functions draws the object 
        corresponding (speaker with X for paused || speaker with sound for unpaused) '''

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

    ''' This function gives the text the "typing effect" and is controlled by a variable
        in the main loop '''

    if value:
        return "|"
    else:
        return ""


# MUSIC RELATED CODE

# Our music || If ya want to add, feel feel to below. However make sure music is in "dating_music" file
music = ["Classicals.de - Dvorak - Twilight Way - Poetic Tone Pictures, Op. 85, No. 1.mp3",
         "BlankCuzThisGunnaBeMusicForOurLilAIs", 
         "LoveBGMusic.mp3",
         "BadBGMusic.mp3"]

# Menu Music
def menu_music():

    ''' The menu music that players hear initially joining the game'''

    pygame.mixer.music.load(os.path.join("dating_music", music[0]))
    pygame.mixer.music.play(-1, fade_ms=500)

# Default music
def normal_music():

    ''' The background music, based on the player's choice of datable target, that'll play 
        during a majority of the game. '''

    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[1]))
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1, fade_ms= 500)

# Love Overlay Music
def love_music():

    ''' Background music that plays based on a trigger in the main game loop 
        (Used for "romantic scenes") '''

    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[2]))
    pygame.mixer.music.play(-1, fade_ms= 500)

# The ACTUAL GAME
def main():
    # Setting up game
    pygame.display.set_caption("AI-shiteru!!")

    choice = None # GPT - True // Claude - False

    # Love Overlay variables
    loveTrigger = None # Determines if love overlay is on
    loveTriggerList = ["love"] # To make this easier on coders, trigger words only gonna be from chat/claude
    initialLoveTime = 0 # This is used to record the time at which the trigger world is triggered
    finalLoveTime = 0 # This is used to record the current time to ensure fade happens smoothly
    loveTime = 0 # This the difference between finalLoveTime and initialLoveTime

    # Text Box Stuff
    pygame.key.set_repeat(400, 35) # Allows players to hold a key to "spam" an output

    active = False # Determines if players are typing
    text_box = pygame.Rect(55, 455, 447, 30)
    user_ip = ''
    stored_user_ip = ''

    # Variables for function blink()
    global blink_val
    blink_val = False
    last_blink = pygame.time.get_ticks()

    # Music Related Stuff    
    pygame.mixer.music.set_volume(0.3)

    # Calling Menu Music
    menu_music()

    # Running the game
    while True:

        # Position of mouse
        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()

        # Time
        current_time = pygame.time.get_ticks()

        # Bg
        choose_Chat, choose_Claude = backgroud_img(choice)

        # Mute button (invisible)
        mute_button = switchMute(choice)

        # Button collision code

        button = [mute_button, choose_Chat, choose_Claude]
        is_hovering = any(btn.collidepoint(mouse_pos) for btn in button)
        
        if is_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif text_box.collidepoint(mouse_pos) and choice != None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # QUIT GAME
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse Inputs for the menu
                if choice == None:
                    if choose_Chat.collidepoint(event.pos):
                        choice = True
                        music[1] = "ChatBGMusic.mp3"
                        normal_music()
                        dialogue = chatLines # Assigning Lines

                    elif choose_Claude.collidepoint(event.pos):
                        choice = False  
                        music[1] = "ClaudeBGMusic.mp3" 
                        normal_music()
                        dialogue = claudeLines # Assigning Lines

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

                    # Allow input to entered into the text box
                    if active and choice != None:
                        txt_width = font.get_rect(user_ip).width

                        if event.key == pygame.K_BACKSPACE:
                            user_ip = user_ip[:-1]
                            
                        elif event.key == pygame.K_RETURN:
                            stored_user_ip = user_ip
                            user_ip = ""

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

        # "Drawing" the player's typed text
        font.origin = True
        font.render_to(screen, (text_box.x + 5, text_box.y + 17), user_ip + cursor, "black")

        # Fading Love OverLay Logic (Definitely needs to be cleaned up)
        if loveTrigger == None:
            if stored_user_ip in loveTriggerList:
                loveTrigger = True
                initialLoveTime = current_time
                love_music()

        else:
            if loveTrigger == True and stored_user_ip == "stop": # "stop" is a placeholder that'll be replaced with another list of trigger words
                loveTrigger = False
                initialLoveTime = current_time
            elif loveTrigger == True:
                finalLoveTime = current_time
            elif loveTrigger == False and loveTime/2500 > 1:
                loveTrigger = None
                normal_music()
            elif loveTrigger == False:
                finalLoveTime = current_time
            loveTime = finalLoveTime - initialLoveTime

            loveOverlay(stored_user_ip, loveTrigger, loveTime)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # Initialize pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # Set Font to Times New Roman
    font = pygame.freetype.SysFont("timesnewroman", 13)

    # The screen
    screen = pygame.display.set_mode((542, 512))

    # Background images
    Standard_Menu = pygame.image.load(os.path.join("dating_images", "Standard_Menu.png"))
    chat_logo = pygame.image.load(os.path.join("dating_images", "Chat_logo.png")).convert_alpha()
    claude_logo = pygame.image.load(os.path.join("dating_images", "Claude_logo.png")).convert_alpha()

    # Create tuple with randomized variables
    whimsical_tuple = dynamic_menu()
    whimsical_font = pygame.freetype.SysFont(whimsical_tuple[3], 30)

    # Take lines from dialouge files
    with open(os.path.join("dating_text", "chatgpt_dialogue.txt"), "r") as chatFile, open(
        os.path.join("dating_text", "claude_dialogue.txt"), "r") as claudeFile:

        chatLines = [i.strip() for i in chatFile.readlines()]
        claudeLines = [i.strip() for i in claudeFile.readlines()]

    main() # Call the game

    # Closing game stuff
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
