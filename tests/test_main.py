import argparse
import io
import sys


from StreetNoParser import __main__ as main


def test_build_parser():
    assert isinstance(main.build_parser(), argparse.ArgumentParser)


def test_process_address():
    ns = argparse.Namespace()
    ns.address = [['Just', 'a', 'test', 'string'], ['Nothing', 'to', 'worry']]
    given = (ns,)
    expected = ['Just a test string', 'Nothing to worry']
    assert main.process_address(*given) == expected


def test_process_file():
    strio = io.StringIO()
    strio.writelines(['Just a test string\n', 'Nothing to worry\n'])
    strio.seek(0)

    ns = argparse.Namespace()
    ns.file = strio
    given = (ns,)
    expected = ['Just a test string', 'Nothing to worry']
    assert main.process_file(*given) == expected


def test_read_addresses():
    strio = io.StringIO()
    strio.writelines(['Just a test string from file\n', 'Nothing to worry from file\n'])
    strio.seek(0)
    strio.name = 'inmemory.txt'
    ns = argparse.Namespace()
    ns.address = [['Just', 'a', 'test', 'string', 'from', 'args'], ['Nothing', 'to', 'worry', 'from', 'args']]
    ns.file = strio
    given = (ns,)
    expected = ['Just a test string from args', 'Nothing to worry from args',
                'Just a test string from file', 'Nothing to worry from file']
    assert main.read_addresses(*given) == expected


def test_run():
    given = (('22 Acacia Avenue', 'Rue Morgue No:3'),)
    expected = [{'street': 'Acacia Avenue', 'housenumber': '22', }, {'street': 'Rue Morgue', 'housenumber': 'No:3', }]
    assert main.run(*given) == expected

    # Should continue on error.
    given = (('Acacia Avenue',),)
    expected = []
    assert main.run(*given) == expected


def test_format_and_print(capsys):
    # json
    given = (
        [{'street': 'Acacia Avenue', 'housenumber': '22', }, {'street': 'Rue Morgue', 'housenumber': 'No:3', }],
        'json'
    )
    expected = '[{"street": "Acacia Avenue", "housenumber": "22"}, {"street": "Rue Morgue", "housenumber": "No:3"}]'
    main.format_and_print(*given)
    cap_stdout, cap_stderr = capsys.readouterr()
    assert cap_stdout == expected

    # csv
    given = (
        [{'street': 'Acacia Avenue', 'housenumber': '22', }, {'street': 'Rue Morgue', 'housenumber': 'No:3', }],
        'csv'
    )
    expected = 'street,housenumber\r\nAcacia Avenue,22\r\nRue Morgue,No:3\r\n'
    main.format_and_print(*given)
    cap_stdout, cap_stderr = capsys.readouterr()
    assert cap_stdout == expected

    # table
    given = (
        [{'street': 'Acacia Avenue', 'housenumber': '22', }, {'street': 'Rue Morgue', 'housenumber': 'No:3', }],
        'table'
    )
    expected = '+---------------+---------------+\n' \
               '| street        | housenumber   |\n' \
               '|---------------+---------------|\n' \
               '| Acacia Avenue | 22            |\n' \
               '| Rue Morgue    | No:3          |\n' \
               '+---------------+---------------+'
    main.format_and_print(*given)
    cap_stdout, cap_stderr = capsys.readouterr()
    assert cap_stdout == expected


def test_main_fail(mocker):
    mocker.patch.object(sys, 'argv', [])
    mocker.patch('sys.exit')
    main.main()
    # noinspection PyUnresolvedReferences
    sys.exit.assert_called_once_with(1)


def test_main_success(mocker):
    mocker.patch.object(sys, 'argv', ['StreetNoParser', '-a', '123', 'street', 'no', '321'])
    mocker.patch('sys.exit')
    main.main()
    # noinspection PyUnresolvedReferences
    sys.exit.assert_called_once_with(0)
