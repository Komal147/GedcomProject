import sys


def process_gedcom_line(line):
    parts = line.split()

    # Check if the line has at least three elements
    if len(parts) < 2:
        print(f"Error: Invalid line - {line.strip()}. It does not have enough elements.")
        exit()

    level = int(parts[0])
    tag = parts[1]
    arguments = ' '.join(parts[2:])

    # Check if the tag is valid based on the project requirements
    valid_tags = {'INDI': 0, 'NAME': 1, 'SEX': 1, 'BIRT': 1, 'DEAT': 1, 'FAMC': 1, 'FAMS': 1, 'FAM': 0, 'MARR': 1,
                  'HUSB': 1, 'WIFE': 1, 'CHIL': 1, 'DIV': 1, 'DATE': 2, 'HEAD': 0, 'TRLR': 0, 'NOTE': 0}

    if arguments == 'INDI' or arguments == 'FAM':
        temp = tag
        tag = arguments
        arguments = temp

    if tag in valid_tags:
        expected_level = valid_tags[tag]
        is_valid = 'Y' if level == expected_level else 'N'
    else:
        is_valid = 'N'

    print(f"--> {line.strip()}")
    print(f"<-- {level}|{tag}|{is_valid}|{arguments}")


def process_gedcom_file(file_path):
    try:
        # Check if the file path is empty or contains only spaces
        if not file_path.strip():
            print("Error: The file path is invalid.")
            return

        # Check if the file is a GEDCOM file
        if not file_path.lower().endswith('.ged'):
            print("Error: The provided file is not a GEDCOM file.")
            return

        # Read the GEDCOM file line by line
        with open(file_path, 'r') as file:
            if file.readable() and file.readline() == "":
                print("Error: The file is empty.")
                return

            # Reset file pointer to the beginning
            file.seek(0)

            for line in file:
                process_gedcom_line(line)

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")


if __name__ == '__main__':
    # Check if the user provided a command line argument for the GEDCOM file path
    if len(sys.argv) != 2:
        print("Error: Please provide the GEDCOM file path as a command line argument.")
        sys.exit(1)

    gedcom_file_path = sys.argv[1]
    process_gedcom_file(gedcom_file_path)
