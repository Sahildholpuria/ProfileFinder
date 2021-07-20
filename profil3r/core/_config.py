import os.path
import shutil
import json

def load_config(self):
    # create config.json from config.json.template if the file doesn't exist
    if not os.path.exists(self.config_path):
        shutil.copy('{}.template'.format(self.config_path), self.config_path)

    # load config from config.json
    with open(self.config_path, 'r') as f:
        self.config = json.load(f)