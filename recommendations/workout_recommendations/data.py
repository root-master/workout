"""
Module for workout_recommendations data.
"""

import pandas as pd
import random
from recommendations.workout_recommendations.constants import *


def normalize(distribution_dict):
    total = 0
    normalized_distribution_dict = {}
    for key, value in distribution_dict.items():
        total += value

    for key, value in distribution_dict.items():
        normalized_distribution_dict[key] = value / total
    return normalized_distribution_dict


def create_fake_workout_sessions_pd(num_workout_sessions=1000) -> pd.DataFrame:
    """Creates a pandas df of `num_workout_sessions` workout_sessions with random attributes.
    returns pandas df:
        index
        workout_session_id
        workout_program
        time_slot
        total_time_minutes
        avg_movements_difficulty
        avg_intensity
        avg_MET
        body_parts_distribution
        fitness_dimensions_distribution
    """
    workout_sessions_list = []
    workout_programs_list = list(workout_programs_category_dict.keys())
    for i in range(num_workout_sessions):
        workout_session_id = i
        workout_program = random.choice(workout_programs_list)
        time_slot = random.choice(workout_programs_time_options_dict[workout_program])
        total_time_minutes = round(random.choice(time_options_dict[time_slot]), 1)
        avg_movements_difficulty = random.choice(movement_difficulty_options_list)
        avg_intensity = random.choice(workout_programs_intensity_dict[workout_program])
        avg_MET = random.choice(intensity_level_MET_ranges_dict[avg_intensity])

        if workout_program == "core_training":
            body_parts_distribution = {
                "legs": random.uniform(0, 0.1),
                "arms": random.uniform(0, 0.1),
                "chest": random.uniform(0, 0.1),
                "shoulders": random.uniform(0, 0.1),
                "back": random.uniform(0.3, 0.6),
                "abs": random.uniform(0.7, 1)
            }
        elif workout_program == "weight_lifting":
            body_parts_distribution = {
                "legs": random.uniform(0.5, 1),
                "arms": random.uniform(0.5, 1),
                "chest": random.uniform(0, 0.5),
                "shoulders": random.uniform(0.5, 1),
                "back": random.uniform(0.3, 0.6),
                "abs": random.uniform(0.1, 0.3)
            }
        elif workout_program == "body_building":
            body_parts_distribution = {
                "legs": random.uniform(0.5, 1),
                "arms": random.uniform(0.5, 1),
                "chest": random.uniform(0.5, 1),
                "shoulders": random.uniform(0.5, 1),
                "back": random.uniform(0.5, 1),
                "abs": random.uniform(0.1, 0.5)
            }
        else:
            body_parts_distribution = {
                "legs": random.uniform(0, 1),
                "arms": random.uniform(0, 1),
                "chest": random.uniform(0, 1),
                "shoulders": random.uniform(0, 1),
                "back": random.uniform(0, 1),
                "abs": random.uniform(0, 1),
            }

        fitness_dimensions_distribution = {
            "strength_training": random.uniform(0, 1),
            "mobility_training": random.uniform(0, 1),
            "balance_training": random.uniform(0, 1),
            "flexibility_training": random.uniform(0, 1),
            "endurance_training": random.uniform(0, 1)
        }

        for key, value in fitness_dimensions_distribution.items():
            if key in list(workout_programs_category_dict[workout_program]):
                fitness_dimensions_distribution[key] = random.uniform(0.5, 1)
            else:
                fitness_dimensions_distribution[key] = random.uniform(0, 0.3)

        body_parts_distribution = normalize(body_parts_distribution)
        fitness_dimensions_distribution = normalize(fitness_dimensions_distribution)
        workout_session = {
            "workout_session_id": workout_session_id,
            "workout_program": workout_program,
            "time_slot": time_slot,
            "total_time_minutes": total_time_minutes,
            "avg_movements_difficulty": avg_movements_difficulty,
            "avg_intensity": avg_intensity,
            "avg_MET": avg_MET,
            "body_parts_distribution": body_parts_distribution,
            "fitness_dimensions_distribution": fitness_dimensions_distribution}
        workout_sessions_list.append(workout_session)

    df_workout_sessions = pd.DataFrame(workout_sessions_list)

    return df_workout_sessions
