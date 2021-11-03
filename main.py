# Importing libraries
from pyzotero import zotero
import json
import pprint


def main():
    # Getting credentials from file
    config = get_config('config.json')

    # Retrieving library
    zot = zotero.Zotero(config['library_id'],
                        config['library_type'],
                        config['api_key'])

    # Querying collection to export
    coll_name = input('Please specify the collection name: ')
    coll_metadata = zot.collections(q=str.lower(coll_name))

    # checking if an unambiguous collection was found
    if len(coll_metadata) == 0:
        print(f"Sorry, no collection named '{coll_name}' found.")
        exit(1)
    elif len(coll_metadata) > 1:
        print(f"Sorry, your search term '{coll_name}' is ambiguous as {len(coll_metadata)} collections were found. Consider renaming the collection you want to retrieve and/or use a different search term.")
        exit(1)

    # Getting collection key - returns list of dicts. If one collection is returned, it is at position 0
    coll_key = coll_metadata[0]['key']

    # Checking for child collections
    if len(zot.collections_sub(coll_key)) > 0:
        print(f"The collection '{coll_name}' has child collections, which are not (yet) supported.")
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
        with open(filename, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        empty_config = {'library_id': None,
                        'library_type': None,
                        'api_key': None,
                        'locale': None
                        }
        with open(filename, 'w') as f:
            f.write(json.dumps(empty_config))
        print(f"The required '{filename}' was not found in the execution directory. A blank file was created.")
        exit(1)

    return config


if __name__ == '__main__':
    main()
