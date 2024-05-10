class CInvaderSpawner:
    def __init__(self, spawner_size: dict) -> None:
        self.time: float = 0.0
        self.spawner_size = spawner_size['spawner_size']
        self.spawn_time = spawner_size['spawner_time']
        self.spawn_is_on = False

