# OFFLINE work with sample data

# Standard library imports
import json
import pprint
from time import sleep

# 3rd-party package imports
from docx import Document
from pyzotero import zotero

# Global variables
EXIT_TIMER = 3

def main():
    # Loading config & setting locale
    config = get_config('config.json')
    locale = set_locale('locale.json', config['locale'])
    # pprint.pp(locale)

    # Saving messages and formatting dicts
    messages = locale['messages']
    formatting = locale['formatting']

    # = = = = = = = = = = = =
    # Skipping retrieval via pyzotero and using the output.json file instead
    with open('output.json', mode='r', encoding='utf-8') as f:
        coll = json.load(f)


    # TODO: Add elements to pick to config.json

    # = = = = = = = = = = = =
    print("coll[0] is: ", coll[0]['data'])
    testing = Entry(config, coll[0])
    pprint.pp(testing.data)


class Entry:
    """This is a class to hold the information of each entry as it is retrieved from the collection as an element.
    Pass a config dict and a raw entry dict to it.
    """
    def __init__(self, config, raw_entry):
        # Getting the fields to fetch
        fetch = dict()
        for field in config['fields_to_fetch']:
            fetch[field] = config['fields_to_fetch'][field]
        # DEBUGGING
        print(fetch)

        self.data = dict()
        for element in fetch:
            print('fetch element is: ', element)
            self.data[element] = self.path_item(raw_entry, fetch[element]['path'])

        # TODO: deal with variable length contractors list
        # TODO: deal with misc
        # TODO: consider redesigning the ordering mechanism


    def path_item(self, item, path):
        """Recursively to the bottom of a path (array) to retrieve a dict item"""
        # Exit condition
        if len(path) == 0:
            return item

        # Recursion logic
        item = item.get(path.pop(0))
        return self.path_item(item, path)


    # = = = = = = = = = = = =

def get_config(filename):
    """Gets the config from the specified file and returns a dict of it. Handles missing file by creating template."""

    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        empty_config = {'library_id': None,
                        'library_type': None,
                        'api_key': None,
                        'locale': None
                        }
        with open(filename, 'w') as f:
            f.write(json.dumps(empty_config))
        print(f"'{filename}' not found in the execution directory. A blank file was created. Consult documentation.")
        sleep(EXIT_TIMER)
        exit(1)

    # TODO: Add additional checks to make sure that the fields 'library_id' and 'library_type' have the right format
    # TODO: Figure out how to store credentials securely

    # assert isinstance(config, dict)
    return config


def set_locale(filename, loc, fallback_loc='en'):
    """Gets locale-specific messages and formatting from json file"""

    # Trying to open the specified file
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            locale = json.load(f)
    except FileNotFoundError:
        print(f"Missing '{filename}' file")
        sleep(EXIT_TIMER)
        exit(1)

    # Trying to retrieve the specified locale setting
    try:
        locale = locale[loc]
    except KeyError:
        # Trying to use the default [specified] fallback locale
        try:
            locale = locale[fallback_loc]
            print(f"Fallback locale '{fallback_loc}' set")
        except KeyError:
            print(f"fallback locale '{fallback_loc}' not found")
            sleep(EXIT_TIMER)
            exit(1)

    # assert isinstance(locale, dict)
    return locale


if __name__ == '__main__':
    main()
