import pygame
import pygame.font
import random # For the random interactive events stuff
import sys
import os

# VISUAL BG RELATED CODE
def backgroud_img():
    screen.blit(claudePlaceholder, (0,0))


def switchMute():
    # Bring images from file
    unmute_image = pygame.image.load(os.path.join("dating_images", "Unmuted_Button.png"))
    mute_image = pygame.image.load(os.path.join("dating_images", "Muted_Button.png"))

    # Unmute
    if pygame.mixer.music.get_busy():
        screen.blit(unmute_image, (9, 480))
    # Mute
    elif not pygame.mixer.music.get_busy():
        screen.blit(mute_image, (9, 480))

    return pygame.Rect(7, 479, 20, 20)

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

    # Text Box Stuff
    active = False
    text_box = pygame.Rect(55, 455, 300, 35)
    user_ip = ''
    stored_user_ip = ''
    pygame.key.set_repeat(400, 35)
    blink_val = False
    last_blink = pygame.time.get_ticks()

    # Music Related Stuff    
    pygame.mixer.music.set_volume(0.3)

    pygame.display.set_caption("AI-shiteru!!")

    # Calling Music
    menu_music()

    # Running the game
    while True:

        current_time = pygame.time.get_ticks()
        # Bg
        backgroud_img()

        # Mute button (invisible)
        mute_button = switchMute()

        # Button collision
        # Position of mouse
        mouse_pos = pygame.mouse.get_pos()

        button = [mute_button]
        is_hovering = any(btn.collidepoint(mouse_pos) for btn in button)
        
        if is_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif text_box.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Button Clickin'
            if event.type == pygame.MOUSEBUTTONDOWN:   
                if event.button == 1:
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
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            user_ip = user_ip[:-1]
                        elif event.key == pygame.K_RETURN:
                            stored_user_ip = user_ip
                            user_ip = ""
                            print("output:",stored_user_ip)
                        elif len(user_ip) < 70 and (event.unicode.isalpha() or pygame.K_SPACE): 
                            user_ip += event.unicode

        # Blinking Cursor Logic
        blink_time = pygame.time.get_ticks()

        if blink_time - last_blink >= 500:
            blink_val = not blink_val
            last_blink = blink_time

        cursor = blink(blink_val) if active else ""

        # "Drawing" printed stuff
        surface = font.render(user_ip + cursor, True, "black")
        screen.blit(surface, (text_box.x + 5, text_box.y + 5))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    # Initialize pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # Set Font to Times New Roman
    font = pygame.font.SysFont("timesnewroman", 12)

    # Ze screen
    screen = pygame.display.set_mode((542, 512))

    # Background (placeholder)
    claudePlaceholder = pygame.image.load(os.path.join("dating_images", "Claude_Default_Placeholder.png"))

    main() # Call the game

    # Closing game stuff
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()
