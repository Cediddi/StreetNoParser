import argparse
import csv
import io
import json
import logging
import sys
from typing import Dict, List

import tabulate

from .parser import parse, ParseError

logger = logging.getLogger(__name__)


def build_parser():
    arg_parser = argparse.ArgumentParser(
            prog='StreetNoParser',
            description='Parses street name and house number in a naive way.',
            usage='You can provide multiple addresses by using multiple --address/-a arguments. There\'s an option to '
                  'read a line delimited file, both options can work together. You can also import this software as a '
                  'library and use the parse function as well.')
    arg_parser.add_argument('--address', '-a', type=str, nargs='+', action='append',
                            help='A street name and a house number')
    arg_parser.add_argument('--file', '-f', type=argparse.FileType('r'), nargs='?', default=None,
                            help='Input file to be parsed, addresses should be split with newline. - means stdin')
    arg_parser.add_argument('--format', '-F', type=str, nargs='?', default='json', choices=['json', 'csv', 'table'],
                            help='Output format. possible')
    return arg_parser


def process_address(args) -> List[str]:
    """Postprocess the --address/-a argument"""
    return [' '.join(addr) for addr in args.address]  # nargs=+ and action=append  will result in a List[List[str]].


def process_file(args) -> List[str]:
    """Postprocess the --file/-f argument"""
    with args.file as f:
        return [line.strip() for line in f.readlines()]  # readlines() doesn't remove the newline character.


def read_addresses(args: argparse.Namespace) -> List[str]:
    """
    Creates a address list to be parsed.
    :param args: Parsed cli arguments.
    :return: List of addresses to be processed.
    """
    all_addresses = []

    if args.address:
        addresses = process_address(args)
        all_addresses.extend(addresses)
        logger.debug(f'Read {len(addresses)} addresses from cli arguments')

    if args.file is not None:
        fname = args.file.name
        addresses = process_file(args)
        all_addresses.extend(addresses)
        logger.debug(f'Read {len(addresses)} addresses from {"stdin" if fname == "<stdin>" else fname}')

    logger.info(f'Read {len(all_addresses)}.')
    return all_addresses


def run(all_addresses: List[str]) -> List[Dict[str, str]]:
    """
    Runs the parse() function on all the addresses.
    :param all_addresses: List of addresses to be parsed
    :return: List of parsed addresses as dictionaries.
    """
    all_parsed: List[Dict[str, str]] = []
    for addr in all_addresses:
        try:
            all_parsed.append(parse(addr))
        except ParseError as e:
            logger.error(f'{e.message} - {e.address}')

    logger.info(f'Parsed {len(all_parsed)} addresses.')
    failed_count = len(all_addresses) - len(all_parsed)
    if failed_count:
        logger.warning(f'Failed to parse {failed_count} addresses.')

    return all_parsed


def format_and_print(parsed_addresses: List[Dict[str, str]], fmt: str):
    """
    Formats and prints the parsed addresses.
    :param parsed_addresses: List of parsed addresses as dictionaries.
    :param fmt: Output format.
    :return: None
    """
    buffer = io.StringIO()

    if fmt == 'json':
        json.dump(parsed_addresses, buffer)

    elif fmt == 'csv':
        writer = csv.DictWriter(buffer, fieldnames=('street', 'housenumber'))
        writer.writeheader()
        writer.writerows(parsed_addresses)

    elif fmt == 'table':
        buffer.write(tabulate.tabulate(parsed_addresses, headers='keys', tablefmt='psql'))

    buffer.seek(0)
    sys.stdout.write(buffer.read())


def main():
    """
    Main entry point.
    :return: None
    """
    arg_parser = build_parser()
    args = arg_parser.parse_args()
    all_addresses = read_addresses(args)
    results = run(all_addresses)
    if not results:
        sys.exit(1)
    else:
        format_and_print(results, fmt=args.format)
        sys.exit(0)


if __name__ == '__main__':
    main()  # pragma: no cover
