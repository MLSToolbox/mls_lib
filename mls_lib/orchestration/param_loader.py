""" ParamLoader: Loads parameters from a yaml file """
import os
import yaml

PARAM_FILE = os.environ.get("PARAM_FILE", "./params.yaml")

class ParamLoader:
    """ ParamLoader: Loads parameters from a yaml file """
    @staticmethod
    def load(param_name):
        """
        Loads a parameter from a yaml file.

        The yaml file is specified by the PARAM_FILE environment variable.
        If PARAM_FILE is not set, the default value is "./params.yaml".

        The param_name is the name of the parameter to load,
        and must be specified as a string.
        The param_name string is split using '.' as the separator,
        and the resulting list of strings is used to traverse the
        yaml dictionary.

        If the parameter is not found, None is returned.

        :param param_name: The name of the parameter to load
        :return: The value associated with the parameter
        """
        with open(PARAM_FILE, 'r', encoding="utf-8") as stream:
            try:
                params = yaml.safe_load(stream)
                result = ParamLoader.recursive_get(params, param_name.split('.'))
                return result
            except yaml.YAMLError as exc:
                print(exc)
                return None
    @staticmethod
    def recursive_get(params, param_name_list):
        """
        Recursively traverse the params dictionary to get the value
        associated with the key specified in param_name_list.

        Args:
            params (dict): The dictionary to traverse.
            param_name_list (list[str]): The list of keys to traverse,
                in order.

        Returns:
            The value associated with the key at the end of
            param_name_list.
        """
        for param_name in param_name_list:
            params = params[param_name]
        return params
