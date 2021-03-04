"""
Workout Session data_type and utils.
"""
from typing import Dict

from workout_demo.utils.utils import now, date


class WorkoutSession:
    def __init__(self,
                 pods: Dict = None):
        self.pods = pods
        self.session_id = int(now())
        self.workout_date = date()
