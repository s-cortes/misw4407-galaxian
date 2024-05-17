class CTagPlayer:

    def __init__(self, bullets: int, lives: int) -> None:
        self.bullets: int = bullets
        self.left: bool = False
        self.right: bool = False
        self.lives: int = lives
