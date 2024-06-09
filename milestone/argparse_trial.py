import argparse

# An ambitious, but not functional, attempt.
p = argparse.ArgumentParser(add_help=False)
p.add_argument('path')
p.add_argument('args', nargs='*')
# This is where it gets weird.
p.add_argument('-', dest='flags')
# This definitely won't work if we get duplicate options.
p.add_argument('--', dest='options')

"""
Conclusion: argparse needs setup info we just can't know in advance.
argparse assumes that you have a specific parse syntax in mind. Some 
aspects of the syntax can be left indefinite (such as repetition of 
terms) but at least a few critical aspects cannot (the full names of 
supported long options.) Parsers enforce a syntax to establish the 
relationship of tokens. What we are trying to do starts at least one 
step before - separating and classifying the tokens, aka lexical 
analysis or lexing.
"""