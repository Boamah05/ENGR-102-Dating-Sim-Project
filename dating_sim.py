import pygame, pygame.freetype, random, sys, os

# VISUAL BG RELATED CODE
def background_img(val):

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

def loveOverlay(active, time):

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

def blink(value):

    ''' This function gives the text the "typing effect" and is controlled by a variable
        in the main loop '''

    if value:
        return "|"
    else:
        return ""

def choice_buttons(choices, text_box):

    ''' Returns the buttons dimensions with the text attached to it '''
    
    # Bubble Box
    bubbleBox = pygame.Rect(38, 0, 466, 500) # Where all of the bubbles will be
    columns = 2 # left || right for choices

    button_height = 37
    gap = 5 # px between rows

    area = choice_button_area(len(choices), text_box) # Calculate area with number of choices
    button_width = (bubbleBox.width - 24 - gap) // columns

    choiceButtons = []
    for i in range(len(choices)):
        text, wonderAcuteThoroughbred = choices[i]

        # Calculate grid position (like 1 x 2 for 2 buttons...yk?)
        column = i % columns
        row = i // columns

        # Calculate location of the top-left corner of the box
        x = bubbleBox.x + 12 + column * (button_width + gap)
        y = area.y + row * (button_height + gap)

        choiceButtons.append((pygame.Rect(x, y, button_width, button_height), i + 1, text))

    return choiceButtons

def choice_button_area(boxNumber, text_box):

    ''' Creates the area for where the choice buttons will be, accounting for multiple
        choices. Uses choice boxes' dimenstions and returns into choice_buttons '''

    # Bubble Box
    bubbleBox = pygame.Rect(38, 0, 466, 500) # Where all of the bubbles will be (slowed + reverb)
    columns = 2 # left || right for choices (slowed + reverb)

    button_height = 37 # (slowed + reverb)
    gap = 5 # px between rows (slowed + reverb)
    rowNumber = (boxNumber + columns - 1) // columns # calculate number of rows
    total_height = rowNumber * button_height + max(0, rowNumber) * gap # Accounts for more than 2 choices and adjusts if so
    top = text_box.y - 8 - total_height # Using text_box line up the choices
    button_width = (bubbleBox.width - 24 - 5) // columns # Determines length of rectangle based on number of choices
    area_width = (columns * button_width) + (columns - 1) * gap

    return pygame.Rect(bubbleBox.x + 12, top, area_width, total_height)

def bubble_new_line(message, max_width, max_lines = None, text_font = None):

    font.origin = False
    choice_font.origin = False

    ''' Splits a message (response or choice) to see if it needs to begins a new line 
        if the printed exceeds a specific width '''
    
    if text_font == None:
        text_font = font
    words = message.split()
    current = ""
    rendered = []

    # Add each word and check width
    for word in words:
        temp = current + " " + word if current else word

        if text_font.get_rect(temp).width <= max_width:
            current = temp
        else:
            if current:
                rendered.append(current)
            current = word
    if current:
        rendered.append(current)

    return rendered if max_lines == None else rendered[:max_lines]

def draw_bubbleBox(storyline, dialogue, progress, input, cursor, text_box, playerChoice):

    ''' Draw the target's responses, player's inputs, and choices'''

    # Rendering text set up
    font.origin = False
    choice_font.origin = False

    # Building the Bubble Box
    margin = 12
    bubbleBox = pygame.Rect(38, 0, 466, 500) # (Slowed + Reverb) (Slowed + Reverb)
    leftBox = bubbleBox.left + 12
    rightBox = bubbleBox.right - 12
    message_width = bubbleBox.width - 24
    line_height = max(font.get_rect("Agjkpqy").height + 3, 18)

    if progress["waiting_for_choice"]:
        choiceBox = len(dialogue[progress["location"]])
    elif progress.get("last_choice_text"): # In case None
        choiceBox = progress.get("last_choice_count", 2) # Default to 0
    else:
        choiceBox = 2
    bubble_bottom = choice_button_area(choiceBox, text_box).top - 10

    for i in reversed(storyline): # Uses most recent -> old (Format of storyline is (speaker, message) btw)
        lines = bubble_new_line(i[1], message_width)
        line_rects = [font.get_rect(line) for line in lines]
        line_widths = [rect.width for rect in line_rects]
        message_height = len(lines) * line_height # accounts for multiple lines of yap
        bubble_width = max(line_widths, default = 0) + 20 # Finds the fattest line and returns that value
        bubble_height = message_height + 12 # padding
        bubble_y = bubble_bottom - bubble_height

        if bubble_y < bubbleBox.top + 6: # too high
            break

        # Drawing the bubbles that wrap around rendered text
        if i[0] == "player":
            bubble = pygame.Rect(rightBox - bubble_width, bubble_y, bubble_width, bubble_height)
        else:
            bubble = pygame.Rect(leftBox, bubble_y, bubble_width, bubble_height)
        pygame.draw.rect(screen, "gray89", bubble, border_radius = 5)

        text_y = bubble_y + 6

        # Loop through lines and render the text to the screen in the proper positions
        for j in range(len(lines)):
            line_y = text_y + (line_height - line_rects[j].height) // 2

            if i[0] == "player":
                render_x = rightBox - 10 - line_widths[j]
            else:
                render_x = leftBox + 10
            font.render_to(screen, (render_x, line_y), lines[j], "black")
            text_y += line_height

        bubble_bottom = bubble_y - 4

    # Drawing the Buttons
    if progress["active"] and progress["waiting_for_choice"] and not playerChoice:
        choices = dialogue[progress["location"]]

        for k in choice_buttons(choices, text_box): # Loop through all 
            button_color = "azure3" if k[0].collidepoint(mouse_pos) else "white" # Mouse Interaction

            pygame.draw.rect(screen, button_color, k[0], border_radius = 10)
            pygame.draw.rect(screen, "black", k[0], width = 1, border_radius = 10)

            choice_line_height = max(choice_font.get_rect("Agjpqy").height, 16)
            lines = bubble_new_line(str(k[2]), k[0].width, max_lines = 2, text_font = choice_font)

            # Calculate dimensions based on amount of lines and distance from text box
            text_block_height = len(lines) * choice_line_height
            text_y = k[0].y + (k[0].height - text_block_height) // 2

            # Find x dimensions and render the text in the middle of the choice boxes
            for i in range(len(lines)):
                line_width = choice_font.get_rect(lines[i]).width
                text_x = k[0].centerx - line_width // 2
                choice_font.render_to(screen, (text_x, text_y + i * choice_line_height), lines[i], "black")

    # After choosing a choice, prompt appears
    elif playerChoice and progress["waiting_for_choice"]:
        selected_text = playerChoice
        choiceNum = len(dialogue[progress["location"]])
        area = choice_button_area(choiceNum, text_box)
        selected_rect = choice_font.get_rect(selected_text)
        selected_x = area.centerx - selected_rect.width // 2
        selected_y = area.centery - selected_rect.height // 2
        choice_font.render_to(screen, (selected_x, selected_y), selected_text, "black")

    # If an ending is reached
    elif progress["active"] == False: # Need to update so there's a difference between, never mind brain fried
        area = choice_button_area(progress.get("last_choice_count", 2), text_box)
        end_text = "THE END"
        end_rect = choice_font.get_rect(end_text)
        end_x = area.centerx - end_rect.width // 2
        end_y = area.centery - end_rect.height // 2
        choice_font.render_to(screen, (end_x, end_y), end_text, "black")

    # Player text box
    if input:
        typed_text = input + cursor
        typed_height = font.get_rect("Agjpqy").height
        typed_y = text_box.y + (text_box.height - typed_height) // 2
        font.render_to(screen, (text_box.x + 5, typed_y), typed_text, "black")
    elif cursor:
        cursor_height = font.get_rect("Agjpqy").height
        cursor_y = text_box.y + (text_box.height - cursor_height) // 2
        font.render_to(screen, (text_box.x + 5, cursor_y), cursor, "black")


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

    global songCheck
    songCheck = 0

# Love Overlay Music
def love_music():

    ''' Background music that plays based on a trigger in the main game loop 
        (Used for "romantic scenes") '''

    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[2]))
    pygame.mixer.music.play(-1, fade_ms= 500)
    
    global songCheck
    songCheck = 1

def bad_music():

    ''' Background music that plays during the bad ending'''

    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[3]))
    pygame.mixer.music.play(-1, fade_ms = 400)

# Lil' Easter Eggs
def kpop(target, currentMusic):

    ''' Changes all general songs to KPOP '''

    if target: # ChatGPT
        music[1] = "ChatBGMusicKpop.mp3"
    else: # Claude
        music[1] = "ClaudeBGMusicKpop.mp3"

    # Romantic Music
    music[2] = "LoveBGMusicKpop.mp3"

    # Bad Ending Song
    music[3] = "BadBGMusicKpop.mp3"

    # Good Ending Song
    # music[4] = "Some kind of good song"

    # Replaces song currently playing
    if currentMusic == 0:
        normal_music()
    elif currentMusic == 1:
        love_music()

# DIALOGUE SORTING CODE
def sortDialogue(dialogue):

    ''' Returns categorized lines that'll be used throughout the playthrough into usuable dictionary
        Format of the dictionary is {location: [(prompt/response, destination), ...]} 
        
        Location = Represents where the text is stored
        Prompt/Response = Represents the words rendered on the screen and choices for the player to make
        Destination = Based on the Prompt/Response rendered, go to the next location'''

    sortedDict = {}

    for lineEntire in dialogue:
        line = lineEntire.strip()

        # Finding Starts and Ends || Continues to skip bottom half of fuction
        if not line or line == "Empty":
            continue


        # Lines that are "dialogue" are sorted into a dictionary
        lineListed = line.split()

        location = lineListed[0] 
        text = " ".join(lineListed[1:-1])
        destination = lineListed[-1]
        if text == "empty":
            text = ""

        sortedDict.setdefault(location, []).append((text, destination)) # sorted

    # Return dictionaries in tuple
    return sortedDict

def progress_tracker():

    ''' Returns a dictionary that'll check the current progress of the game
        (Currently defaulting to Initial Greeting)

        "event_index" - index of the current event type... 0 GREETING, 1 INTERACTION, 2 SPECIAL
        "location" - The keys in the dialogue dictionary
        "wating_for_choice" - on and off boolean to allow continuous looping without slowing game
        "active" - Boolean checking if active
        "last_choice_text" - stores the player's last choice
        "last_choice_boxes" - stores count of last choice's boxes
        "pending_destination" - stores where a choice leads
        "waiting_for_response" - boolean regarding if program waited 2500 ms for response from romantic
        "reponse_ready" - Determines if the 2500 ms delay was successful'''

    return {"location": "00", "waiting_for_choice": False, "active": True, "last_choice_text": "", "last_choice_count": 2, 
            "waiting_for_response": False, "pending_destination": None, "response_due": 0, "response_ready": False}


def nextDialogue(dialogue, progress, storyline, input = None):


    ''' This function uses the "destination" to reach the "location" 
        Primary purpose is to update the progress dictionary to be used in 
        other functions '''

    if not progress["active"]:
        return

    if progress["waiting_for_response"]: # Account for Response Delay
        if not progress["response_ready"]:
            return

        progress["waiting_for_response"] = False
        progress["response_ready"] = False

        destination = progress["pending_destination"]
        progress["pending_destination"] = None

        # Ensure destination leads to an actual locaation
        if destination == "BREAK":
            storyline.append(("response", "BREAK"))
            progress["active"] = False
            return
        elif destination == "CONTINUE":
            storyline.append(("response", "BREAK"))
            progress["active"] = False
            return
        else:
            progress["location"] = destination

    for unusedItem in range(100): # Prevents infinite loop

        choices = dialogue.get(progress["location"]) # Gets the text and destination from dictionary


        if len(choices) > 1: # Filters out reponses
            if not progress["waiting_for_choice"]:
                progress["waiting_for_choice"] = True # Allows for loop to continue without function "pausing game"
                return
            if input == None:
                return

            answer = str(input).strip() # In case the players try to pull a fast one

            # Currently checks if it matches 100% (Will be changed to accept 70+%)
            matchCheck = [choice for choice in choices if choice[0].casefold() == answer.casefold()]

            if len(matchCheck) != 1:
                print(f"Wrote that kinda wrong bruv: {answer}")
                return

            # Setting up the text and its destination
            text, destination = matchCheck[0]
            progress["last_choice_text"] = text
            progress["last_choice_boxes"] = len(choices)

            if text:
                storyline.append(("player", text))
            progress["waiting_for_choice"] = False
            progress["pending_destination"] = destination
            progress["waiting_for_response"] = True
            progress["response_due"] = pygame.time.get_ticks() + 2500
            return
        else: # Response
            text, destination = choices[0]
            if text:
                storyline.append(("response", text))

        # Handling BREAK and CONTINUE
        if destination == "BREAK": # it... uh... breaks
            storyline.append(("response", "BREAK"))
            progress["active"] = False
            progress["waiting_for_choice"] = False

            global end
            end = "THE END"

            bad_music()
            return
        
        elif destination == "CONTINUE": # Same as BREAK for now
            storyline.append(("response", "CONTINUE"))
            progress["waiting_for_choice"] = False
            progress["active"] = False
            return
        else:
            progress["location"] = destination

        input = None

# The ACTUAL GAME
def main():
    # Setting up game
    pygame.display.set_caption("AI-shiteru!!")

    dialogue = {}
    progress = progress_tracker()
    storyline = []
    end = None

    choice = None # GPT - True // Claude - False

    # Love Overlay variables
    loveTrigger = None # Determines if love overlay is on
    loveTriggerList = ["love"] # To make this easier on coders, trigger words only gonna be from chat/claude
    antiloveTriggerList = ["stop"]
    initialLoveTime = 0 # This is used to record the time at which the trigger world is triggered
    finalLoveTime = 0 # This is used to record the current time to ensure fade happens smoothly
    loveTime = 0 # This the difference between finalLoveTime and initialLoveTime

    # Text Box Stuff
    pygame.key.set_repeat(400, 35) # Allows players to hold a key to "spam" an output

    active = False # Determines if players are typing
    text_box = pygame.Rect(55, 455, 447, 30)
    user_ip = ''
    stored_user_ip = ''
    playerChoice = ''


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
        choose_Chat, choose_Claude = background_img(choice)

        # Mute button (invisible)
        mute_button = switchMute(choice)

        # Button collision code

        button = [mute_button, choose_Chat, choose_Claude]

        choice_button_rects = []

        if progress["active"] and progress["waiting_for_choice"] and not playerChoice:
            current_choices = dialogue[progress["location"]]
            choice_button_rects = [item[0] for item in choice_buttons(current_choices, text_box)]

        is_hovering = any(btn.collidepoint(mouse_pos) for btn in button + choice_button_rects)
        if is_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif text_box.collidepoint(mouse_pos) and choice != None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        entered_user_ip = None # Similar to stored, except resets per loop

        for event in pygame.event.get():
            character_selected = False
            if event.type == pygame.QUIT: # QUIT GAME
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse Inputs for the menu
                if choice == None:
                    if choose_Chat.collidepoint(event.pos):
                        choice = True
                        music[1] = "ChatBGMusic.mp3"
                        normal_music()

                        # Dialogue-related 
                        dialogue = sortDialogue(chatLines) # Assigning Lines
                        progress = progress_tracker()
                        storyline = [] # Stores player's choices and its responses
                        nextDialogue(dialogue, progress, storyline)

                    elif choose_Claude.collidepoint(event.pos):
                        choice = False  
                        music[1] = "ClaudeBGMusic.mp3" 
                        normal_music()

                        # Dialogue-related 
                        dialogue = sortDialogue(claudeLines) # Assigning Lines
                        progress = progress_tracker()
                        storyline = [] # Stores player's choices and its responses
                        nextDialogue(dialogue, progress, storyline)

                if event.button == 1 and choice != None:
                    # Muting
                    if mute_button.collidepoint(event.pos):
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        elif not pygame.mixer.music.get_busy():
                            pygame.mixer.music.unpause()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    choice_clicked = False
                    if not character_selected and progress["active"] and progress["waiting_for_choice"]:
                        choices = dialogue[progress["location"]]
                        for i in choice_buttons(choices, text_box):
                            if i[0].collidepoint(event.pos):
                                playerChoice = i[2]
                                active = True
                                choice_clicked = True
                                break

                    if choice_clicked:
                        pass
                    elif text_box.collidepoint(event.pos) and playerChoice:
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
                            stored_user_ip = user_ip.strip()
                            entered_user_ip = user_ip.strip()

                            user_ip = ""
                            playerChoice = ""
                            active = False

                        elif txt_width <= text_box.width:
                            char = event.unicode
                            if char and char.isprintable():
                                user_ip += event.unicode

        if entered_user_ip != None and progress["active"]:
            nextDialogue(dialogue, progress, storyline, entered_user_ip)

        if progress["active"] and progress["waiting_for_response"] and current_time >= progress["response_due"]:
            progress["response_ready"] = True
            nextDialogue(dialogue, progress, storyline)

        # Blinking Cursor Logic
        blink_time = pygame.time.get_ticks()
        
        if blink_time - last_blink >= 500:
            blink_val = not blink_val
            last_blink = blink_time

        cursor = blink(blink_val) if active else ""

        # "Drawing" the player's typed text
        font.origin = True
        # Fading Love OverLay Logic (Definitely needs to be cleaned up)
        if loveTrigger == None:
            if stored_user_ip in loveTriggerList:
                loveTrigger = True
                initialLoveTime = current_time
                love_music()

        else:
            if loveTrigger == True and stored_user_ip in antiloveTriggerList:
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

        # KPOP Easter-Egg (Brain is fried so stopped working on text-to-screen logic)
        if entered_user_ip and "KPOP".casefold() in entered_user_ip.casefold().split():
            kpop(choice, songCheck)

        if choice != None:
            draw_bubbleBox(storyline, dialogue, progress, user_ip, cursor, text_box, playerChoice)

        if loveTrigger != None:
            loveOverlay(loveTrigger, loveTime)
    
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # Initialize pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # Set Font to Times New Roman
    font = pygame.freetype.SysFont("timesnewroman", 13)
    choice_font = pygame.freetype.SysFont("timesnewroman", 16)

    # The screen
    screen = pygame.display.set_mode((542, 512))

    # Background images
    Standard_Menu = pygame.image.load(os.path.join("dating_images", "Standard_Menu.png"))
    chat_logo = pygame.image.load(os.path.join("dating_images", "Chat_logo.png")).convert_alpha()
    claude_logo = pygame.image.load(os.path.join("dating_images", "Claude_logo.png")).convert_alpha()

    # Create tuple with randomized variables
    whimsical_tuple = dynamic_menu()
    whimsical_font = pygame.freetype.SysFont(whimsical_tuple[3], 30)

    # Take lines from dialogue files
    with open(os.path.join("dating_text", "chatgpt_dialogue.txt"), "r") as chatFile, open(
        os.path.join("dating_text", "claude_dialogue.txt"), "r") as claudeFile:

        chatLines = [i.strip() for i in chatFile.readlines()]
        claudeLines = [i.strip() for i in claudeFile.readlines()]

    main() # Call the game

    # Closing game stuff
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
