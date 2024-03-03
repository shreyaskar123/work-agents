import argparse
import slug_computation

def encrypt_character(character, source, slug):
    try:
        index = source.index(character)
        return slug[index]
    except ValueError:
        return character

def encrypt_string(input_string, source, slug):
    encrypted = ''
    for character in input_string:
        encrypted += encrypt_character(character, source, slug)
    return encrypted

def decrypt_character(character, source, slug):
    try:
        index = slug.index(character)
        return source[index]
    except ValueError:
        return character

def decrypt_string(encrypted_string, source, slug):
    decrypted = ''
    for character in encrypted_string:
        decrypted += decrypt_character(character, source, slug)
    return decrypted

def encrypt_file(input_file_path, output_file_path, source, slug):
    with open(input_file_path, 'r') as file:
        content = file.read()
    encrypted_content = encrypt_string(content, source, slug)
    with open(output_file_path, 'w') as file:
        file.write(encrypted_content)

def decrypt_file(input_file_path, output_file_path, source, slug):
    with open(input_file_path, 'r') as file:
        encrypted_content = file.read()
    decrypted_content = decrypt_string(encrypted_content, source, slug)
    with open(output_file_path, 'w') as file:
        file.write(decrypted_content)

# The source alphabet
SOURCE = 'abcdefghijklmnopqrstuvwxyz'

# Define the main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=['encrypt', 'decrypt'], help='Operation to perform: encrypt or decrypt')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('--key', help='Key string for slug computation. If not provided, a default will be used')
    args = parser.parse_args()

    # Compute or use provided slug
    if args.key:
        slug = slug_computation.compute_slug(args.key)
    else:
        # A predefined slug can be placed here if required
        slug = slug_computation.compute_slug(SOURCE)

    # Perform the requested operation
    if args.operation == 'encrypt':
        encrypt_file(args.input_file, args.output_file, SOURCE, slug)
    elif args.operation == 'decrypt':
        decrypt_file(args.input_file, args.output_file, SOURCE, slug)

# Check if the script is run as main
if __name__ == '__main__':
    main()