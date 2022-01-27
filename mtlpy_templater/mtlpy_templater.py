#!/usr/bin/python3

""" Generate various texts relative to the organizatoin of Montréal-Python 
events. """

import os
import sys
import locale
from argparse import ArgumentParser
from datetime import datetime
from collections import defaultdict
from glob import glob
from random import shuffle

import tomlkit


FIELDS = ["number", "name_fr", "name_en", "date",
          "youtube_url", "meetup_url", "streamyard_url", "happyhour_url", 
          "presentations_fr", "presentations_en"]
HAPPYHOUR_URL = "https://pymtl-meet.fjnr.ca/mp-{number}"
TOP_MARKERS = {"fr": "français plus bas", 
               "en": "English follows"}

def templates_dir():
    return os.path.join(os.path.dirname(__file__), "templates")


def list_templates(args): 
    t_langs = defaultdict(lambda: [])
    templates = os.listdir(templates_dir())

    # add entries for the templates for which we can do a bilingual aggregate
    for t in templates:
        base, ext = os.path.splitext(t)
        if base.endswith(("-fr", "-en")):
            base, lang = base.rsplit("-", 1)
            t_langs[base].append(lang)
    for basename, langs in t_langs.items():
        if len(langs) == 2:
            templates.append(f"{basename}-bilingual")

    print("\n".join(sorted(templates)))


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

    when = datetime.fromisoformat(event["date"])
    loc = locale.getlocale()
    try:
        locale.setlocale(locale.LC_ALL, "fr_CA")
        event["month_fr"] = when.strftime("%B")
        locale.setlocale(locale.LC_ALL, "en_CA")
        event["month_en"] = when.strftime("%B")        
    finally:
        locale.setlocale(locale.LC_ALL, loc)

    return event


def load_event(args):
    if args.input is None:
        data = sys.stdin.read()
    else:
        data = open(args.input, "rt").read()
    event = normalize_event(tomlkit.loads(data)["event"]) 
    return event


def bilingual_body(name):
    """ Join French and English versions of a template in a random order. 
    
    The two languages are separated by ugly but unambiguous text markers. 
    """
    
    langs = ["fr", "en"]
    shuffle(langs)
    first, second = langs
    
    first_glob = name.replace("-bilingual", f"-{first}.*")
    first_path = glob(os.path.join(templates_dir(), first_glob))[0]

    second_glob = name.replace("-bilingual", f"-{second}.*")
    second_path = glob(os.path.join(templates_dir(), second_glob))[0]

    segments = [f"-- {TOP_MARKERS[second]} --", 
                template_body(first_path), 
                f"== {second.upper()} ==", 
                template_body(second_path)]
    return "\n".join(segments)


def template_body(name):
    if os.path.isfile(name):
        return open(name, "rt").read()
    fq_path = os.path.join(templates_dir(), name)   
    if os.path.isfile(fq_path):
        return open(fq_path, "rt").read()
    if name.endswith("-bilingual"):
        return bilingual_body(name)
    raise ValueError(f"Don't know where the find to body of template '{name}'. "
                     "Try specifying a full path or one of the names returned "
                     "by the list-templates command.")


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
# - default values in new event TOML
# - make it generic enough to use for programming nights and teaching workshops


if __name__ == "__main__":
    main()
