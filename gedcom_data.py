from prettytable import PrettyTable
from datetime import datetime, date
import sys


class Individual:
    def __init__(self, identifier, name, sex, birth_date, death_date=None, child_of=None, spouse_of=None, age=None,
                 is_duplicate=False, alive=True, mother=None, father=None, number_of_siblings=0, marriage_info=None):
        self._identifier = identifier
        self._name = name
        self._sex = sex
        self._birth_date = birth_date
        self._death_date = death_date
        self._child_of = child_of
        self._spouse_of = spouse_of
        self._age = age
        self._alive = alive
        self._is_duplicate = is_duplicate
        self._mother = mother
        self._father = father
        self._number_of_siblings = number_of_siblings
        self._marriage_info = marriage_info

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

    @property
    def mother(self):
        return self._mother

    @mother.setter
    def mother(self, value):
        self._mother = value

    @property
    def father(self):
        return self._father

    @father.setter
    def father(self, value):
        self._father = value

    @property
    def number_of_siblings(self):
        return self._number_of_siblings

    @number_of_siblings.setter
    def number_of_siblings(self, value):
        self._number_of_siblings = value

    @property
    def marriage_info(self):
        return self._marriage_info

    @marriage_info.setter
    def marriage_info(self, value):
        self._marriage_info = value

    def fifteen_or_more_siblings(self, individuals):
        if self.child_of:
            siblings = [ind for ind in individuals.values() if
                        ind.child_of == self.child_of and ind.identifier != self.identifier]
            self.number_of_siblings = len(siblings)
        else:
            self.number_of_siblings = 0
        if self.number_of_siblings >= 15:
            return f"ERROR: INDIVIDUAL: US15: {self.identifier}: The individual has 15 siblings or more."

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
        if (self.birth_date is not None and self.birth_date.strip() != "") and (
                self.death_date is not None and self.death_date.strip() != ""):
            birth_date_obj = datetime.strptime(self.birth_date, '%Y-%m-%d')
            death_date_obj = datetime.strptime(self.death_date, '%Y-%m-%d')
            if birth_date_obj >= death_date_obj:
                return f"ERROR: INDIVIDUAL: US03: {self.identifier}: Birthdate {self.birth_date} is the same as or after death date {self.death_date}"

    def find_missing_required_fields(self):
        required_fields = {
            "Name": self.name,
            "Sex": self.sex,
            "Birth Date": self.birth_date,
            "Child Of (FAMC)": self.child_of
        }

        missing_fields = [field for field, value in required_fields.items() if not value]

        if missing_fields:
            return f"ERROR: INDIVIDUAL: US23: {self.identifier}: Missing required fields {', '.join(missing_fields)}"

    def add_marriage_info(self, families, individuals):
        self._marriage_info = []
        spouse_id = ''
        spouse_death_date = ''
        for spouse in self.spouse_of:
            if families:
                for fam_id, family in families.items():
                    if spouse == family.identifier:
                        if family.husband_id == self.identifier:
                            spouse_id = family.wife_id
                        elif family.wife_id == self.identifier:
                            spouse_id = family.husband_id

                        for indi_id, individual in individuals.items():
                            if individual.identifier == spouse_id:
                                spouse_death_date = individual.death_date

                        self._marriage_info.append({
                            'family_id': family.identifier,
                            'marriage_date': family.marriage_date,
                            'divorce_date': family.divorce_date,
                            'spouse_id': spouse_id,
                            'spouse_death_date': spouse_death_date
                        })

    def detect_bigamy(self):
        marriages = self.marriage_info
        if len(marriages) > 1:
            marriages.sort(key=lambda x: x['marriage_date'])
            for i in range(len(marriages) - 1):
                if not marriages[i]['divorce_date']:
                    if not marriages[i]['spouse_death_date']:
                        return f"ERROR: INDIVIDUAL: US11: {self.identifier}: Bigamy has been detected. {self.name} is married to multiple individuals at the same time."
                    elif marriages[i]['spouse_death_date'] and marriages[i + 1]['marriage_date'] < marriages[i][
                        'spouse_death_date']:
                        return f"ERROR: INDIVIDUAL: US11: {self.identifier}: Bigamy has been detected. {self.name} is married t0 multiple individuals at the same time."
                elif marriages[i + 1]['marriage_date'] < marriages[i]['divorce_date']:
                    return f"ERROR: INDIVIDUAL: US11: {self.identifier}: Bigamy has been detected. {self.name} is married to multiple individuals at the same time."

    def age_at_date(self, event_date):
        delta = 0
        years = 0
        event_date = datetime.strptime(event_date, "%Y-%m-%d")  # Convert event_date to datetime object
        if self.birth_date and not isinstance(self.birth_date, datetime):
            self.birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d")

        if self.birth_date:
            delta = event_date - self.birth_date

        if delta:
            years = delta.days // 365

        return years


class Family:
    def __init__(self, identifier, husband_id, husband_name=None, wife_id=None, wife_name=None, children=None,
                 marriage_date=None, divorce_date=None, is_duplicate=False, childrenIds=None, husband=None, wife=None):
        self._identifier = identifier
        self._husband_id = husband_id
        self._husband_name = husband_name
        self._wife_id = wife_id
        self._wife_name = wife_name
        self._children = children
        self._marriage_date = marriage_date
        self._divorce_date = divorce_date
        self._is_duplicate = is_duplicate
        self._childrenIds = childrenIds
        self._husband = husband
        self._wife = wife

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

    @property
    def childrenIds(self):
        return self._childrenIds

    @childrenIds.setter
    def childrenIds(self, value):
        self._childrenIds = value

    @property
    def husband(self):
        return self._husband

    @husband.setter
    def husband(self, value):
        self._husband = value

    @property
    def wife(self):
        return self._wife

    @wife.setter
    def wife(self, value):
        self._wife = value


    def parentsTooOld(self, individual):
            
            if (self.wife != None and self.wife.birth_date - individual.birth_date > 60) or (self.husband != None and self.husband.birth_date - individual.birth_date > 80):
             return (f"ERROR: FAMILY: US12: {individual.identifier}: "
                        f"One of the parents is too old compared to the child")
            
            return ""
       

    def unique_family_names(self):

        # todo return the reason why
        for child in self._children:
            if (child.name == None):
                name = "Unknown"
            else:
                name = child.name.split(" ")[0]

            if (self.husband_name == None):
                husband_name = "Unknown"
            else:
                husband_name = self.husband_name.split(" ")[0]

            if (self.wife_name == None):
                wife_name = "Unknown"
            else:
                wife_name = self.wife_name.split(" ")[0]
            birthday = child.birth_date
            if (name == husband_name):
                return "ERROR: FAMILY: US25: " + self.identifier + ": Child " + name + " has the same name as father " + husband_name
            elif name == wife_name:
                return "ERROR: FAMILY: US25: " + self.identifier + ": Child " + name + " has the same name as mother " + wife_name
            for child2 in self._children:
                if (child2.name == None):
                    name2 = "Unknown"
                else:
                    name2 = child2.name.split(" ")[0]
                birthday2 = child2.birth_date
                if (birthday2 != birthday):
                    if (name == name2):
                        "ERROR: FAMILY: US25: " + self.identifier + ": Child " + name + " has the same name as sibling " + name2
        return ""

    def children_before_marriage(self):
        # todo return the reason why
        if self.marriage_date is not None:
            marriage_date_obj = datetime.strptime(self.marriage_date, '%Y-%m-%d')
            for child in self._children:
                if child.birth_date is not None:
                    child_birth_date_obj = datetime.strptime(child.birth_date, '%Y-%m-%d')
                    if child_birth_date_obj < marriage_date_obj:
                        return "ERROR: FAMILY: US02: " + self.identifier + ": Child " + child.identifier + " was born before marriage on " + self.marriage_date
        return ""

    def is_marriage_before_14(self, individuals):
        if not self.marriage_date:
            return None

        for indi_id, individual in individuals.items():
            if individual.identifier == self.husband_id:
                self.husband = individual
            elif individual.identifier == self.wife_id:
                self.wife = individual

        if self.husband and self.wife:
            if self.husband.age_at_date(self.marriage_date) < 14 or self.wife.age_at_date(self.marriage_date) < 14:
                return f"ERROR: FAMILY: US10: {self.identifier}: Marriage occurred before one of the spouses reached 14 years of age."
        return None


def set_parents_of_individuals(individuals, families):
    for ind_id, individual in individuals.items():
        child_of_family = individual.child_of
        mother_id = ''
        father_id = ''

        for fam_id, family in families.items():
            if fam_id and child_of_family == fam_id:
                mother_id = family.wife_id
                father_id = family.husband_id

        for parent_id, potential_parent in individuals.items():
            if parent_id and parent_id == mother_id:
                individual.mother = potential_parent
            elif parent_id and parent_id == father_id:
                individual.father = potential_parent


def is_individual_birth_date_after_parent_death_date(individual):
    if (
            individual.birth_date and individual.mother and individual.mother.death_date and individual.birth_date > individual.mother.death_date) and (
            individual.birth_date and individual.father and individual.father.death_date and individual.birth_date > individual.father.death_date):
        return (f"ERROR: INDIVIDUAL: US09: {individual.identifier}: "
                f"Birth date {individual.birth_date} is after mother's death date {individual.mother.death_date} and after father's death date {individual.father.death_date}")
    elif individual.birth_date and individual.mother and individual.mother.death_date and individual.birth_date > individual.mother.death_date:
        return (f"ERROR: INDIVIDUAL: US09: {individual.identifier}: "
                f"Birth date {individual.birth_date} is after mother's death date {individual.mother.death_date}")


def is_valid_tag(tag, level):
    valid_tags = {'INDI': 0, 'NAME': 1, 'SEX': 1, 'BIRT': 1, 'DEAT': 1, 'FAMC': 1, 'FAMS': 1, 'FAM': 0,
                  'MARR': 1, 'HUSB': 1, 'WIFE': 1, 'CHIL': 1, 'DIV': 1, 'DATE': 2, 'HEAD': 0, 'TRLR': 0, 'NOTE': 0}

    if tag in valid_tags:
        expected_level = valid_tags[tag]
        if level == expected_level:
            return True

    return False


def print_missing_required_fields_for_all_individuals(individuals):
    for individual in individuals.values():
        missing_required_fields_str = individual.find_missing_required_fields()
        if missing_required_fields_str:
            print(missing_required_fields_str)


def print_birth_before_death_errors_for_all_individuals(individuals):
    for individual in individuals.values():
        birth_before_death_error_str = individual.is_birth_before_death()
        if birth_before_death_error_str:
            print(birth_before_death_error_str)


def extract_numeric_part(identifier):
    return int(identifier[2:-1])


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d %b %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return date_str


def process_gedcom_line(file, line, individuals, families, current_individual, current_family, duplicate_individual,
                        duplicate_family):
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
        indi_id = components[1]
        if indi_id in individuals:
            individuals[indi_id].is_duplicate = True
            duplicate_individual.append(indi_id)
        else:
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
        fam_id = components[1]
        if fam_id in families:
            families[fam_id].is_duplicate = True
            duplicate_family.append(fam_id)
        else:
            current_family = Family(components[1], None, None, None, None, [], None, childrenIds=[])
            families[current_family.identifier] = current_family

    elif tag == 'HUSB' and is_valid_tag(tag, level):
        current_family.husband_id = components[2]
        husband = individuals.get(components[2], None)
        if husband is not None:
            current_family.husband_name = husband.name

    elif tag == 'WIFE' and is_valid_tag(tag, level):
        current_family.wife_id = components[2]
        wife = individuals.get(components[2], None)
        if wife is not None:
            current_family.wife_name = wife.name

    elif tag == 'CHIL' and is_valid_tag(tag, level):
        current_family.children.append(individuals.get(components[2], None))
        current_family.childrenIds.append(components[2])

    elif tag == 'MARR' and is_valid_tag(tag, level):
        marriage_date = ' '.join(file.readline().strip().split()[2:])
        current_family.marriage_date = format_date(marriage_date)

    elif tag == 'DIV' and is_valid_tag(tag, level):
        divorce_date = ' '.join(file.readline().strip().split()[2:])
        current_family.divorce_date = format_date(divorce_date)
    return current_individual, current_family, duplicate_individual, duplicate_family


def getCurrDate():
    curr_date = str(datetime.now().today())
    return curr_date


def convertDateFormat(date):
    temp = date.split()
    if (temp[1] == 'JAN'): temp[1] = '01';
    if (temp[1] == 'FEB'): temp[1] = '02';
    if (temp[1] == 'MAR'): temp[1] = '03';
    if (temp[1] == 'APR'): temp[1] = '04';
    if (temp[1] == 'MAY'): temp[1] = '05';
    if (temp[1] == 'JUN'): temp[1] = '06';
    if (temp[1] == 'JUL'): temp[1] = '07';
    if (temp[1] == 'AUG'): temp[1] = '08';
    if (temp[1] == 'SEP'): temp[1] = '09';
    if (temp[1] == 'OCT'): temp[1] = '10';
    if (temp[1] == 'NOV'): temp[1] = '11';
    if (temp[1] == 'DEC'): temp[1] = '12';
    if (temp[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
        temp[2] = '0' + temp[2]
    return (temp[0] + '-' + temp[1] + '-' + temp[2])


def DatesBeforeCurrDate(individuals, families):
    curr_date = getCurrDate()
    bad_date_list = []

    for indi_id, indi_data in individuals.items():
        if indi_data.birth_date is not None and indi_data.birth_date > curr_date:
            bad_date_list.append(indi_data.birth_date)
            print(f"ERROR: INDIVIDUAL: US01: {extract_numeric_part(indi_id)}: Birthday {indi_data.birth_date}")

        if not indi_data.alive and indi_data.death_date is not None and indi_data.death_date > curr_date:
            bad_date_list.append(indi_data.death_date)
            print(f"ERROR: INDIVIDUAL: US01: {extract_numeric_part(indi_id)}: Death Date {indi_data.death_date}")

    for fam_id, fam_data in families.items():
        if fam_data.marriage_date is not None and fam_data.marriage_date > curr_date:
            bad_date_list.append(fam_data.marriage_date)
            print(f"ERROR: FAMILY: US01: {extract_numeric_part(fam_id)}: Marriage Date {fam_data.marriage_date}")

        if fam_data.divorce_date is not None and fam_data.divorce_date > curr_date:
            bad_date_list.append(fam_data.divorce_date)
            print(f"ERROR: FAMILY: US01: {extract_numeric_part(fam_id)}: Divorce Date {fam_data.divorce_date}")

    if not bad_date_list:
        print("US01: All the Dates are before the current date.")
        return 'Yes'
    else:
        return 'No'
    

def check_death_and_age(individuals):
    bad_date_list = []
    bad_age = []

    for indi_id, indi_data in individuals.items():
        if not indi_data.alive and indi_data.death_date is not None:
            death_date_obj = datetime.strptime(indi_data.death_date, '%Y-%m-%d')
            birth_date_obj = datetime.strptime(indi_data.birth_date, '%Y-%m-%d')
            age_at_death = death_date_obj.year - birth_date_obj.year - (
                    (death_date_obj.month, death_date_obj.day) < (birth_date_obj.month, birth_date_obj.day))
            if age_at_death is not None and age_at_death > 150:
                bad_date_list.append(age_at_death)
                print(f"ERROR: INDIVIDUAL: US07: {extract_numeric_part(indi_id)}: Age at death is: {age_at_death} greater than 150 years.")

        if indi_data.alive and indi_data.birth_date is not None:
            if indi_data.age is not None and indi_data.age > 150:
                bad_age.append(indi_data.age)
                print(f"ERROR: INDIVIDUAL: US07: {extract_numeric_part(indi_id)}: Age from birth is: {indi_data.age} greater than 150 years.")

    if not bad_date_list and not bad_age:  # Corrected conditional logic
        print("US07: Age is less than 150 years")
        return 'Yes'
    else:
        return 'No'
    
def check_marriage_and_divorce_date(sorted_families):
    errors = []

    for fam_id, fam_data in sorted_families.items():
        marriage_date = fam_data.marriage_date
        divorce_date = fam_data.divorce_date

        if marriage_date is not None and divorce_date is not None:
            if marriage_date > divorce_date:
                errors.append(marriage_date)
                print(f"ERROR: FAMILY: US04: {extract_numeric_part(fam_id)} : Divorce occurs before marriage")
        elif marriage_date is None and divorce_date is not None:
            errors.append(marriage_date)
            print(f"ERROR: FAMILY: US04: {extract_numeric_part(fam_id)}: Divorce date specified but marriage date is missing")

    if not errors:
        print(f"US04: {extract_numeric_part(fam_id)} : Marriage occure before divorce")
        return 'Yes'
    else:
        return 'No'


def check_marriage_before_death(sorted_families, sorted_individuals):
    errors = []

    for fam_id, fam_data in sorted_families.items():
        marriage_date = fam_data.marriage_date
        husband_id = fam_data.husband_id
        wife_id = fam_data.wife_id

        if marriage_date is not None:
            if husband_id in sorted_individuals:
                husband_death_date = sorted_individuals[husband_id].death_date
                if husband_death_date is not None and marriage_date > husband_death_date:
                    errors.append(husband_death_date)
                    print(f"ERROR: FAMILY: US05: {extract_numeric_part(fam_id)}: Marriage occurs after husband's death. ID: {husband_id} Death date:{husband_death_date}")

            if wife_id in sorted_individuals:
                wife_death_date = sorted_individuals[wife_id].death_date
                if wife_death_date is not None and marriage_date > wife_death_date:
                    errors.append(wife_death_date)
                    print(f"ERROR: FAMILY: US05: {extract_numeric_part(fam_id)}: Marriage occurs after wife's death. ID: {wife_id} Death date:{wife_death_date}")
    if not errors:
        print(f"US05: {extract_numeric_part(fam_id)}: Marriage occure before death of spouse")
        return 'Yes'
    else:
        return 'No'



def check_sibling_birth_dates(individuals, families):
    sibling_birth_dates = {}

    for fam_id, fam_data in families.items():
        for child_id in fam_data.childrenIds:
            birth_date = individuals[child_id].birth_date
            if birth_date in sibling_birth_dates:
                sibling_birth_dates[birth_date].append(child_id)
            else:
                sibling_birth_dates[birth_date] = [child_id]

    for birth_date, sibling_ids in sibling_birth_dates.items():
        if len(sibling_ids) >= 5:
            print(f"ERROR: FAMILY: US15: More than five siblings born on the same date ({birth_date}): {', '.join(sibling_ids)}")

            

def parse_gedcom(file_path):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    duplicate_individual = []
    duplicate_family = []

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
                current_individual, current_family, duplicate_individual, duplicate_family = process_gedcom_line(file,
                                                                                                                 line,
                                                                                                                 individuals,
                                                                                                                 families,
                                                                                                                 current_individual,
                                                                                                                 current_family,
                                                                                                                 duplicate_individual,
                                                                                                                 duplicate_family
                                                                                                                 )
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
    return individuals, families, duplicate_individual, duplicate_family


if __name__ == '__main__':
    # Check if the user provided a command line argument for the GEDCOM file path
    if len(sys.argv) < 2:
        print("Error: Please provide the GEDCOM file path as a command line argument.")
        sys.exit(1)

    gedcom_file_path = sys.argv[1]

    individuals_data, families_data, duplicate_individual, duplicate_family = parse_gedcom(gedcom_file_path)

    sorted_individuals = dict(sorted(individuals_data.items(), key=lambda x: extract_numeric_part(x[0])))

    sorted_families = dict(sorted(families_data.items(), key=lambda x: extract_numeric_part(x[0])))

    indi_table = PrettyTable(
        ["Individual ID", "Name", "Sex", "Birth Date", "Age", "Death Date", "Alive", "Spouse Of", "Child Of"])

    for indi_id, indi_data in sorted_individuals.items():
        spouse_of_str = ", ".join(indi_data.spouse_of) if indi_data.spouse_of else 'NA'
        indi_table.add_row(
            [indi_id, indi_data.name, indi_data.sex, indi_data.birth_date, indi_data.age, indi_data.death_date,
             indi_data.alive,
             spouse_of_str, indi_data.child_of])

    print("Individuals:")
    print(indi_table)

    fam_errors = []

    fam_table = PrettyTable(
        ["Family ID", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children", "Marriage Date",
         "Divorce Date"])
    

    for fam_id, fam_data in sorted_families.items():
        if (fam_data.unique_family_names() != ""):
            fam_errors.append(fam_data.unique_family_names())
        elif fam_data.children_before_marriage() != "":
            fam_errors.append(fam_data.children_before_marriage())
        else:
            children_str = ", ".join(fam_data.childrenIds) if fam_data.childrenIds else 'NA'
            fam_table.add_row(
                [fam_id, fam_data.husband_id, fam_data.husband_name, fam_data.wife_id, fam_data.wife_name, children_str,
                 fam_data.marriage_date, fam_data.divorce_date])
        
        for child_id in fam_data.childrenIds:
            child = sorted_individuals[child_id]
            if fam_data.parentsTooOld(child) != "":
                fam_errors.append(fam_data.parentsTooOld(child))

    print("\nFamilies:")
    print(fam_table)

    # Access and print information about duplicate individuals
    for duplicate_individual_id in duplicate_individual:
        print(
            f"ERROR: INDIVIDUAL: US22: {extract_numeric_part(duplicate_individual_id)}: Duplicate Individual Id: {duplicate_individual_id}")

    # Access and print information about duplicate Family
    for duplicate_family_id in duplicate_family:
        print(
            f"ERROR: FAMILY: US22: {extract_numeric_part(duplicate_family_id)}: Duplicate Family Id: {duplicate_family_id}")

    DatesBeforeCurrDate(sorted_individuals, sorted_families)
    check_death_and_age(sorted_individuals)
    check_sibling_birth_dates(sorted_individuals, sorted_families)
    check_marriage_and_divorce_date(sorted_families)
    check_marriage_before_death(sorted_families, sorted_individuals)


    fam_errors.sort()
    print()
    for err in fam_errors:
        print(err)

    print_missing_required_fields_for_all_individuals(sorted_individuals)
    print_birth_before_death_errors_for_all_individuals(sorted_individuals)

    set_parents_of_individuals(sorted_individuals, sorted_families)

    for ind_id, individual in sorted_individuals.items():
        error = is_individual_birth_date_after_parent_death_date(individual)
        if error:
            print(error)

        fifteen_or_more_siblings_error = individual.fifteen_or_more_siblings(sorted_individuals)
        if fifteen_or_more_siblings_error:
            print(fifteen_or_more_siblings_error)

    # Populate marriage information for each individual
    for individual in sorted_individuals.values():
        individual.add_marriage_info(sorted_families, sorted_individuals)

    # Detect bigamy for each individual
    for individual in sorted_individuals.values():
        bigamy_error = individual.detect_bigamy()
        if bigamy_error:
            print(bigamy_error)

    for family in sorted_families.values():
        marriage_before_14_error = family.is_marriage_before_14(sorted_individuals)
        if marriage_before_14_error:
            print(marriage_before_14_error)
