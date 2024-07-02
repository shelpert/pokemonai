from pyboy import PyBoy

class Player:

    pyboy: PyBoy

    def __init__(self, pyboy: PyBoy):
        self.pyboy = pyboy

    def attack (self, num):
        self.press_a()
        for _ in range (num - 1):
            self.press_down()
        self.press_a()

    def switch (self, num):
        self.press_right()
        self.press_a()
        for _ in range (num - 1):
            self.press_down()
        self.press_a()


    def press_a(self):
        self.pyboy.button('a')
        self.pyboy.tick()
        self.pyboy.tick()

    def press_b(self):
        self.pyboy.button('s')
        self.pyboy.tick()
        self.pyboy.tick()

    def press_start(self):
        self.pyboy.button("start")
        self.pyboy.tick()
        self.pyboy.tick()

    def press_select(self):
        self.pyboy.button("select")
        self.pyboy.tick()
        self.pyboy.tick()

    def press_left(self):
        self.pyboy.button("left")
        self.pyboy.tick()
        self.pyboy.tick()

    def press_right(self):
        self.pyboy.button("right")
        self.pyboy.tick()
        self.pyboy.tick()

    def press_up(self):
        self.pyboy.button("up")
        self.pyboy.tick()
        self.pyboy.tick()

    def press_down(self):
        self.pyboy.button("down")
        self.pyboy.tick()
        self.pyboy.tick()




    