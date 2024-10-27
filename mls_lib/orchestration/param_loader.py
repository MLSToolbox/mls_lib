import os
import yaml

PARAM_FILE = os.environ.get("PARAM_FILE", "./params.yaml")

class ParamLoader:
    @staticmethod
    def load(param_name):
        with open(PARAM_FILE, 'r') as stream:
            try:
                params = yaml.safe_load(stream)
                result = ParamLoader.recursive_get(params, param_name.split('.'))
                return result
            except yaml.YAMLError as exc:
                print(exc)
                return None
    @staticmethod
    def recursive_get(params, param_name_list):
        for param_name in param_name_list:
            params = params[param_name]
        return params