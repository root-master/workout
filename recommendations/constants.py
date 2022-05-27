workout_programs_category_dict = {
    "physical_therapy": ["mobility_training", "rehabilitation"],
    "pose_correction": ["mobility_training", "rehabilitation"],
    "weight_lifting": ["strength_training"],
    "body_building": ["strength_training"],
    "core_training": ["strength_training"],
    "yoga": ["mobility_training", "flexibility_training", "balance_training"],
    "high_intensity_interval_training": ["endurance_training"],
    "functional_training": ["strength_training", "endurance_training"],
    "calisthenics": ["strength_training", "endurance_training", "mobility_training"],
    "dance": ["mobility_training", "endurance_training"],
    "movement_flow": ["strength_training", "mobility_training", "balance_training"],
    "cardio_training": ["endurance_training"],
    "balanced_workout": ["strength_training", "mobility_training",
                         "balance_training", "flexibility_training", "endurance_training"]
}

time_unit = "minute"
time_options_dict = {
    "under_1_min": [1 / 6, 1 / 4, 1 / 3, 1 / 2, 2 / 3, 3 / 4, 1],
    "under_5_min": [1.5, 2, 3, 4, 5],
    "under_15_min": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "under_30_min": [20, 25, 30],
    "under_1_hour": [35, 40, 45, 50, 55, 60]
}

workout_programs_time_options_dict = {
    "physical_therapy": ["under_5_min", "under_15_min", "under_30_min"],
    "pose_correction": ["under_1_min", "under_5_min", "under_15_min"],
    "weight_lifting": ["under_5_min", "under_15_min", "under_30_min"],
    "body_building": ["under_5_min", "under_15_min", "under_30_min"],
    "yoga": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "high_intensity_interval_training": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "functional_training": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "calisthenics": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "dance": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "movement_flow": ["under_5_min", "under_15_min", "under_30_min"],
    "core_training": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "cardio_training": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
    "balanced_workout": ["under_5_min", "under_15_min", "under_30_min", "under_1_hour"],
}

workout_programs_intensity_dict = {
    "physical_therapy": ["light", "moderate"],
    "pose_correction": ["light"],
    "weight_lifting": ["moderate", "vigorous"],
    "body_building": ["moderate", "vigorous"],
    "yoga": ["light", "moderate"],
    "high_intensity_interval_training": ["moderate", "vigorous"],
    "functional_training": ["moderate", "vigorous"],
    "calisthenics": ["moderate", "vigorous"],
    "dance": ["light", "moderate", "vigorous"],
    "movement_flow": ["light", "moderate", "vigorous"],
    "core_training": ["light", "moderate", "vigorous"],
    "cardio_training": ["light", "moderate", "vigorous"],
    "balanced_workout": ["light", "moderate", "vigorous"],
}

body_parts_dict = {
    "legs": {},
    "arms": {},
    "shoulders": {},
    "chest": {},
    "back": {},
    "abs": {}
}

fitness_dimensions_distribution = {
    "strength_training": {},
    "mobility_training": {},
    "balance_training": {},
    "flexibility_training": {},
    "endurance_training": {}
}

body_parts_list = list(body_parts_dict.keys())

movement_difficulty_options_list = ["beginner", "intermediate", "advanced"]

intensity_level_MET_ranges_dict = {
    "light": [1, 1.5, 2, 2.5],
    "moderate": [3, 3.5, 4, 4.5, 5, 5.5],
    "vigorous": [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12]
}
