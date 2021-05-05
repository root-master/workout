"""
Module global context.
"""
import os
from typing import Dict
from pathlib import Path

import yaml


def read_yaml_file(path_to_yaml: str) -> Dict:
    """Reads yaml files to a Dict.

    Args:
        path_to_yaml: path to the yaml file.

    Returns:
        parsed_yaml_dict: A python Dict with yaml key, values in the file.
    """
    with open(path_to_yaml, "r") as stream:
        parsed_yaml_dict = yaml.load(stream, Loader=yaml.FullLoader)

    return parsed_yaml_dict


def read_all_yaml_files(env_list) -> Dict:
    """Reads all yaml files to a Dict.

        Args:
            env_list: list of environments, e.g. ["local"]. The corresponding env is in
                config/{env}

        Returns:
            all_parameters: A python Dict with all yaml key, values of all environments.
        """
    file_path = Path(__file__).parent
    all_parameters = {}
    for env in env_list:
        all_parameters[env] = {}
        relative_path = "config/{env}/".format(env=env)
        directory = os.path.join(str(file_path), relative_path)

        for file_name in os.listdir(directory):
            if file_name.endswith(".yml"):
                key = file_name.replace(".yml", "")
                path_to_yaml = os.path.join(directory, file_name)
                parsed_yaml_dict = read_yaml_file(path_to_yaml)
                all_parameters[env][key] = parsed_yaml_dict
    return all_parameters


class Context:
    """Repo's context."""

    def __init__(self, env="local"):
        """Initializes context for the given env."""
        self.env_list = ["local"]
        self.all_parameters = read_all_yaml_files(self.env_list)
        self.parameters = self.all_parameters[env]
        self.repo_path = Path(__file__).parent.parent

    def __del__(self):
        del self.all_parameters
        del self.parameters

    def get_params(self, env):
        """Returns env's params."""
        return self.all_parameters[env]
