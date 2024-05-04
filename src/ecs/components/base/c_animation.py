class AnimationData:
    def __init__(self, animation: dict) -> None:
        self.name = animation["name"]
        self.start = int(animation["start"])
        self.end = int(animation["end"])
        self.framerate = 1.0 / animation["framerate"]


class CAnimation:
    def __init__(self, animation: dict) -> None:
        self.number_frames = animation["number_frames"]
        self.animations = [AnimationData(a) for a in animation["list"]]

        self.current = 0
        self.current_time = 0
        self.current_frame = self.animations[self.current].start
