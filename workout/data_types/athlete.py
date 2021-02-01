"""
data_type and utils for athletes.
"""


class Athlete:
    """Athlete's data."""

    def __init__(self,
                 name: str,
                 height: int,
                 weight: int,
                 **kwargs):
        self.name = name
        self.height = height
        self.weight = weight
        self.__dict__.update(kwargs)
