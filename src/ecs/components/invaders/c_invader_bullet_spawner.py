class CInvaderBulletSpawner:
    def __init__(self, spawner_cfg: dict) -> None:
        self.time: float = 0.0
        self.shooters = spawner_cfg['shooters']
        self.spawn_time = spawner_cfg['spawner_time']
