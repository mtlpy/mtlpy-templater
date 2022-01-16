Montréal-Python Event Templater
===============================

This project contains utilities to produce common texts that are used for most events.

## Usage
First install the dependencies of the package and setup a virtualenv:
```
pipenv sync
pipenv shell 
# OR
echo "layout pipenv" >> .envrc
direnv allow
```

Then play around:
```
python mtlpy_template/mtlpy_template.py --help
python mtlpy_template/mtlpy_template.py list-templates
python mtlpy_template/mtlpy_template.py -o mp-90.toml new-event
# edit mp-90.toml
python mtlpy_template/mtlpy_template.py -i mp-90.toml expand meetup-desc-en.txt
```

## TODO
* Upload event data to Google Drive with rclone
