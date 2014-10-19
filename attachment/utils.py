#attachment/utils.py

def generate_file(fname):
    """Generate a dummy file, typically for upload testing

    Concept from http://stackoverflow.com/a/11171303/1593443"""

    gen_file = open(fname, 'a+')
    gen_file.write('Testing file upload?')
    gen_file.write('Does it work?')

    return gen_file

