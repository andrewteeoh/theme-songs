#!/usr/bin/python

import sys, getopt, sekurrity, face_recognition

def main(argv):
    name = None
    image_path = None
    classification = None
    usage = '''
    USAGE: (all flags required)

    python encode_image_and_save_as.py
        -n <full_name> name e.g. 'John Smith'
        -i <path_to_image> image e.g. './employees/numer_one.jpg'
        -c <employee|guest> classification e.g. 'employee' or 'guest' '''

    try:
        opts, args = getopt.getopt(argv,"hn:i:c:", ['name=','image=','classification='])
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

    is_missing_args = name is None or image_path is None or classification is None
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

    sekurrity.save_new_face(name, classification, encoding)

if __name__ == "__main__":
   main(sys.argv[1:])
