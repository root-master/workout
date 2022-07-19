"""
Module for workout_recommendations model.
"""


def calculate_dist_distributions(input_dist, data_dist):
    """
    Calculates the distance between two distributions.
    Args:
        input_dist:
        data_dist:

    Returns:

    """
    dist = 0
    for k, v in input_dist.items():
        dist += (data_dist[k] - v) ** 2
    return dist ** 0.5


def recommend_workout(df_workout_sessions,
                      total_time_minutes=None,
                      avg_MET=None,
                      avg_movements_difficulty=None,
                      input_fitness_dimensions_distribution=None,
                      input_body_parts_distribution=None,
                      top_rank=0.5
                      ):
    """
    Recommends a workout from df_workout_sessions based on user macro inputs.
    Args:
        df_workout_sessions:
        total_time_minutes:
        avg_MET:
        avg_movements_difficulty:
        input_fitness_dimensions_distribution:
        input_body_parts_distribution:
        top_rank:

    Returns:

    """
    df_bundles = df_workout_sessions
    if total_time_minutes:
        df_bundles = filter_bundles_for_time(df_workout_sessions,
                                             total_time_minutes=total_time_minutes,
                                             error_tolerance=0.2)
    if avg_MET:
        df_bundles = filter_bundles_for_intensity(df_bundles,
                                                  avg_MET,
                                                  error_tolerance=0.2)
    if avg_movements_difficulty:
        df_bundles = filter_bundles_for_movement_difficulty(df_bundles, avg_movements_difficulty)

    if input_fitness_dimensions_distribution and input_body_parts_distribution:
        df_bundles = rank_bundles_for_other_parameters(df_bundles,
                                                       input_fitness_dimensions_distribution,
                                                       input_body_parts_distribution)
    return choose_bundle(df_bundles, top_rank)


def filter_bundles_for_time(df_workout_sessions,
                            total_time_minutes,
                            error_tolerance=0.2):
    """
    Filters workout_sessions that satisfies total_time_minutes within a tolerance.
    Args:
        df_workout_sessions:
        total_time_minutes:
        error_tolerance:

    Returns:
        df_bundles:
    """
    df_bundles = df_workout_sessions[
        (total_time_minutes * (1 - error_tolerance) < df_workout_sessions["total_time_minutes"]) &
        (df_workout_sessions["total_time_minutes"] < total_time_minutes * (1 + error_tolerance))
        ]

    return df_bundles


def filter_bundles_for_intensity(df_bundles,
                                 avg_MET,
                                 error_tolerance=0.2):
    """
    Filters workout_bundles that satisfies total_time_minutes within a tolerance.
    Args:
        df_bundles:
        avg_MET:
        error_tolerance:

    Returns:
    """
    df_bundles = df_bundles[
        (avg_MET * (1 - error_tolerance) < df_bundles["avg_MET"]) &
        (df_bundles["avg_MET"] < avg_MET * (1 + error_tolerance))
        ]
    return df_bundles


def filter_bundles_for_movement_difficulty(df_bundles, avg_movements_difficulty):
    """Filters bundles based on movement difficulty.
        Args:
            df_bundles:
            avg_movements_difficulty:

        Returns:

        """
    df_bundles = df_bundles[df_bundles["avg_movements_difficulty"] == avg_movements_difficulty]
    return df_bundles


def rank_bundles_for_other_parameters(df_bundles,
                                      input_fitness_dimensions_distribution,
                                      input_body_parts_distribution):
    """
    Ranks bundles based on a relevance metric for parameters other than time and avg_MET.
    Args:
        df_bundles:
        input_fitness_dimensions_distribution
        input_body_parts_distribution

    Returns:
        df_bundles_ranked
    """
    df_bundles["fitness_distribution_distance"] = 0.0
    df_bundles["body_parts_distribution_distance"] = 0.0
    df_bundles["dist_error"] = 0.0
    for index, row in df_bundles.iterrows():
        df_bundles.loc[index, "fitness_distribution_distance"] = calculate_dist_distributions(
            input_fitness_dimensions_distribution, row["fitness_dimensions_distribution"])
        df_bundles.loc[index, "body_parts_distribution_distance"] = calculate_dist_distributions(
            input_body_parts_distribution, row["body_parts_distribution"])
        df_bundles.loc[index, "dist_error"] = \
            (row["fitness_distribution_distance"] ** 2 + row["body_parts_distribution_distance"] ** 2) ** 0.5
    df_bundles = df_bundles.sort_values(by="dist_error", ascending=True)
    return df_bundles


def choose_bundle(df_bundles,
                  top_rank):
    """Output a bundle for a given page:
    Args:
        df_bundles:
        top_rank:

    Returns:

    """
    return df_bundles.head(int(len(df_bundles.index) * top_rank)).sample()
