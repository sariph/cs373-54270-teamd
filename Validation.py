#!/usr/bin/env python

# -------------
# Validation.py
# -------------

import re

# ------------
# phone_number
# ------------
def phone_number (s) :
        return not re.search('^(\d\d\d-)?\d\d\d-\d\d\d\d$', s) is None
# ----------------
# phone_number_ext
# ----------------
def phone_number_ext (s) :
        return not re.search('^(\d)*$',s) is None
# ------------
# email
# ------------
def email (s) :
        return not re.search('(^(\w|\-|\_)+((\.)?(\w|\-|\_)+)*)\@(\w)+(\-|\w)*(\w)+((\.)?(\w)+(\-|\w)*(\w)+)*\.(com|net|org|gov|edu)$', s) is None
# ------------
# date
# ------------
def date (s) :
        result = False
        #Feb
        if(not re.search('^(02)\-((0[1-9])|((1|2)(\d)))\-[0-9][0-9][0-9][0-9]$',s) is None): return True
        #Jan, Mar, May...
        if(not re.search('^(01|03|05|07|08|10|12)\-(30|31|(((0[1-9])|((1|2)(\d)))))\-[0-9][0-9][0-9][0-9]$',s) is None): return True
        #Apr, Jun, Sep, Nov
        if(not re.search('^(04|06|09|11)\-(30|(((0[1-9])|((1|2)(\d)))))\-[0-9][0-9][0-9][0-9]$',s) is None): return True
        return False
# ------------
# name
# ------------
def name (s) :
        return not re.search('^^([A-Z]([a-zA-Z]*(\-|\')?[a-zA-Z]*[a-zA-Z](\')?)*(\s))+$',s) is None
# ------------
# class_number
# ------------
def class_number (s) :
        return not re.search('(^cs\d\d\d)|(^CS\d\d\d)',s) is None
# ------------
# number
# ------------
def number (s) :
        return not re.search('^(\d)+$',s) is None

# ------------
# comment
# ------------
def comment (s) :
        return not re.search('.+',s) is None

# ------------
# Degree type
# ------------
def degree_type (s) :
        return not re.search('^(PhD|Masters)$',s) is None

# ------------
# Citizen or Resident
# ------------
def citizen (s) :
        return not re.search('^(citizen|resident)$',s) is None

# ------------
# Yes or No
# ------------
def yes_no (s) :
        return not re.search('^(yes|no)$',s) is None
