class CLevel:
    def __init__(self) -> None:
        self.intro_active: bool = True
        self.paused: bool = False
        self.completed: bool = False
        self.restart: bool = False

        self.inputs_enaled: bool = False
        self.attacks_enabled: bool = False
        self.next_level: bool = False

        self.current = -1
        self.player = None
        self.invaders_rage = -1
