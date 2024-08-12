# This is a sample Python script.
from time import time
from os import path, utime, rename
from re import sub
from json import load
from glob import glob

basedir = ''


def list():
    return glob(basedir + '/**', recursive=True)


# Log information to TXT File
# And if Verbose, Print it on the console
def log(msg, verbose=False):
    logfile = open("logfile.log", "a")
    logfile.write(msg)
    logfile.close()

    if verbose:
        print(msg)


# Get Timestamp from JSON-Data or Default time
def get_timestamp_or_default(data, key):
    try:
        return data[key]['timestamp']
    except KeyError:
        return time()


# Fix/Set the Date-Attributes from JSON-Data
# into MODIFIED/CREATED File-Dates
def set_dates(file, data):
    dates = [
        int(get_timestamp_or_default(data, 'photoTakenTime')),
        int(get_timestamp_or_default(data, 'creationTime')),
        int(get_timestamp_or_default(data, 'photoLastModifiedTime')),
    ]
    dates.sort()
    utime(file, (dates[0], dates[0]))


# Main Name Fixing Function
# Fix Folder-Names with Regex:
# rename in terminal:
# 's#\.(.*)(\([0-9]\)).json#$2\.$1.json#g' *
# rename these in pyhton:
# x = re.sub("\.(.*)(\([0-9]\)).json", r'\2.\1.json', txt)

def main_fix_file_names():
    for entry in list():
        if path.isfile(entry):
            file = entry
            orig_name = path.basename(file)
            fixed_name = sub(r'\.(.*)(\([0-9]\)).json', r'\2.\1.json', orig_name)

            if orig_name != fixed_name:
                log('Renaming! \r\n"{}" \r\nto \r\n"{}" \r\n'.format(
                    orig_name, fixed_name), True)
                rename(
                    path.join(basedir, orig_name),
                    path.join(basedir, fixed_name)
                )


# Main Attribute Fixing Function
def main_fix_file_attributes():
    for entry in list():
        if path.isfile(entry) and entry.endswith('.json'):
            file = entry
            s_json = path.join(basedir, file)
            s_file = path.join(basedir, path.splitext(s_json)[0])

            print('File A: "{}"'.format(s_file))
            print('File B: "{}"'.format(s_json))

            if path.isfile(s_json):
                print('  => ✅ Json exists!')

                if path.isfile(s_file):
                    print('  => ✅ File exists!')
                    data = load(open(s_json))
                    set_dates(s_file, data)
                else:
                    log('   => ❌ File-Error on: \r\n❌ "{}" \r\n✅ "{}"'
                        .format(s_file, s_json), True)
            else:
                log('   => ❌ Json-Error on: \r\n❌ "{}" \r\n✅ "{}"'
                    .format(s_json, s_file), True)


if __name__ == '__main__':
    print('Set the Base-Directory')
    basedir = input('Input full Path where to go:')

    if basedir:
        log('Selected basedir is:\r\n"{}"\r\n'.format(basedir), True)

        if path.isdir(basedir):
            print('✅ Is directory!')

            if input('Should we continue with {} Files? (y/N) '.format(len(glob(basedir)))) == 'y':

                if input('Should we fix filenames like (1).JPG with Regex renaming? (y/N) ') == 'y':
                    print('✅ Fixing Names... ')
                    main_fix_file_names()
                else:
                    print('❌ Not fixing Names... ')

                if input('Should we Continue fixing File-Attributes (y/N) ') == 'y':
                    print('✅ Start merging/fixing on File-attributes... ')
                    main_fix_file_attributes()
                else:
                    print('❌ Not fixing File-attributes... ')
            else:
                print('❌ cancelled')
            print('❌ Is not a Directory!')
