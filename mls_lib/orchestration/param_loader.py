import os
import yaml

class ParamLoader:
    def __init__(self):
        self.param_file = os.environ.get("PARAM_FILE", "params.yaml")
    @staticmethod
    def load(self, param_name):
        with open(self.param_file, 'r') as stream:
            try:
                params = yaml.safe_load(stream)
                return params[param_name]
            except yaml.YAMLError as exc:
                print(exc)
                return None