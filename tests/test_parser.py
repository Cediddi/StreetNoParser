import pytest

from StreetNoParser import parser

simple_cases = {
    'Winterallee 3': {'street': 'Winterallee', 'housenumber': '3'},
    'Musterstrasse 45': {'street': 'Musterstrasse', 'housenumber': '45'},
    'Blaufeldweg 123B': {'street': 'Blaufeldweg', 'housenumber': '123B'},
}
more_complex_cases = {
    'Am Bächle 23': {'street': 'Am Bächle', 'housenumber': '23'},
    'Auf der Vogelwiese 23 b': {'street': 'Auf der Vogelwiese', 'housenumber': '23 b'},
}
even_more_complex_cases = {
    '4, rue de la revolution': {'street': 'rue de la revolution', 'housenumber': '4'},
    '200 Broadway Av': {'street': 'Broadway Av', 'housenumber': '200'},
    'Calle Aduana, 29': {'street': 'Calle Aduana', 'housenumber': '29'},
    'Calle 39 No 1540': {'street': 'Calle 39', 'housenumber': 'No 1540'},
}
custom_cases = {
    'Öztekin Cad. No: 7': {'street': 'Öztekin Cad.', 'housenumber': 'No: 7'},  # TR
    'Bakla Sokak No: 11-13 A': {'street': 'Bakla Sokak', 'housenumber': 'No: 11-13 A'},  # TR
    '1359. Sokak No 3/B': {'street': '1359. Sokak', 'housenumber': 'No 3/B'},  # TR
    '22 Acacia Avenue': {'street': 'Acacia Avenue', 'housenumber': '22'},  # UK
    'No. 3 Abbey Road NW8': {'street': 'Abbey Road NW8', 'housenumber': 'No. 3'},  # Abbey Road Studios UK
    'Warschauer Str. 43': {'street': 'Warschauer Str.', 'housenumber': '43'},  # Berlin DE (just for luck!)
    'Cihelná 635/2b': {'street': 'Cihelná', 'housenumber': '635/2b'},  # Franz Kafka Museum CZ
}


def test_split_particles():
    # A simple case
    given = (' ', ('The quick brown fox jumps over the lazy dog',),)
    expected = ('The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog')
    assert parser.split_particles(*given) == expected

    # In place replacement
    given = (',', ('Lorem', 'ipsum', 'dolor', 'sit', 'amet,consectetur', 'adipiscing', 'elit.',),)
    expected = ('Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit.',)
    assert parser.split_particles(*given) == expected


def test_check_neighbors():
    # Plain
    given = (2, ('Bağdat', 'Cd.', '7',),)
    expected = (('Bağdat', 'Cd.',), ('7',))
    assert parser.check_neighbors(*given) == expected

    # Preceeding Neighbor
    given = (3, ('Bağdat', 'Cd.', 'No:', '7',),)
    expected = (('Bağdat', 'Cd.',), ('No:', '7',))
    assert parser.check_neighbors(*given) == expected

    # Succeeding Neighbor
    given = (2, ('Bağdat', 'Cd.', '7', 'B',),)
    expected = (('Bağdat', 'Cd.',), ('7', 'B',))
    assert parser.check_neighbors(*given) == expected

    # Preceeding and Succeeding Neighbor
    given = (3, ('Bağdat', 'Cd.', 'No:', '7', 'B',),)
    expected = (('Bağdat', 'Cd.',), ('No:', '7', 'B',))
    assert parser.check_neighbors(*given) == expected

    # Multiple possibilities second one is highly probable
    given = (3, ('12.', 'Street', 'No:', '7',),)
    expected = (('12.', 'Street',), ('No:', '7',))
    assert parser.check_neighbors(*given) == expected
    given = (0, ('12.', 'Street', 'No:', '7',),)
    expected = (('Street', 'No:', '7',), ('12.',))
    assert parser.check_neighbors(*given) == expected


def test_search_address():
    # Plain
    given = ('Bağdat', 'Cd.', '7',),
    expected = (('Bağdat', 'Cd.',), ('7',))
    assert parser.search_address(*given) == expected

    # Preceeding Neighbor
    given = ('Bağdat', 'Cd.', 'No:', '7',),
    expected = (('Bağdat', 'Cd.',), ('No:', '7',))
    assert parser.search_address(*given) == expected

    # Succeeding Neighbor
    given = ('Bağdat', 'Cd.', '7', 'B',),
    expected = (('Bağdat', 'Cd.',), ('7', 'B',))
    assert parser.search_address(*given) == expected

    # Preceeding and Succeeding Neighbor
    given = ('Bağdat', 'Cd.', 'No:', '7', 'B',),
    expected = (('Bağdat', 'Cd.',), ('No:', '7', 'B',))
    assert parser.search_address(*given) == expected

    # Multiple possibilities second one is highly probable
    given = ('12.', 'Street', 'No:', '7',),
    expected = (('12.', 'Street',), ('No:', '7',))
    assert parser.search_address(*given) == expected

    # Multiple possibilities first one is highly probable
    given = ('No:', '4', '1439', 'Guthenberg', 'Street'),
    expected = (('1439', 'Guthenberg', 'Street'), ('No:', '4',))
    assert parser.search_address(*given) == expected

    # Multiple possibilities low probability
    # This is an edge case, it may be, '12 Road, No:7' or 'No:12, Road 7'
    given = ('12', 'Road', '7',),
    expected = (('Road', '7',), ('12',))
    assert parser.search_address(*given) == expected

    # Multiple possibilities low probability
    # This is an edge case, it may be, '12 Road, No:7' or 'No:12, Road 7'
    with pytest.raises(parser.ParseError):
        given = (('Ion', 'Ghica', 'Street',),)
        parser.search_address(*given)
    with pytest.raises(parser.ParseError):
        given = (('223', ),)
        parser.search_address(*given)
    with pytest.raises(parser.ParseError):
        given = (('223', '446',),)
        parser.search_address(*given)

def test_parse_simple_cases():
    for case, expected in simple_cases.items():
        assert parser.parse(case) == expected


def test_parse_more_complex_cases():
    for case, expected in more_complex_cases.items():
        assert parser.parse(case) == expected


def test_parse_even_more_complex_cases():
    for case, expected in even_more_complex_cases.items():
        assert parser.parse(case) == expected


def test_parse_custom_cases():
    for case, expected in custom_cases.items():
        assert parser.parse(case) == expected
