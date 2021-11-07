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
    user_messages = locale['messages']
    formatting = locale['formatting']

    # Retrieving library
    zot = zotero.Zotero(config['library_id'],
                        config['library_type'],
                        config['api_key'])

    # Querying collection to export
    coll_name = (input(user_messages['prompt_coll_name']))  # TODO: make sure that UTF-8 encoding works fine
    coll_metadata = zot.collections(q=str.lower(coll_name))

    # checking if an unambiguous collection was found
    if len(coll_metadata) == 0:
        print(user_messages['err_no_coll_found'].format(coll_name=coll_name))
        sleep(EXIT_TIMER)
        exit(1)
    elif len(coll_metadata) > 1:
        print(user_messages['err_ambiguous_term'].format(coll_name=coll_name, len_coll_meta=len(coll_metadata)))
        sleep(EXIT_TIMER)
        exit(1)

    # Getting collection key - returns list of dicts. If one collection is returned, it is at position 0
    coll_key = coll_metadata[0]['key']

    # Checking for child collections
    if len(zot.collections_sub(coll_key)) > 0:
        print(user_messages['err_child_colls'].format(coll_name=coll_name))
        sleep(EXIT_TIMER)
        exit(1)

    # Getting all collection items as a list of dicts
    coll = zot.collection_items(coll_key)

    testing = Entry(config, coll[0])
    print("type of 'testing.data' is: ", type(testing.data))
    pprint.pp(testing.data)

    # TODO: continue writing here
    # TODO: Remove template entry if there is one


class Entry:
    """This is a class to hold the information of each entry as it is retrieved from the collection as an element.
    Pass a config dict and a raw entry dict to it.
    """

    def __init__(self, config, raw_entry):
        # Getting the fields to fetch
        fetch = dict()
        for field in config['fields_to_fetch']:
            fetch[field] = config['fields_to_fetch'][field]

        # saving content and the output order of elements in separate dicts
        self.data = dict()
        self.positions = dict()
        for element in fetch:
            self.data[element] = self.path_item(raw_entry, fetch[element]['path'])

            # Sorting the elements if their data entry isn't none
            if self.data[element]:
                self.positions[element] = fetch[element]['position']

        self.order = list()
        for key in self.positions:
            # Will skip positions that can't be interpreted
            try:
                self.order.append(float(self.positions[key]))
            except ValueError:
                pass

        # Sorting elements' positions (ascending order)
        self.order.sort()

        # Turning the info_string into a dict
        print(self.data['info_string'])
        self.data['info_string'] = self.process_info_str(self.data['info_string'])

        # Turning the contractors dict list into a list
        print("self.data['contractors'] is: ", self.data['contractors'])

        contractor_list = list()
        for contractor in self.data['contractors']:
            contractor_list.append(contractor['name'])
        self.data['contractors'] = contractor_list

    def path_item(self, item, path):
        """Recursively to the bottom of a path (array) to retrieve a dict item"""
        # Exit condition
        if len(path) == 0:
            return item

        # Recursion logic
        item = item.get(path.pop(0))
        return self.path_item(item, path)

    @staticmethod
    def process_info_str(info_str, kv_delimiter='=', item_delimiter=';'):
        """Takes the info string and turns it into a dict"""
        # splitting string items
        items = info_str.replace('\n', '').split(item_delimiter)

        # splitting items into key/value pairs
        items_dict = dict()
        for item in items:
            k, v = item.split(kv_delimiter)
            v = v.strip()
            # Turning empty and 'none' strings into None type
            if v.lower() == 'none' or len(v) == 0:
                v = None
            items_dict[k.strip()] = v

        return items_dict


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
