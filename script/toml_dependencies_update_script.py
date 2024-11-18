import os
import toml

def find_pyproject_files():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    pyproject_files = []

    for root, dirs, files in os.walk(current_dir):
        if "pyproject.toml" in files:
            pyproject_files.append(os.path.join(root, "pyproject.toml"))

    return pyproject_files


def load_lock_file(lock_file_path):
    with open(lock_file_path, 'r') as lock_file:
        lock_data = toml.load(lock_file)
    return lock_data


def update_pyproject_versions(toml_file_path, lock_data):
    with open(toml_file_path, 'r') as file:
        toml_data = toml.load(file)

    for dependency in toml_data['project']['dependencies']:
        dep_name = dependency.split('>=')[0] 
        for pkg in lock_data['package']:
            if pkg['name'] == dep_name:
                new_version = pkg['version']
                toml_data['project']['dependencies'] = [
                    f"{dep_name}>={new_version}" if dep_name in dep else dep for dep in toml_data['project']['dependencies']
                ]

    with open(toml_file_path, 'w') as file:
        toml.dump(toml_data, file)


if __name__ == "__main__":
    toml_file_paths = find_pyproject_files()
    lock_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uv.lock')

    lock_data = load_lock_file(lock_file_path)

    for toml_file_path in toml_file_paths:
        print(f"Updating {toml_file_path}...")
        update_pyproject_versions(toml_file_path, lock_data)
        print(f"Updated {toml_file_path}")
