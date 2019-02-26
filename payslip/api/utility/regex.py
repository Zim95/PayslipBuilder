import re


EMPLOYEE_REGEX_CODE = [
    ('^VS\-[0-9]{3}\-BH[0-9]{4}$', 'varadhi')
]

DATATYPE_REGEX_CODE = [
    ('^Integer$', 'INTEGER'),
    ('^Float$', 'FLOAT'),
    ('^Character$', 'VARCHAR'),
    ('^Dropdown$', 'VACHAR'),
    ('^Boolean$', 'BOOLEAN'),
    ('^Operation$', 'FLOAT')
]

ALLOWED_META_VALUES = {
    'Character': '^\d+$',
    'Boolean': '(Yes|No)',
    'Operation': '(concat([a-zA-Z0-9]+,[a-zA-Z0-9]+)|[a-zA-Z0-9]+[\-\+\*\/\^\(\)][a-zA-Z0-9]+)',
    'Dropdown': '^(\S+)$'
}

EXPECTED_META = {
    'Character': 'size',
    'Boolean': 'default',
    'Integer': None,
    'Float': None,
    'Operation': 'operation',
    'Date': None,
    'Time': None,
    'DateTime': None,
    'Dropdown': 'choices'
}


def lookupfieldsmeta(field, valuetype, lookuptype):
    if lookuptype == "allowedtype":
        if re.search(ALLOWED_META_VALUES[valuetype], field):
            return True
        else:
            return False


def lookup(s, valuetype):
    if valuetype == "employee":
        for pattern, value in EMPLOYEE_REGEX_CODE:
            if re.search(pattern, s):
                return str(value)
        return None
    elif valuetype == "dbtype":
        for pattern, value in DATATYPE_REGEX_CODE:
            if re.search(pattern, s):
                return str(value)
        return None
    elif valuetype == "allowedtype":
        for pattern, value in ALLOWED_VALUES:
            if re.search(value, s):
                return True
        return False
    else:
        return None
