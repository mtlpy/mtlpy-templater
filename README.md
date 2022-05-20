Montréal-Python Event Templater
===============================

This project contains utilities to produce common texts that are used for most events.

## Usage
First setup a virtualenv then install the dependencies of the package:
```
python3 -m venv .venv
. .venv/bin/activate
# OR
echo "layout python3" >> .envrc
direnv allow
```

```
pip install -r requirements.txt
```

Then install the package (-s to symlink to the repository, which auto updates after 
`git pull`): 
```
flit install -s
```

Then play around:
```
mp-templater --help
mp-templater list-templates
mp-templater -o mp-90.toml new-event
# edit mp-90.toml, then generate the description for Meetup
mp-templater -i mp-90.toml expand meetup-desc-en.txt

# you can save the generated text or copy it to your clipboard
mp-templater -i mp-90.toml -o output.txt expand meetup-desc-en.txt
# OR
mp-templater -i mp-90.toml expand meetup-desc-en.txt | xsel -b
```
