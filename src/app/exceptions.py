class StoryException(Exception):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
