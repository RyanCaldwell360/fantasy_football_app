import yaml

def get_yaml(path):
    with open(path, "r") as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    return config