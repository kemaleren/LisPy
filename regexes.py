import re

#some useful regexes:
ATOM_regex = re.compile("^[0-9a-zA-Z%*\-\+/=<>]+$")
INT_regex = re.compile("^-?[0-9]+$|^\+?[0-9]+$")
WHITESPACE_regex = re.compile("^\s+$")
