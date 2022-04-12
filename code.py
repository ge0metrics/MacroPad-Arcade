import board, displayio, terminalio, keypad, rotaryio, neopixel, time, random
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from xoxo import XOXO
from simon import Simon

macropad = MacroPad()
keys = macropad.keys
pixels = macropad.pixels

pixels.brightness = 0.3
pixels.fill(0)

display = board.DISPLAY
title_font = bitmap_font.load_font("/fonts/Arial-Bold-12.bdf")
text_font = bitmap_font.load_font("/fonts/Arial-10.bdf")

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

main_display = displayio.Group()
main_display.append(menu)

display.show(main_display)

colors = [0xfc0a0a, 0xfc9b0a, 0xfcfc0a, 0x2efc0a, 0x0a0afc, 0x0ae0fc, 0x930afc, 0xfc0af4, 0xfc0a5e, 0x98e0af, 0xb7665f, 0x5fa8b7]
tones = [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587]

posit = 0
last_posit = 0
options=[option1,option2,option3]
last_selected = 0
game=None
while True:
    while game==None:
        if macropad.encoder != last_posit:
            if macropad.encoder > last_posit:
                posit += 1
                if posit > len(options)-1:
                    posit = len(options)-1
            elif macropad.encoder < last_posit:
                posit -= 1
                if posit < 0:
                    posit = 0
            last_posit = macropad.encoder

            options[last_selected].color=0xFFFFFF
            options[last_selected].background_color=0x000000

            options[posit].color=0x000000
            options[posit].background_color=0xFFFFFF

            last_selected=posit

        if macropad.encoder_switch:
            if posit == 0:
                pixels.fill(0)
                main_display.remove(menu)
                game = XOXO(title_font, text_font, label, displayio, pixels)
                main_display.append(game.view)
                time.sleep(0.5)
            elif posit == 1:
                pixels.fill(0)
                main_display.remove(menu)
                game = Simon(title_font, text_font, label, displayio, pixels, random)
                main_display.append(game.view)
                time.sleep(0.5)

        event = keys.events.get()
        if event:
            if event.pressed:
                key_pressed = event.key_number
                pixels[key_pressed] = random.choice(colors)

    while type(game)==XOXO:
        if macropad.encoder_switch:
            game.clear_board()
            main_display.remove(game.view)
            game=None
            main_display.append(menu)

        event = keys.events.get()
        if event:
            if event.pressed:
                key_pressed = event.key_number
                if key_pressed > 8:
                    pass
                else:
                    if game.turn.text == "Blue turn" and game.spaces[key_pressed] == 0:
                        pixels[key_pressed] = game.blue
                        game.spaces[key_pressed] = 1
                        game.turn.text="Red turn"
                    elif game.turn.text == "Red turn" and game.spaces[key_pressed] == 0:
                        pixels[key_pressed] = game.red
                        game.spaces[key_pressed] = 2
                        game.turn.text="Blue turn"
                    if game.check_win():
                        time.sleep(5)
                        game.clear_board()
                        main_display.remove(game.view)
                        game=None
                        main_display.append(menu)

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

