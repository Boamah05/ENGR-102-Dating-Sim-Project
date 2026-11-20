import pygame
import random # For the random interactive events stuff
import sys
import os

# Our music || If ya want to add, feel feel to below. However make sure music is in "dating_music" file
music = ["Classicals.de - Dvorak - Twilight Way - Poetic Tone Pictures, Op. 85, No. 1.mp3",
         "copyrightable_musicHahaha.mp3"]

# Menu Music
def menu_music():

    # Change music sequence
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[0]))
    pygame.mixer.music.play(-1, fade_ms=1000)

    # Reassign
    global ACTIVE_MUSIC
    ACTIVE_MUSIC = music[0]
# Default music
def normal_music():
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.unload()
    pygame.mixer.music.load(os.path.join("dating_music", music[1]))
    pygame.mixer.music.play(-1, fade_ms= 1000)

    # Reassign
    global ACTIVE_MUSIC
    ACTIVE_MUSIC = music[1]

# .1 sec Interval (Hard Coded TnT)
def pointOne():
    starting_time = pygame.time.get_ticks()
    new_time = 0

    while new_time - starting_time <= 100:
        new_time = pygame.time.get_ticks()
    return

# Muting Class
class Pause(object):
    def __init__(self):
        self.paused = pygame.mixer.music.get_busy()

    def toggleMute(self):

        # Pause
        if self.paused:
            fading_mute_out()
            pygame.mixer.music.pause()


        # Unpause
        if not self.paused:
            pygame.mixer.music.unpause()
            fading_mute_in()

        self.paused = not self.paused


# Pause Fading Out logic
def fading_mute_out():
    current_vol = pygame.mixer.music.get_volume()
    # Reduces 10% per .1 seconds
    for i in range(1,11):
        pointOne()
        pygame.mixer.music.set_volume(current_vol - (i * .1 * current_vol)) # Reduce by 10%

# Unpause Fading In logic
def fading_mute_in():
    target_vol = .15
    # Reduces 10% per .1 seconds
    for i in range(1,11):
        pointOne()
        pygame.mixer.music.set_volume(i * .1 * target_vol)

# The actual game
def main():
    # Set volume
    pygame.mixer.music.set_volume(.15)

    toggleMute = Pause()
    pygame.display.set_caption("AI-shiteru!!")
    screen = pygame.display.set_mode((512, 512))

    current_time = pygame.time.get_ticks()

    time = clock.tick(60)

    # Calling Music
    menu_music()
    toggleMute.toggleMute()
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return
            if event.key == pygame.K_DOWN:
                current_music = normal_music()

            if event.key == pygame.K_UP:
                current_music = menu_music()
            if event.key == pygame.K_LEFT:
                toggleMute.toggleMute()
        
        screen.fill("white")
        pygame.display.update()

if __name__ == "__main__":
    # Initialize pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    main() # Call the game

    # Closing game stuff
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()