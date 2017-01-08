from config.settings import server_name
from email.utils import parseaddr, formataddr, getaddresses
import table as t
import logging
import re
import hashlib
import random

# data model:

# roll-%rollid -> object ( campaign: %cid, character: %localpart, roll: str, rolled: value-str )
# campaign-rolls-%cid -> list of %rollid

# not-yet rolled rolls have no rolled field
# the campaign-rolls-%cid are used for deleting all rolls at the end of a campaign

class RollStrParseException(Exception):
    pass

ROLL_PATTERN = re.compile('^\s*(\d*D?\d+)(\s*[+-]\s*(\d*D?\d+))*\s*[\<\>]\s*\d+\s*$')


def _parse(roll_str):
    roll_str = roll_str.upper()
    if ROLL_PATTERN.match(roll_str) is None:
        raise RollStrParseException("Cannot parse '" + roll_str + "'")

    is_less_than = '<' in roll_str
    terms = re.split('\s*[\<\>]\s*', roll_str)
    limit = int(terms[1])
    
    tokens0 = re.split('\s+', terms[0])
    tokens1 = []
    for tok in tokens0:
        if '+' in tok:
            plus_tok = tok.split('+')
            first = True
            for t in plus_tok:
                if first:
                    first = False
                else:
                    tokens1.append('+')
                tokens1.append(t)
        else:
            tokens1.append(tok)
    tokens = []
    for tok in tokens1:
        if '-' in tok:
            minus_tok = tok.split('-')
            first = True
            for t in minus_tok:
                if first:
                    first = False
                else:
                    tokens.append('-')
                tokens.append(t)
        else:
            tokens.append(tok)

    parsed_tokens = []
    is_plused = True

    for tok in tokens:
        if tok == '+':
            is_plused = True
        elif tok == '-':
            is_plused = False
        else:
            parts = tok.split('D')
            if len(parts) == 1:
                parsed_tokens.append( ( is_plused, int(tok), 1) )  # 10 = 10D1
            else:
                parsed_tokens.append( ( is_plused, int(parts[0]), int(parts[1]) ) ) # 3D6

    return (parsed_tokens, is_less_than, limit)

def add_roll(campaign, character, roll_str):
   """Adds a roll, might throw a RollStrParseException if the roll_str does not validate."""

    _parse(roll_str) # validate

    while True:
        hashid = hashlib.sha256("%s-%s-%d" %
                                   (cid, character, random.randint(0,9001))).hexdigest()[0:10]
        roll_key = 'roll-%s' % (hashid,)
        if not t.has_key(roll_key):
            break

    t.create_object(roll_key, { 'campaign' : campaign, 'character' : character, 'roll': roll_str })
    t.add_to_list('campaign-' + campaign, hashid)
    return hashid


def _find_roll(hashid):
    key = "roll-" + hashid
    if not t.has_key(key):
        return None
    return t.get_object(key)
    

def find_roll(hashid):
   """Find a roll and returns the campaign, character, roll_str or None if not found or True if already rolled"""
    obj = _find_roll(hashid)
    if obj is None:
        return obj
    if 'rolled' in obj:
        return True
    return ( obj['campaign'], obj['character'], obj['roll_str'] )


def execute_roll(hashid):
    """
    Executes a roll, records it in the DB and returns its value, whether the check succeeded and its string form.
    If already rolled, returns the existing value (as a pair value, whether it succeeded or not and its string form).
    If the roll does not exist, returns None. 
    """
    obj = _find_roll(hashid)
    if obj is None:
        return obj
    if 'rolled' in obj:
        value_str, check = obj['rolled'].split(" ")
        return ( int(value_str), bool(check), obj['roll'] )

    # parse and execute the roll_str
    ( parsed_tokens, is_less_than, limit ) = _parse( obj['roll'] )

    r = random.Random()
    r.seed(int(hashid, 16)) # the hash is the result

    roll = 0
    for tok in parsed_tokens:
        value = 0
        if tok[2] == 1:
            value = tok[1]
        else:
            for v in range(tok[1]):
                value += r.randint(1, tok[2])
        if not tok[0]:
            value = -value
        roll += value

    check =  (is_less_than and (roll < limit)) or (not is_less_than and (roll > limit))

    t.set_field('roll-' + hashid, 'rolled', str(roll) + " " + str(check) )

    return ( roll, check, obj['roll'] )

