
STANDARD_LIBRARY = {
    'noop': [],
    'is_zero': ['0 ='],
    'sum': [
        ':fn done_all',
        '2 size <',
        '.',

        '0',
        '\+ \done_all while',
    ],
}