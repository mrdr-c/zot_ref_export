# standard library
import json
import pprint

# 3rd-party libraries
from pyzotero import zotero


def main():
    # Loading config & setting locale
    config = get_config('config.json')
    locale = set_locale('locale.json', config['locale'])
    # pprint.pp(locale)

    # Saving messages and formatting dicts
    messages = locale['messages']
    formatting = locale['formatting']

    # Retrieving library
    zot = zotero.Zotero(config['library_id'],
                        config['library_type'],
                        config['api_key'])

    # Querying collection to export
    coll_name = (input(messages['prompt_coll_name']))  # TODO: make sure that UTF-8 encoding works fine
    coll_metadata = zot.collections(q=str.lower(coll_name))

    # checking if an unambiguous collection was found
    if len(coll_metadata) == 0:
        print(messages['err_no_coll_found'].format(coll_name=coll_name))
        exit(1)
    elif len(coll_metadata) > 1:
        print(messages['err_ambiguous_term'].format(coll_name=coll_name, len_coll_meta=len(coll_metadata)))
        exit(1)

    # Getting collection key - returns list of dicts. If one collection is returned, it is at position 0
    coll_key = coll_metadata[0]['key']

    # Checking for child collections
    if len(zot.collections_sub(coll_key)) > 0:
        print(messages['err_child_colls'].format(coll_name=coll_name))
        exit(1)

    # Getting all collection items as a list
    coll = zot.collection_items(coll_key)

    item_keys = []
    for coll_item in coll:
        item_keys.append(coll_item['key'])

    print(coll)
    # print(zot.item(item_keys[0]))

    with open('output.json', 'w') as f:
        f.write(json.dumps(coll))

    # refactoring of retrieved data
    for element in coll:
        # debugging
        print(element['data']['abstractNote'])

        # TODO: create a class that contains the required data and make sure that there is sufficient error handling
        # element['data']

    '''
    # DEBUGGING
    with open('output.json', 'w') as f:
        f.write(json.dumps(zot.collection_items(collection_key)))
    '''

    '''
    items = zot.top(limit=15)
    # we've retrieved the latest five top-level items in our library
    # we can print each item's item type and ID
    for item in items:
        print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))
        print(item['data'])
    '''


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
        exit(1)

    # TODO: Add additional checks to make sure that the fields 'library_id' and 'library_type' have the right format
    # TODO: Figure out how to store credentials securely

    # assert isinstance(config, dict)
    return config


def set_locale(filename, loc, fallback_loc='en'):
    """Gets locale-specific messages and formatting from json file"""

    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            locale = json.load(f)
    except FileNotFoundError:
        print(f"Missing '{filename}' file")
        exit(1)

    try:
        locale = locale[loc]
    except KeyError:
        try:
            locale = locale[fallback_loc]
            print(f"Fallback locale '{fallback_loc}' set")
        except KeyError:
            print(f"fallback locale '{fallback_loc}' not found")
            exit(1)

    # assert isinstance(locale, dict)
    return locale


if __name__ == '__main__':
    main()
