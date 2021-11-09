 # Zotero references script (and app)
This project aims to create a flexible, minimalistic interface that enables retrieving reference collections from Zotero 
and pasting them into a docx file.

## What is a 'reference collection'?
A reference collection is a collection of project references stored as Zotero items of the type 'document'. The idea is 
to enable building reference lists with descriptions and other important project informations automatically, e.g. for 
project applications. It's a very specific use case, but it can be adapted to fit your individual needs. The config file
(see below) yields some options and could be expanded. It's supposed to be distributed to (non-technical) colleagues for 
easy everyday usage.

## File requirements
zot_ref_export requires two JSON files, `config.json` and `locale.json`. The former holds information on multiple things, 
e.g. the library id and the key required to access it (create one in your Zotero account), as well as fields that 
contain the items to retrieve and their output positions etc. If the file is not found, an *incomplete* template will be created.  
Locale holds the messages that are displayed, as well as language-specific field descriptions. Currently, there is no 
mechanism to build it if it is missing, though this could be easily implemented.

## Building with PyInstaller
There is a spec that specifies the JSON files as datas. It is not otherwise modified.  
Run `pyinstaller --clean --noconfirm zot_ref_export.spec` to build. If the file is missing, run PyInstaller on the script
and specify the files as options `pyinstaller --add-data="config.json;." --add-data="locale.json;." zot_ref_export.py`