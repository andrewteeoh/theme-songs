#!/usr/bin/python

import sys, getopt, re, sekurrity, face_recognition

def main(argv):
    name = None
    image_path = None
    classification = None
    track = None
    start_time = None

    usage = '''
    USAGE: (-nict flags required)

    python encode_image_and_save_as.py
        -n <full_name> name e.g. 'John Smith'
        -i <path_to_image> image e.g. './employees/numer_one.jpg'
        -c <employee|guest> classification e.g. 'employee' or 'guest'
        -t <track_id> from spotify e.g. 02DurCgOvDdX0uKEjqcl3W
        -s <start_time> in seconds e.g. to start 107 seconds in: -s 107
        '''

    try:
        opts, args = getopt.getopt(argv,"n:i:c:t:s::")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    if len(opts) == 0:
        print(usage)
        sys.exit()
    for opt, arg in opts:
        if opt == '-n':
            name = arg
        elif opt == '-i':
            image_path = arg
        elif opt == '-c':
            classification = arg
        elif opt == '-t':
            track = arg
        elif opt == '-s':
            print(opt)
            print(arg)
            start_time = arg.strip()

    is_missing_args = name is None or image_path is None or classification is None or track is None
    are_invalid_params = classification != 'employee' and classification != 'guest'

    if is_missing_args:
        print('missing_args')

    if are_invalid_params:
        print('invalid_params')

    if is_missing_args or are_invalid_params:
        print(usage)
        sys.exit()

    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]

    start_time_begins_with_non_digit = re.compile('^\d').match(start_time) is None
    if start_time is None or start_time_begins_with_non_digit:
        start_seconds = 0
    else:
        digits = re.compile('(\d)+').search(start_time).group()
        start_seconds= int(digits)

    sekurrity.save_new_face(name, classification, encoding, track, start_seconds)

if __name__ == "__main__":
   main(sys.argv[1:])
