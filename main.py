# Importing libraries
from pyzotero import zotero
import json
import pprint

def main():
    # Getting credentials from file
    with open('credentials.json') as f:
        credentials = json.load(f)

    # Retreiving library
    zot = zotero.Zotero(credentials['library_id'],
                        credentials['library_type'],
                        credentials['api_key'])

    # Querying collection to export
    coll_name = input('Please specify the collection name: ')
    coll_metadata = zot.collections(q=str.lower(coll_name))

    # checking if an unambiguous collection was found
    if len(coll_metadata) == 0:
        print(f"Sorry, no collection named '{coll_name}' found.")
        exit(0)
    elif len(coll_metadata) > 1:
        print(f"Sorry, your search term '{coll_name}' is ambiguous as {len(coll_metadata)} collections were found. Consider renaming the collection you want to retreive and/or use a different search term.")
        exit(0)

    # Getting collection key - returned collection in formation is a list of dicts. If one collection is returned, dict is at position 0
    coll_key = coll_metadata[0]['key']

    # Checking for child collections
    if len(zot.collections_sub(coll_key)) > 0:
        print(f"The collection '{coll_name}' has child collections, which are not (yet) supported.")
        exit(0)

    # Getting all collection items as a list
    coll = zot.collection_items(coll_key)

    item_keys = []
    for coll_item in coll:
        item_keys.append(coll_item['key'])

    print(item_keys)
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

if __name__ == '__main__':
    main()