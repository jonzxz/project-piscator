from argparse import ArgumentParser
from cryptography.fernet import Fernet


# Generates an symmetric encryption key based off the Fernet symmetric encryption scheme
# Usage: py -m generate_key -o <OUTPUT_FILE.KEY>
def generate_key():
    parser = ArgumentParser("KeyGenerator")
    parser.add_argument("-o", dest="output_file")
    args = parser.parse_args()

    print("Output file: {}".format(args.output_file))
    print("Generating Fernet Key..")
    key = Fernet.generate_key()
    with open(args.output_file, 'wb') as out_file:
        out_file.write(key)
        out_file.close()
    print("Key file generated. Place this in the project root.")

generate_key()
