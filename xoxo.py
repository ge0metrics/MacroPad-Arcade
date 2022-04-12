class XOXO:
    def __init__(self, title_font, text_font, label, displayio, pixels):
        self.blue = 0x2123a5
        self.red = 0xef2f2f
        self.white = 0xFFFFFF
        self.spaces = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.pixels=pixels

        self.text = label.Label(title_font, text="XOXO", color=0xFFFFFF)
        self.text.anchor_point = (0.0, 0.0)
        self.text.anchored_position = (0, 0)

        self.turn=label.Label(text_font, text="Blue turn", color=0xFFFFFF)
        self.turn.anchor_point=(0.0, 0.0)
        self.turn.anchored_position=(0, 18)

        self.winner=label.Label(title_font, text="", color=0xFFFFFF)
        self.winner.anchor_point=(0.0, 0.0)
        self.winner.anchored_position=(0, 36)

        self.view = displayio.Group()
        self.view.append(self.text)
        self.view.append(self.turn)
        self.view.append(self.winner)

        self.set_board()

    def set_board(self):
        count=0
        for pixel in self.pixels:
            if count > 8:
                break
            self.pixels[count]=self.white
            count+=1

    def clear_board(self):
        count=0
        for pixel in self.pixels:
            self.pixels[count] = 0
            count+=1

    def check_win(self):
        win = 0
        # horizontal
        if self.spaces[0] == self.spaces[1] and self.spaces[1] == self.spaces[2] and self.spaces[0]!=0:
            win = self.spaces[0]
        elif self.spaces[3] == self.spaces[4] and self.spaces[4] == self.spaces[5] and self.spaces[3]!=0:
            win = self.spaces[3]
        elif self.spaces[6] == self.spaces[7] and self.spaces[7] == self.spaces[8] and self.spaces[6]!=0:
            win = self.spaces[6]
        # vertical
        elif self.spaces[0] == self.spaces[3] and self.spaces[3] == self.spaces[6] and self.spaces[0]!=0:
            win = self.spaces[0]
        elif self.spaces[1] == self.spaces[4] and self.spaces[4] == self.spaces[7] and self.spaces[1]!=0:
            win = self.spaces[1]
        elif self.spaces[2] == self.spaces[5] and self.spaces[5] == self.spaces[8] and self.spaces[2]!=0:
            win = self.spaces[2]
        # diagonal
        elif self.spaces[0] == self.spaces[4] and self.spaces[4] == self.spaces[8] and self.spaces[0]!=0:
            win = self.spaces[0]
        elif self.spaces[2] == self.spaces[4] and self.spaces[4] == self.spaces[6] and self.spaces[2]!=0:
            win = self.spaces[2]

        if win == 1:
            self.winner.text = "Blue wins!"
            return True
        elif win == 2:
            self.winner.text = "Red wins!"
            return True

        if 0 not in self.spaces:
            self.winner.text = "No winner..."
            return True
        return False
