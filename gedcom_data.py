from prettytable import PrettyTable
from datetime import datetime
import sys


class Individual:
    def __init__(self, identifier, name, sex, birth_date, death_date=None, childOf=None, spouseOf=None):
        self.identifier = identifier
        self.name = name
        self.sex = sex
        self.birth_date = birth_date
        self.death_date = death_date
        self.childOf = childOf
        self.spouseOf = spouseOf


class Family:
    def __init__(self, identifier, husband_id, husband_name=None, wife_id=None, wife_name=None, children=None,
                 marriage_date=None):
        self.identifier = identifier
        self.husband_id = husband_id
        self.husband_name = husband_name
        self.wife_id = wife_id
        self.wife_name = wife_name
        self.children = children
        self.marriage_date = marriage_date


def is_valid_tag(tag, level):
    valid_tags = {'INDI': 0, 'NAME': 1, 'SEX': 1, 'BIRT': 1, 'DEAT': 1, 'FAMC': 1, 'FAMS': 1, 'FAM': 0,
                  'MARR': 1, 'HUSB': 1, 'WIFE': 1, 'CHIL': 1, 'DIV': 1, 'DATE': 2, 'HEAD': 0, 'TRLR': 0, 'NOTE': 0}

    if tag in valid_tags:
        expected_level = valid_tags[tag]
        if level == expected_level:
            return True

    return False


def extract_numeric_part(identifier):
    return int(identifier[2:-1])


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d %b %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return date_str


def process_gedcom_line(file, line, individuals, families, current_individual, current_family):
    components = line.split()
    level = int(components[0])
    tag = components[1]
    arguments = ' '.join(components[2:])

    if arguments == 'INDI' or arguments == 'FAM':
        temp = tag
        tag = arguments
        arguments = temp

    if tag == 'INDI' and is_valid_tag(tag, level):
        current_individual = Individual(components[1], None, None, None)
        individuals[current_individual.identifier] = current_individual

    elif tag == 'NAME' and is_valid_tag(tag, level):
        current_individual.name = ' '.join(components[2:])

    elif tag == 'SEX' and is_valid_tag(tag, level):
        current_individual.sex = components[2]

    elif tag == 'BIRT' and is_valid_tag(tag, level):
        birth_date = ' '.join(file.readline().strip().split()[2:])
        current_individual.birth_date = format_date(birth_date)

    elif tag == 'DEAT' and is_valid_tag(tag, level):
        death_date = ' '.join(file.readline().strip().split()[2:])
        current_individual.death_date = format_date(death_date)

    elif tag == 'FAMC' and is_valid_tag(tag, level):
        current_individual.childOf = components[2]

    elif tag == 'FAMS' and is_valid_tag(tag, level):
        current_individual.spouseOf = components[2]

    elif tag == 'FAM' and is_valid_tag(tag, level):
        current_family = Family(components[1], None, None, None, None, [], None)
        families[current_family.identifier] = current_family

    elif tag == 'HUSB' and is_valid_tag(tag, level):
        current_family.husband_id = components[2]
        current_family.husband_name = individuals.get(components[2], None).name

    elif tag == 'WIFE' and is_valid_tag(tag, level):
        current_family.wife_id = components[2]
        current_family.wife_name = individuals.get(components[2], None).name

    elif tag == 'CHIL' and is_valid_tag(tag, level):
        current_family.children.append(components[2])

    elif tag == 'MARR' and is_valid_tag(tag, level):
        marriage_date = ' '.join(file.readline().strip().split()[2:])
        current_family.marriage_date = format_date(marriage_date)

    return current_individual, current_family


def parse_gedcom(file_path):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None

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
                current_individual, current_family = process_gedcom_line(file,
                                                                         line, individuals, families, current_individual,
                                                                         current_family
                                                                         )

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

    return individuals, families


if __name__ == '__main__':
    # Check if the user provided a command line argument for the GEDCOM file path
    if len(sys.argv) != 2:
        print("Error: Please provide the GEDCOM file path as a command line argument.")
        sys.exit(1)

    gedcom_file_path = sys.argv[1]

    individuals_data, families_data = parse_gedcom(gedcom_file_path)

    sorted_individuals = dict(sorted(individuals_data.items(), key=lambda x: extract_numeric_part(x[0])))
    sorted_families = dict(sorted(families_data.items(), key=lambda x: extract_numeric_part(x[0])))

    indi_table = PrettyTable(["Individual ID", "Name", "Sex", "Birth Date", "Spouse Of", "Child Of"])
    for indi_id, indi_data in sorted_individuals.items():
        indi_table.add_row(
            [indi_id, indi_data.name, indi_data.sex, indi_data.birth_date, indi_data.spouseOf, indi_data.childOf])

    print("Individuals:")
    print(indi_table)

    fam_table = PrettyTable(
        ["Family ID", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children", "Marriage Date"])
    for fam_id, fam_data in sorted_families.items():
        children_str = ", ".join(fam_data.children) if fam_data.children else 'NA'
        fam_table.add_row(
            [fam_id, fam_data.husband_id, fam_data.husband_name, fam_data.wife_id, fam_data.wife_name, children_str,
             fam_data.marriage_date])

    print("\nFamilies:")
    print(fam_table)