#!/bin/python
# -*- coding: utf-8 -*-
#PREREQUISITES TO RUN THIS THING
# -Python27
# -ConfigParser
# -ArgParse
# -nova-cli? or will it be hosted in tchai? if tchai true, we need to make it public

import sys
import logging
from argparse import ArgumentParser
from classer import NoNovaConfigParser
from classer import NovaCliConn
import activity

activities = []


# --------- Arg Parser arguments --------------------------


def cli_parser():
    parser = ArgumentParser(description = """Command line helper for filling nova""")
    parser.add_argument("-c" " --config", dest="config", help="You must run this only the first time", type=str, default="config.ini")
    parser.add_argument("-C" " --category", dest="category", help="Show categories available", action="store_true")
    parser.add_argument("-p" " --project", dest="getp", help="Show your project list", action="store_true")
    parser.add_argument("-a" " --activity", dest="new_activity", help="Insert new set of activities", action="store_true")
    parser.add_argument("-A", dest="from file", help="Reads activity from file --UNAVAILABLE", action="store_true")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    return args

def new_activity():
    logging.info("Starting to add activities n' stuff")

    # activities.append(a)
    stop_input = "y"
    invalid_data = 'true'
    while stop_input == "y".lower().strip()[0]:
        a = activity.Activity()
        # while invalid_data == 'true':
        #     invalid_data = 'false'
        #     if not a.project:
        #         invalid_data = 'true'
        a.project = raw_input("Project number?[{}]: ".format(a.project)) or a.project
        #     if not a.category:
        #         invalid_data = 'true'
        a.category = raw_input("Category number?[{}]: ".format(a.category)) or a.category
        #     if not a.hours:
        #         invalid_data = 'true'
        a.hours = raw_input("Number of hours?[{}]: ".format(a.hours)) or a.hours
        #     if not a.comment:
        #         invalid_data = 'true'
        a.comment = raw_input("Comment?[{}]: ".format(a.comment)) or a.comment

        backend.execute(a.toString())

        # Adding to file
        store = raw_input("Want to save activity to file? [y/N]")
        if store == "y".lower().strip()[0]:
            save_activity(a)

        # Loop
        stopInput = raw_input("Want to add another? [Y/n]: ")
        logging.info("add another? %s", stopInput)


def get_projects(): # Only changes the word to send
    backend.execute("projects")
    logging.info("Yo, I just checked my projects!")


def get_categories(): # Should we be saving this in the .ini file? To avoid requiring it from nova each time and quicker printing.
    backend.execute("categories")
    logging.info("Mah categories dawg! here they are")


def save_activity(act):
    data = [a for a in dir(act) if not a.startswith('__')]
    for i in data:
        novaconf.set("Activities", "{} {}".format(act.id, i), getattr(act, i))
    with open(novaconf.args.config, "wb") as config_file:
        try:
            novaconf.write(config_file)
        finally:
            logging.info("Activity {} added to config".format(act.id))




def main():
    global novaconf
    global backend
    logging.basicConfig(filename='nonovawtf.log' ,format='%(asctime)s - %(levelname)s:%(message)s',datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    #Parse teh world (one command line at a time)
    logging.info("WOOOOT I\'M ALIVE MTF!")
    args = cli_parser()
    # Read config file, if not, create one.
    novaconf = NoNovaConfigParser(args)
    # Ensure connection to nova-cli backend
    backend = NovaCliConn(novaconf)
    # Choose your destiny

    if args.new_activity:
        new_activity()
    elif args.getp:
        get_projects()
    elif args.category:
        get_categories()

if __name__ == "__main__":
    sys.exit(main())
