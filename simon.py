class Simon:
    def __init__(self, title_font, text_font, label, displayio, pixels, random):
        self.pixels = pixels
        self.random = random

        self.title = label.Label(title_font, text="Simon Says", color=0xFFFFFF)
        self.title.anchor_point = (0.0, 0.0)
        self.title.anchored_position = (0, 0)

        self.text = label.Label(text_font, text="Repeat the sequence!", color=0xFFFFFF)
        self.text.anchor_point = (0.0, 0.0)
        self.text.anchored_position = (0, 18)

        self.end = label.Label(title_font, text="", color=0xFFFFFF)
        self.end.anchor_point = (0.0, 0.0)
        self.end.anchored_position = (0, 36)

        self.view = displayio.Group()
        self.view.append(self.title)
        self.view.append(self.text)
        self.view.append(self.end)

        self.sequence = []

    def new(self):
        choice = self.random.randint(0,11)
        self.sequence.append(choice)
        return choice

    def clear_board(self):
        count = 0
        for pixel in self.pixels:
            self.pixels[count] = 0
            count+=1
