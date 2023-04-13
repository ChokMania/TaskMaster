import yaml


class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load()

    def load(self):
        with open(self.config_path, "r") as config_file:
            self.data = yaml.safe_load(config_file)

    # Ajouter cette méthode pour rendre l'objet Config subscriptable
    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self):
        return f"Config({self.config_path})"
