from prettytable import PrettyTable
from datetime import datetime
import sys


class Individual:
    def __init__(self, identifier, name, sex, birth_date, death_date=None, child_of=None, spouse_of=None, age=None,
                 alive=True):
        self._identifier = identifier
        self._name = name
        self._sex = sex
        self._birth_date = birth_date
        self._death_date = death_date
        self._child_of = child_of
        self._spouse_of = spouse_of
        self._age = age
        self._alive = alive

    @property
    def identifier(self):
        return self._identifier

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def death_date(self):
        return self._death_date

    @death_date.setter
    def death_date(self, value):
        self._death_date = value

    @property
    def child_of(self):
        return self._child_of

    @child_of.setter
    def child_of(self, value):
        self._child_of = value

    @property
    def spouse_of(self):
        return self._spouse_of

    @spouse_of.setter
    def spouse_of(self, value):
        self._spouse_of = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    def calculate_age(self):
        if self.birth_date is not None:
            birth_date_obj = datetime.strptime(self.birth_date, '%Y-%m-%d')
            if self.death_date is not None:
                death_date_obj = datetime.strptime(self.death_date, '%Y-%m-%d')
                age = death_date_obj.year - birth_date_obj.year - ((death_date_obj.month, death_date_obj.day)
                                                                   < (birth_date_obj.month, birth_date_obj.day))
            else:
                age = datetime.now().year - birth_date_obj.year - ((datetime.now().month, datetime.now().day)
                                                                   < (birth_date_obj.month, birth_date_obj.day))
            return age
        return None

    def is_birth_before_death(self):
        if self.birth_date is None:
            return "Unknown Birthdate"
        elif self.death_date is None:
            return "Unknown Death Date"
        else:
            birth_date_obj = datetime.strptime(self.birth_date, '%Y-%m-%d')
            death_date_obj = datetime.strptime(self.death_date, '%Y-%m-%d')
            if birth_date_obj < death_date_obj:
                return "Yes"
            else:
                return "No"

    def find_missing_required_fields(self):
        required_fields = {
            "Name": self.name,
            "Sex": self.sex,
            "Birth Date": self.birth_date,
            "Child Of (FAMC)": self.child_of
        }

        missing_fields = [field for field, value in required_fields.items() if value is None]
        return missing_fields


class Family:
    def __init__(self, identifier, husband_id, husband_name=None, wife_id=None, wife_name=None, children=None,
                 marriage_date=None, divorce_date=None):
        self._identifier = identifier
        self._husband_id = husband_id
        self._husband_name = husband_name
        self._wife_id = wife_id
        self._wife_name = wife_name
        self._children = children
        self._marriage_date = marriage_date
        self._divorce_date = divorce_date

    @property
    def identifier(self):
        return self._identifier

    @property
    def husband_id(self):
        return self._husband_id

    @husband_id.setter
    def husband_id(self, value):
        self._husband_id = value

    @property
    def husband_name(self):
        return self._husband_name

    @husband_name.setter
    def husband_name(self, value):
        self._husband_name = value

    @property
    def wife_id(self):
        return self._wife_id

    @wife_id.setter
    def wife_id(self, value):
        self._wife_id = value

    @property
    def wife_name(self):
        return self._wife_name

    @wife_name.setter
    def wife_name(self, value):
        self._wife_name = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def marriage_date(self):
        return self._marriage_date

    @marriage_date.setter
    def marriage_date(self, value):
        self._marriage_date = value

    @property
    def divorce_date(self):
        return self._divorce_date

    @divorce_date.setter
    def divorce_date(self, value):
        self._divorce_date = value


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

    if len(components) < 2:
        print(f"Error: Invalid line - {line.strip()}. It does not have enough items.")
        exit()

    level = int(components[0])
    tag = components[1]
    arguments = ' '.join(components[2:])

    if arguments == 'INDI' or arguments == 'FAM':
        temp = tag
        tag = arguments
        arguments = temp

    if tag == 'INDI' and is_valid_tag(tag, level):
        current_individual = Individual(components[1], None, None, None, None,
                                        None, [], None, True)
        individuals[current_individual.identifier] = current_individual

    elif tag == 'NAME' and is_valid_tag(tag, level):
        current_individual.name = ' '.join(components[2:])

    elif tag == 'SEX' and is_valid_tag(tag, level):
        current_individual.sex = components[2]

    elif tag == 'BIRT' and is_valid_tag(tag, level):
        birth_date = ' '.join(file.readline().strip().split()[2:])
        current_individual.birth_date = format_date(birth_date)
        current_individual.age = current_individual.calculate_age()

    elif tag == 'DEAT' and is_valid_tag(tag, level):
        death_date = ' '.join(file.readline().strip().split()[2:])
        current_individual.death_date = format_date(death_date)
        current_individual.alive = False
        current_individual.age = current_individual.calculate_age()

    elif tag == 'FAMC' and is_valid_tag(tag, level):
        current_individual.child_of = components[2]

    elif tag == 'FAMS' and is_valid_tag(tag, level):
        current_individual.spouse_of.append(components[2])

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

    elif tag == 'DIV' and is_valid_tag(tag, level):
        divorce_date = ' '.join(file.readline().strip().split()[2:])
        current_family.divorce_date = format_date(divorce_date)

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

    indi_table = PrettyTable(["Individual ID", "Name", "Sex", "Birth Date", "Age", "Death Date", "Alive", "Spouse Of", "Child Of",
                              "Birth Before Death", "Missing Required Fields (Required fields are Name, "
                                                    "Sex, Birth Date, and Child Of"])
    for indi_id, indi_data in sorted_individuals.items():
        spouse_of_str = ", ".join(indi_data.spouse_of) if indi_data.spouse_of else 'NA'
        missing_required_fields = indi_data.find_missing_required_fields()
        missing_required_fields_str = ", ".join(missing_required_fields) if missing_required_fields else 'NA'
        is_birth_before_death = indi_data.is_birth_before_death()
        indi_table.add_row(
            [indi_id, indi_data.name, indi_data.sex, indi_data.birth_date, indi_data.age, indi_data.death_date, indi_data.alive,
             spouse_of_str, indi_data.child_of, is_birth_before_death, missing_required_fields_str])

    print("Individuals:")
    print(indi_table)

    fam_table = PrettyTable(
        ["Family ID", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children", "Marriage Date", "Divorce Date"])
    for fam_id, fam_data in sorted_families.items():
        children_str = ", ".join(fam_data.children) if fam_data.children else 'NA'
        fam_table.add_row(
            [fam_id, fam_data.husband_id, fam_data.husband_name, fam_data.wife_id, fam_data.wife_name, children_str,
             fam_data.marriage_date, fam_data.divorce_date])

    print("\nFamilies:")
    print(fam_table)
