# StreetNoParser

A simple project that installs as both an executable and as a library. It can parse most street name - house number
combinatios. This software is developed with Python 3.8+ in mind and does not support 3.7 or prior.

### Installation

You can clone this repo and run setup.py while your environment is activated or you can add this git repo to your
requirements.txt.
`python setup.py install` or `pip install git+git://github.com/cediddi/StreetNoParser.git#egg=StreetNoParser`

### CLI Usage

```
usage: You can provide multiple addresses by using multiple --address/-a arguments. There's an option to read a line delimited file, both options can work together. You can also import this software as a library and use the parse function as well.

Parses street name and house number in a naive way.

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS [ADDRESS ...], -a ADDRESS [ADDRESS ...]
                        A street name and a house number
  --file [FILE], -f [FILE]
                        Input file to be parsed, addresses should be split with newline. - means stdin
  --format [{json,csv,table}], -F [{json,csv,table}]
                        Output format. possible
```

### Documentation

Module exposes only two things. parse() function and ParseError exception. Both objects have docstrings and type
annotations.

```
parse(address: str) -> Dict[str, str]
    Parses a street name + house number combo, returns a dictionary with appropriate keys.
    
    :param address: The address to be parsed.
    :return: A dictionary with 'street' and 'housenumber' keys.
```

### Testing

In order to test the software, you should clone this project, create a Python 3.8 based virtual environment, activate
the environment and then run `pip install -r requirements_tests.txt`. Then you can just run `pytest`.

## License

This software is licensed under GPLv3. You can read more at the LICENSE file.