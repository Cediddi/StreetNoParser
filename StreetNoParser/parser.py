import logging
import math
from typing import Dict, List, Tuple

__all__ = ['parse', 'ParseError']

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Generic Parse Error"""

    def __init__(self, message: str, address: str):
        self.message = message
        self.address = address


def split_particles(delimiter: str, particles: Tuple[str]) -> Tuple[str]:
    """
    Applies splits all the strings inside a tuple using a delimiter, returns a new flat tuple. Split strings
    will be inserted to the same place.

    :param delimiter: The string you want to split with
    :param particles: A tuple of strings.
    :return: A new tuple of strings with split applied to all.
    """
    particles_list = list(particles)
    for idx in range(len(particles_list)):
        particle = particles_list.pop(idx)
        for subparticle in reversed(particle.split(delimiter)):  # type: str
            if subparticle:
                particles_list.insert(idx, subparticle)
    return tuple(particles_list)


def check_neighbors(candidate: int, particles: Tuple[str]) -> Tuple[Tuple[str], Tuple[str]]:
    """
    Checks for preceding and succeeding neighbors of a house number candidate. Takes a tuple of strings and returns two
    new tuples of strings, first one being the street and second one being the house number + neighbors if any.

    :param candidate: An index of a candidate house number.
    :param particles: A tuple of strings.
    :return: A tuple of tuples, first being the street and second being the house number + neighbors if any.
    """
    neighboring_candidates: List[int] = []

    if (candidate - 1 >= 0) and \
            (particles[candidate - 1].lower().startswith('n')):  # That's usually something like No or Number
        neighboring_candidates.append(candidate - 1)

    neighboring_candidates.append(candidate)

    if (candidate + 1 <= (len(particles) - 1)) and \
            (len(particles[candidate + 1]) == 1):  # That's usually the block name, single letter
        neighboring_candidates.append(candidate + 1)

    particles_list = list(particles)

    no = tuple(particles_list[neighboring_candidates[0]:(neighboring_candidates[-1] + 1)])
    del particles_list[neighboring_candidates[0]:(neighboring_candidates[-1] + 1)]

    street = tuple(particles_list)

    return street, no


def search_address(particles: Tuple[str]) -> Tuple[Tuple[str], Tuple[str]]:
    """
    Searches for possible house number candidates, selects the most appropriate one and returns as a tuple of tuples.

    :param particles: A tuple of strings.
    :return: A tuple of tuples, first being the street and second being the house number + neighbors if any.
    """
    candidates: List[int] = []
    for idx, particle in enumerate(particles):
        if particle[0].isdigit() or particle[-1].isdigit():  # Misses 'No:7B' but there's usually a space after ':'
            candidates.append(idx)

    if len(candidates) == 1:
        logger.debug(f'A single candidate is found.')
        candidate: int = candidates[0]
        results = check_neighbors(candidate, particles)
        if not results[0]:
            raise ParseError('Street name is missing.', ' '.join(particles))

        return results

    elif len(candidates) > 1:
        logger.debug(f'Multiple candidates are found.')
        possibilities: List[Tuple[Tuple[str], Tuple[str]]] = []
        if len(candidates) == len(particles):  # If all particles are candidates, then there's no street name.
            raise ParseError('Street name is missing.', ' '.join(particles))

        for candidate in candidates:
            results = check_neighbors(candidate, particles)
            possibilities.append(results)
        possibilities.sort(key=lambda x: len(x[1]), reverse=True)  # Longest street no match has the higher possibility

        lengths = [len(possibility[1]) for possibility in possibilities]
        total_length = sum(lengths)
        confidence = math.ceil((lengths[0] / total_length) * 100)
        logger.debug(f'Best candidate selected, confidence is {confidence}%')
        return possibilities[0]

    else:
        raise ParseError('House number is missing.', ' '.join(particles))


def parse(address: str) -> Dict[str, str]:
    """
    Parses a street name + house number combo, returns a dictionary with appropriate keys.

    :param address: The address to be parsed.
    :return: A dictionary with 'street' and 'housenumber' keys.
    """
    particles = (address,)
    particles = split_particles(' ', particles)
    if ',' in address:
        particles = split_particles(',', particles)

    logger.debug(f'{len(particles)} particles found.')

    street_tuple, housenumber_tuple = search_address(particles)
    return {'street': ' '.join(street_tuple), 'housenumber': ' '.join(housenumber_tuple)}
