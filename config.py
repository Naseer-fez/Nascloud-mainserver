import json
import os
import sys

class Config:
    def __init__(self):
        # Store in AppData/NasCloudMainServer/config.json
        self.path = "config.json"
        self.reload()

    def reload(self):
        self.data = {}
        if not os.path.exists(self.path):
            print(f"WARNING: Config file not found at {self.path}. Falling back to Environment Variables.")
            return
            
        try:
            with open(self.path) as file:
                content = file.read().strip()
                if not content:
                    print(f"ERROR: Config file at {self.path} is empty.")
                    print("Please configure the server properly before starting.")
                    sys.exit(1)
                self.data = json.loads(content)
        except json.JSONDecodeError:
            print(f"ERROR: Config file at {self.path} is not valid JSON.")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR reading config: {e}")

    def get(self, key, default=None):
        env_val = os.getenv(key)
        if env_val is not None:
            if env_val.lower() == 'true': return True
            if env_val.lower() == 'false': return False
            if env_val.isdigit(): return int(env_val)
            return env_val
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)
        
config = Config()
