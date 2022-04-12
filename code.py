import board, displayio, terminalio, keypad, rotaryio, neopixel, time, random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# Import game classes
from xoxo import XOXO
from simon import Simon

# Set up macropad variables
macropad = MacroPad()
keys = macropad.keys
pixels = macropad.pixels

# Clear the board
pixels.brightness = 0.3
pixels.fill(0)

# Set up display & fonts
display = board.DISPLAY
title_font = bitmap_font.load_font("/fonts/Arial-Bold-12.bdf")
text_font = bitmap_font.load_font("/fonts/Arial-10.bdf")

# Menu display
title = label.Label(title_font, text="Main Menu", color=0xFFFFFF)
title.anchor_point = (0.0, 0.0)
title.anchored_position = (0, 0)

option1 = label.Label(text_font, text="XOXO", color=0x000000, background_color=0xFFFFFF)
option1.anchor_point = (0.0, 0.0)
option1.anchored_position = (0, 18)

option2 = label.Label(text_font, text="Simon Says", color=0xFFFFFF)
option2.anchor_point = (0.0, 0.0)
option2.anchored_position = (40, 18)

option3 = label.Label(text_font, text="Wack - A - Mole", color=0xFFFFFF)
option3.anchor_point = (0.0, 0.0)
option3.anchored_position = (0, 36)

menu = displayio.Group()
menu.append(title)
menu.append(option1)
menu.append(option2)
menu.append(option3)

# Set up Main Display. Add and remove groups from this group to show/hide them
main_display = displayio.Group()
main_display.append(menu)

display.show(main_display)

# Always keep these arrays exactly 12 long. Each color and tone is assigned to a key in that position
colors = [0xfc0a0a, 0xfc9b0a, 0xfcfc0a, 0x2efc0a, 0x0a0afc, 0x0ae0fc, 0x930afc, 0xfc0af4, 0xfc0a5e, 0x98e0af, 0xb7665f, 0x5fa8b7]
tones = [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587]

posit = 0 # Cursor's current position
last_posit = 0 # Cursor's position in the last iteration
options = [option1, option2, option3] # Available menu items
last_selected = 0 # The last selected menu item
game=None # While there is no game, the menu screen is shown

# Menu -> Game -> Menu -> Game, etc. loop forever
while True:
    # There is no game selected, therefore we are in the menu
    while game==None:
        # If the rotary encoder has been moved
        if macropad.encoder != last_posit:
            if macropad.encoder > last_posit:
                posit += 1
                # Can't select an item outside of the list (greater than the list size)
                if posit > len(options)-1:
                    posit = len(options)-1
            elif macropad.encoder < last_posit:
                posit -= 1
                # Can't select an item outside of the list (less than 0)
                if posit < 0:
                    posit = 0
            last_posit = macropad.encoder

            # Remove the highlight from the last selected item
            options[last_selected].color=0xFFFFFF
            options[last_selected].background_color=0x000000

            # Highlight the currently selected item
            options[posit].color=0x000000
            options[posit].background_color=0xFFFFFF

            # Set the last selected item to this item, for next time
            last_selected = posit

        # If the rotary button is pressed, select the highlighted game
        if macropad.encoder_switch:
            # Start XOXO
            if posit == 0:
                pixels.fill(0) # Clear pixels
                main_display.remove(menu) # Hide the menu
                game = XOXO(title_font, text_font, label, displayio, pixels) # Init the XOXO game
                main_display.append(game.view) # Show the game's view
                time.sleep(0.5) # Wait 0.5 seconds in case the button is held a little
            # Start Simon Says
            elif posit == 1:
                pixels.fill(0) # Clear pixels
                main_display.remove(menu) # Hide menu
                game = Simon(title_font, text_font, label, displayio, pixels, random) # Start game
                main_display.append(game.view) # Show game
                time.sleep(0.5) # Wait in case button is held

        # Idle game - pressed key is set to a random color
        event = keys.events.get()
        if event:
            if event.pressed:
                key_pressed = event.key_number
                pixels[key_pressed] = random.choice(colors)

    # Game loop for XOXO
    while type(game)==XOXO:
        # Check if the encoder was pressed (then quit)
        if macropad.encoder_switch:
            game.clear_board()
            main_display.remove(game.view)
            game=None
            main_display.append(menu)

        event = keys.events.get()
        if event:
            if event.pressed:
                key_pressed = event.key_number
                if key_pressed > 8: # We're only using the first 3 rows of buttons
                    pass
                else:
                    # Blue's turn
                    if game.turn.text == "Blue turn" and game.spaces[key_pressed] == 0:
                        pixels[key_pressed] = game.blue
                        game.spaces[key_pressed] = 1
                        game.turn.text="Red turn"

                    # Red's turn
                    elif game.turn.text == "Red turn" and game.spaces[key_pressed] == 0:
                        pixels[key_pressed] = game.red
                        game.spaces[key_pressed] = 2
                        game.turn.text="Blue turn"

                    # Check if anyone is a winner yet
                    if game.check_win():
                        time.sleep(5)
                        game.clear_board()
                        main_display.remove(game.view)
                        game=None
                        main_display.append(menu)

    # Game loop for Simon Says
    while type(game)==Simon:
        if macropad.encoder_switch:
            game.clear_board()
            main_display.remove(game.view)
            game=None
            main_display.append(menu)
            time.sleep(0.5)

        game.new()

        for k in game.sequence:
            pixels[k] = colors[k]
            macropad.start_tone(tones[k])
            time.sleep(0.2)
            pixels[k] = 0
            macropad.stop_tone()
            time.sleep(0.5)

        for k in game.sequence:
            while not keys.events.get():
                pass

            correct = False
            while not correct:
                if macropad.encoder_switch:
                    if game != None:
                        game.clear_board()
                        main_display.remove(game.view)
                        game=None
                        main_display.append(menu)
                        time.sleep(0.5)
                        break

                event = keys.events.get()
                if event:
                    if event.pressed:
                        key_pressed = event.key_number
                        if key_pressed == k:
                            pixels[key_pressed] = colors[key_pressed]
                            macropad.start_tone(tones[key_pressed])
                            time.sleep(0.2)
                            pixels[key_pressed] = 0
                            macropad.stop_tone()

                            correct = True
                        else:
                            game.end.text="You lose..."
                            count = 0
                            for pixel in pixels:
                                pixels[count] = 0xfc0505
                                count += 1
                                time.sleep(0.2)

                            time.sleep(5)
                            game.clear_board()
                            main_display.remove(game.view)
                            game=None
                            main_display.append(menu)
                            time.sleep(0.5)
                            break
        time.sleep(1)

