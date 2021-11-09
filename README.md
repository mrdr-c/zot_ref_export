 # Zotero references script (and app)
This project aims to create a user-friendly interface that enables retreiving reference collections from Zotero and pasting them into a docx file.

## TODO
- [ ] ~~Which kind of attachment to use? Potential candidates: `docx`, `md`, Zotero notes format (whatever that is...)~~
- [ ] How to deal with templates? *- what did you mean by that?*
- [x] Specify which information is relevant for references
- [x] Figure out how to store and retrieve the zotero item fields flexibly
  - [x] Make sure that the user can specify the order of the fields in the document to be created
  - [x] Store this information in the config file
- [x] Read up on docx-handling
- [x] Read up on PyInstaller-wrapping everything

## Requirements
main.py requires a file named `config.json` with the following info:
```
{
   "library_id": < int >,
   "library_type": < string >,
   "api_key": < string >,
   "locale": < string >,
   [...]
}
```
If the file does not exist, a blank template will be added. 