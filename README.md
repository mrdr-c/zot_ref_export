 # Zotero references script (and app)
This project aims to create a user-friendly interface that enables retreiving reference collections from Zotero and pasting them into a docx file.

## TODO
- [ ] Which kind of attachment to use? Potential candidates: `docx`, `md`, Zotero notes format (whatever that is...)
- [ ] How to deal with templates?
- [ ] Specify which information is relevant for references

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