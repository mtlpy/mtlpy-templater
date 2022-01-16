#!/usr/bin/python3

""" Generate various texts relative to the organizatoin of Montréal-Python 
events. """

import os
import sys
from argparse import ArgumentParser

import tomlkit


FIELDS = ["number", "name_fr", "name_en", 
          "youtube_url", "meetup_url", "streamyard_url", "happyhour_url"]
HAPPYHOUR_URL = "https://pymtl-meet.fjnr.ca/mp-{number}"


def templates_dir():
    return os.path.join(os.path.dirname(__file__), "templates")


def list_templates(args): 
    templates = os.listdir(templates_dir())
    print("\n".join(templates))


def new_event(args):
    doc = tomlkit.document()
    doc["event"] = {}
    for key in FIELDS:
        doc["event"][key] = ""
    return doc.as_string()


def normalize_event(event):
    """ Add all the fields that are missing and that we can reasonalbly infer 
    from the existing data. """
    if not event.get("happyhour_url"):
        event["happyhour_url"] = HAPPYHOUR_URL.format(**event)
    return event


def load_event(args):
    if args.input is None:
        data = sys.stdin.read()
    else:
        data = open(args.input, "rt").read()
    event = normalize_event(tomlkit.loads(data)["event"]) 
    return event


def template_body(name):
    if not os.path.isfile(name):
        name = os.path.join(templates_dir(), name)
    return open(name, "rt").read()


def expand_template(args):
    event = load_event(args)
    body = template_body(args.template)
    return body.format(**event)
    

def main():
    parser = ArgumentParser(sys.argv[0], description=__doc__)
    parser.add_argument("-i", "--input", metavar="FILE", 
                        help="Get TOML data about the event in FILE")
    parser.add_argument("-o", "--output", metavar="FILE", 
                        help="Save output to FILE")
    subparsers = parser.add_subparsers(title="commands")

    cmd_parser = subparsers.add_parser('list-templates')
    cmd_parser.set_defaults(func=list_templates)    

    cmd_parser = subparsers.add_parser('new-event')
    cmd_parser.set_defaults(func=new_event)    

    cmd_parser = subparsers.add_parser('expand')
    cmd_parser.set_defaults(func=expand_template)    
    cmd_parser.add_argument("template", metavar="TEMPLATE",
                            help="Template to expand")

    args = parser.parse_args()
    
    if "func" in args:
        result = args.func(args)
        if result is not None:
            if "output" in args and args.output not in ["-", None]:
                open(args.output, "wt").write(result)
            else:
                print(result)
    else:
        parser.print_help()



# TODO:
# - template for an even toml
# - template for the invite for speakers


if __name__ == "__main__":
    main()
