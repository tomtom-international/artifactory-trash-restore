#!/usr/bin/python3

import argparse
import coloredlogs
import logging
import os
import requests
import sys


from ast import literal_eval


def configure_logger(verbose):
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)
    coloredlogs.install(level=log_level)


def main():
    parser = argparse.ArgumentParser(
        description="Restore artifacts from Artifactory trashcan"
    )
    parser.add_argument(
        "path", action="store", help="Path to be restored from trashcan (e.g., my-repo or my-repo/org/acme/)"
    )
    parser.add_argument(
        "--url", "-u", required=True, action="store", help="Artifactory URL"
    )
    parser.add_argument(
        "--token", "-t", required=True, action="store", help="Artifactory access token"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Increase output verbosity"
    )
    parser.add_argument(
        "--dry-run", "-d", action="store_true", help="Run in dry-run mode only"
    )
    args = parser.parse_args()

    configure_logger(args.verbose)
    logging.info("Attempting to restore {} from trashcan on {}".format(args.path, args.url))
    restore_trashcan_item(args, args.path)


def restore_trashcan_item(args, path):
    header = {'Authorization': 'Bearer ' + args.token}
    response = requests.get("{}/api/storage/auto-trashcan/{}".format(args.url, path), headers=header)

    if response.status_code != 200:
        logging.error(response.json())
        return

    payload = response.json()
    logging.debug("Items found: {}".format(payload))
    for children in payload['children']:
        if children['folder']:
            logging.debug("child {}".format(children))
            restore_trashcan_item(args, path + children['uri'])
        else:
            url = "{}/api/trash/restore/{}?to={}".format(args.url, path, path)

            if args.dry_run:
                logging.info("DRY-RUN: Restoring {}".format(url))
            else:
                logging.info("Restoring {}".format(url))
                post_response = requests.post(url, headers=header)
                logging.info(post_response.json())
            break


if __name__ == "__main__":
    sys.exit(main())
