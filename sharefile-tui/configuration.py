import configparser
import os
from rich.prompt import Prompt

config_file = configparser.ConfigParser()

home_directory = os.path.expanduser('~')
config_dir_default = os.path.join(
    home_directory, ".config", "sharefile-tui")
config_fname_default = "config.ini"


def set_defaults(config_file):
    # ADD ORGANIZATION SECTION
    config_file.add_section("General")

    config_dir = Prompt.ask("Configuration directory",
                            default=config_dir_default)
    config_file.set("General", "config_dir", config_dir)

    subdomain = Prompt.ask(
        "ShareFile subdomain [https://TYPE_THIS_PART_HERE.sharefile.com]")
    config_file.set("Organization", "subdomain", subdomain)

    # ADD CREDENTIALS SECTION
    config_file.add_section("Credentials")

    client_id = Prompt.ask("API client_id")
    config_file.set("Credentials", "client_id", client_id)

    client_secret = Prompt.ask("API client_secret")
    config_file.set("Credentials", "client_secret", client_secret)

    user_email = Prompt.ask("API user user_email")
    config_file.set("Credentials", "username", user_email)

    user_pass = Prompt.ask("API user application-specific user_password")
    config_file.set("Credentials", "password", user_pass)


def make_config_dir(config_dir):
    isExist = os.path.exists(config_dir)
    if not isExist:
        try:
            os.mkdirs(config_dir)
            created_config_dir = True
            print("Successfully created the directory %s " % config_dir)
        except OSError:
            created_config_dir = False
            print("Creation of the directory %s failed" % config_dir)
    return created_config_dir


def save_config_file(configuration=config_file, config_dir=config_dir_default, file_name=config_fname_default):
    full_path = os.path.join(config_dir, file_name)
    with open(full_path, 'w') as configfileObj:
        config_file.write(configfileObj)
        configfileObj.flush()
        configfileObj.close()
    print("Config file {} created".format(full_path))


def delete_config_dir(config_dir):
    try:
        os.rmdir(config_dir)
    except OSError:
        print("Deletion of the directory %s failed" % config_dir)
    else:
        print("Successfully deleted the directory %s" % config_dir)


def read_config_file(config_dir=config_dir_default, file_name=config_fname_default):
    global config_file 
    full_path = os.path.normpath(os.path.join(config_dir, file_name))
    with open(full_path, 'r') as config_file_path:
        config_file.read(config_file_path)
    return config_file

def load_config():
    # Load the configuration file
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(r"C:\Users\spencersm\.config\sharefile-tui\config.ini")
    return config


default_full_path = os.path.join(config_dir_default, config_fname_default)
default_config_exists = os.path.exists(default_full_path)
if not default_config_exists:
    set_defaults()
    make_config_dir()
    save_config_file()

settings = read_config_file()
print(settings)
