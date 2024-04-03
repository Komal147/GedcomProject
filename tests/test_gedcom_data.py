import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

import gedcom_data
from gedcom_data import DatesBeforeCurrDate, check_marriage_and_divorce_date, check_death_and_age, \
    check_marriage_before_death
import unittest


def initData():
    individuals = [gedcom_data.Individual("@I1@", "Tyler", "M", "1999-08-31", None, "", "", 24, False, True),
                   gedcom_data.Individual("@I2@", "John", "M", "2003-12-13", None, "", "", 20, False, True),
                   gedcom_data.Individual("@I3@", "Jane", "F", "1997-08-23", "2018-02-12", "", "", 27, False, False),
                   gedcom_data.Individual("@I4@", "Jill", "F", "1995-05-08", None, "", "", 29, False, True),
                   gedcom_data.Individual("@I5@", "Jack", "M", "1987-02-12", None, "", "", 37, False, True),
                   gedcom_data.Individual("@I6@", "Erica", "F", "2017-01-19", None, "", "", 7, False, True),
                   gedcom_data.Individual("@I7@", "Jeffery", "M", "1997-11-17", None, "", "", 27, False, True),
                   gedcom_data.Individual("@I8@", "Willow", "F", "1999-12-27", None, "", "", 24, False, True),
                   gedcom_data.Individual("@I9@", "Gavin", "M", "1993-012-26", None, "", "", 31, False, True),
                   gedcom_data.Individual("@I10@", "Hannah", "F", "1977-03-22", None, "", "", 47, False, False),
                   gedcom_data.Individual("@I11@", "Jack", "M", "2010-02-13", None, "", "", 37, False, True),
                   ]

    families = [
        gedcom_data.Family("@F1@", "@I2@", "John", "@I3@", "Jane", [individuals[1], individuals[2]], "2018-11-12", None,
                           ["@I2@", "@I3@"]),
        gedcom_data.Family("@F2@", "@I4@", "Jill", "@I5@", "Jack", [individuals[5]], "2016-12-25", None, ["@I6@"]),
        gedcom_data.Family("@F3@", "@I6@", "Erica", "@I7@", "Jeffery", [], "1999-11-12", "2015-11-12", []),
        gedcom_data.Family("@F4@", "@I8@", "Willow", "@I9@", "Gavin", [], "2010-11-12", None, []),
        gedcom_data.Family("@F5@", "@I10@", "Hannah", "@I5@", "Jack", [], "2010-11-12", "1980-11-12", []), ]

    return families, individuals


class TestGedcomFamilyUniqueFamilyNames(unittest.TestCase):

    def setUp(self):
        self.families, self.individuals = initData()

    def test_unique_family_names_true(self):
        family_data = self.families[0]
        self.assertTrue(family_data.unique_family_names() != "")

    def test_unique_family_names_false(self):
        family_data = self.families[1]
        self.assertEqual(family_data.unique_family_names(), "")

    def test_unique_family_names_no_children(self):
        family_data = self.families[2]
        self.assertEqual(family_data.unique_family_names(), "")


class TestGedcomBirthBeforeMarriage(unittest.TestCase):

    def setUp(self):
        self.families, self.individuals = initData()

    def test_birth_before_marriage_true(self):
        family_data = self.families[0]
        self.assertTrue(family_data.children_before_marriage() != "")

    def test_birth_before_marriage_false(self):
        family_data = self.families[1]
        self.assertEqual(family_data.children_before_marriage(), "")

    def test_birth_before_marriage_no_children(self):
        family_data = self.families[2]
        self.assertEqual(family_data.children_before_marriage(), "")

    def test_birth_before_marriage_none_date(self):
        family_data = self.families[3]
        self.assertEqual(family_data.children_before_marriage(), "")

    def test_birth_before_marriage_no_children_second(self):
        family_data = self.families[4]
        self.assertEqual(family_data.children_before_marriage(), "")


class TestGedcomDatesBeforeCurrDate(unittest.TestCase):

    def setUp(self):
        self.families, self.individuals = initData()

    def test_dates_before_curr_date_true(self):
        # Test case where all dates are before the current date

        expected_output = 'Yes'

        indi = self.individuals[0]
        individuals_dict = {indi.identifier: indi}

        fam = self.families[0]
        families_dict = {fam.identifier: fam}

        result = DatesBeforeCurrDate(individuals_dict, families_dict)
        self.assertEqual(result, expected_output)

    def test_dates_before_curr_date_birthdate_false(self):
        # Test case where birthdate are after the current date

        expected_output = 'No'

        indi = self.individuals[1]
        indi.birth_date = '2026-05-08'
        individuals_dict = {indi.identifier: indi}

        fam = self.families[1]
        families_dict = {fam.identifier: fam}

        result = DatesBeforeCurrDate(individuals_dict, families_dict)
        self.assertEqual(result, expected_output)

    def test_dates_before_curr_date_deathdate_false(self):
        # Test case where death date are after the current date

        expected_output = 'No'

        indi = self.individuals[2]
        indi.death_date = '2035-09-01'
        individuals_dict = {indi.identifier: indi}

        fam = self.families[2]
        families_dict = {fam.identifier: fam}

        result = DatesBeforeCurrDate(individuals_dict, families_dict)
        self.assertEqual(result, expected_output)

    def test_dates_before_curr_date_marriagedate_false(self):
        # Test case where marriage date are after the current date

        expected_output = 'No'

        indi = self.individuals[0]
        individuals_dict = {indi.identifier: indi}

        fam = self.families[0]
        fam.marriage_date = '2030-10-12'
        families_dict = {fam.identifier: fam}

        result = DatesBeforeCurrDate(individuals_dict, families_dict)
        self.assertEqual(result, expected_output)

    def test_dates_before_curr_date_divorcedate_false(self):
        # Test case where divorce date are after the current date

        expected_output = 'No'

        indi = self.individuals[1]
        individuals_dict = {indi.identifier: indi}

        fam = self.families[1]
        fam.divorce_date = '2032-11-08'
        families_dict = {fam.identifier: fam}

        result = DatesBeforeCurrDate(individuals_dict, families_dict)
        self.assertEqual(result, expected_output)


class TestBirthBeforeDeath(unittest.TestCase):

    def setUp(self):
        self.individuals = [
            gedcom_data.Individual("@I1@", "Alice", "F", "1990-01-01", "2020-12-31"),
            gedcom_data.Individual("@I2@", "Bob", "M", "1985-06-15", "1980-05-20"),
            gedcom_data.Individual("@I3@", "Charlie", "M", "1999-03-10"),
            gedcom_data.Individual("@I4@", "Diana", "F", "2005-08-20"),
            gedcom_data.Individual("@I5@", "Eva", "F", "1992-11-05", "1995-02-10"),
            gedcom_data.Individual("@I6@", None, "M", "1980-01-01"),
            gedcom_data.Individual("@I7@", "Frank", "M", "1990-01-01", "1990-01-01"),
            gedcom_data.Individual("@I8@", "Grace", "F", "1985-06-15"),
            gedcom_data.Individual("@I9@", "Henry", "M", None, "1995-02-10")
        ]

    def test_birth_before_death_true(self):
        individual_data = self.individuals[0]
        self.assertIsNone(individual_data.is_birth_before_death())

    def test_birth_before_death_false(self):
        individual_data = self.individuals[1]
        self.assertEqual(individual_data.is_birth_before_death(),
                         "ERROR: INDIVIDUAL: US03: @I2@: Birthdate 1985-06-15 is the same as or after death date 1980-05-20")

    def test_birth_before_death_missing_dates(self):
        individual_data = self.individuals[2]
        self.assertIsNone(individual_data.is_birth_before_death())

    def test_birth_before_death_same_birth_and_death_date(self):
        individual_data = self.individuals[6]
        self.assertEqual(individual_data.is_birth_before_death(),
                         "ERROR: INDIVIDUAL: US03: @I7@: Birthdate 1990-01-01 is the same as or after death date 1990-01-01")

    def test_birth_before_death_no_death_date(self):
        individual_data = self.individuals[7]
        self.assertIsNone(individual_data.is_birth_before_death())

    def test_birth_before_death_no_birth_date(self):
        individual_data = self.individuals[8]
        self.assertIsNone(individual_data.is_birth_before_death())


class TestMissingRequiredFields(unittest.TestCase):

    def setUp(self):
        self.individuals = [
            gedcom_data.Individual("@I1@", "Alice", "F", "1990-01-01", "2020-12-31"),
            gedcom_data.Individual("@I2@", "Bob", "M", "1985-06-15", "1980-05-20"),
            gedcom_data.Individual("@I3@", "Charlie", "M", "1999-03-10"),
            gedcom_data.Individual("@I4@", "Diana", "F", "2005-08-20", child_of="@F1@"),
            gedcom_data.Individual("@I5@", "", "F", "1992-11-05", "1995-02-10", child_of="@F1@"),
            gedcom_data.Individual("@I6@", "Amy", "M", "", child_of="@F1@"),
            gedcom_data.Individual("@I10@", "Ivy", "F", "1998-05-15", child_of=""),
            gedcom_data.Individual("@I11@", "", "M", "1990-03-20", child_of="@F1@"),
            gedcom_data.Individual("@I12@", "James", "", "1975-08-12", child_of="@F1@"),
            gedcom_data.Individual("@I14@", "", "", "", child_of="")
        ]

    def test_find_missing_required_fields_all_fields_present(self):
        individual_data = self.individuals[3]
        self.assertIsNone(individual_data.find_missing_required_fields())

    def test_find_missing_required_fields_missing_name(self):
        individual_data = self.individuals[4]
        self.assertEqual(individual_data.find_missing_required_fields(),
                         "ERROR: INDIVIDUAL: US23: @I5@: Missing required fields Name")

    def test_find_missing_required_fields_missing_birth_date(self):
        individual_data = self.individuals[5]
        self.assertEqual(individual_data.find_missing_required_fields(),
                         "ERROR: INDIVIDUAL: US23: @I6@: Missing required fields Birth Date")

    def test_find_missing_required_fields_missing_child_of(self):
        individual_data = self.individuals[6]
        expected_error_message = "ERROR: INDIVIDUAL: US23: @I10@: Missing required fields Child Of (FAMC)"
        self.assertEqual(individual_data.find_missing_required_fields(), expected_error_message)

    def test_find_missing_required_fields_multiple_missing_fields(self):
        individual_data = self.individuals[9]
        expected_error_message = "ERROR: INDIVIDUAL: US23: @I14@: Missing required fields Name, Sex, Birth Date, Child Of (FAMC)"
        self.assertEqual(individual_data.find_missing_required_fields(), expected_error_message)

    def test_find_missing_required_fields_missing_sex(self):
        individual_data = self.individuals[8]
        self.assertEqual(individual_data.find_missing_required_fields(),
                         "ERROR: INDIVIDUAL: US23: @I12@: Missing required fields Sex")


class TestCheckDates(unittest.TestCase):

    def setUp(self):
        self.individuals = [
            gedcom_data.Individual("@I3@", "Jane", "F", "1778-07-21", "2018-02-12", "", "", 239, False, False),
            gedcom_data.Individual("@I1@", "Patrick", "M", "1996-08-23", "2019-04-10", "", "", 28, False, False),
            gedcom_data.Individual("@I2@", "Aadi", "M", "1778-01-01", None, "", "", 239, False, True),
            gedcom_data.Individual("@I5@", "Jack", "M", "1987-02-12", None, "", "", 37, False, True),
            gedcom_data.Individual("@I6@", "Erica", "F", "2017-01-19", None, "", "", 157, False, True)
        ]

    def test_check_age_at_death_above_150(self):
        expected_output = 'No'

        indi = self.individuals[0]

        individuals_dict = {indi.identifier: indi}
        result = check_death_and_age(individuals_dict)
        self.assertEqual(result, expected_output)

    def test_check_age_at_death_less_150(self):
        expected_output = 'Yes'

        indi = self.individuals[1]

        individuals_dict = {indi.identifier: indi}
        result = check_death_and_age(individuals_dict)
        self.assertEqual(result, expected_output)

    def test_check_age_from_birth_less_150(self):
        expected_output = 'Yes'

        indi = self.individuals[3]

        individuals_dict = {indi.identifier: indi}
        result = check_death_and_age(individuals_dict)
        self.assertEqual(result, expected_output)

    def test_check_age_from_birth_above_150(self):
        expected_output = 'No'

        indi = self.individuals[4]

        individuals_dict = {indi.identifier: indi}
        result = check_death_and_age(individuals_dict)
        self.assertEqual(result, expected_output)


class TestBirthDateAfterParentDeathDate(unittest.TestCase):

    def setUp(self):
        # Create individuals for the test cases
        self.individuals = [
            gedcom_data.Individual("@I1@", "Alice", "F", "2022-01-01"),
            gedcom_data.Individual("@I2@", "Bob", "M", "2001-06-15"),
            gedcom_data.Individual("@I3@", "Charlie", "M", "1960-03-10"),
            gedcom_data.Individual("@I4@", "Diana", "F", "2005-08-20"),
            gedcom_data.Individual("@I5@", "Eva", "F", "1992-11-05"),
            gedcom_data.Individual("@I6@", None, "M", "1997-01-01"),
            gedcom_data.Individual("@I7@", "Frank", "M", "1990-01-01"),
            gedcom_data.Individual("@I8@", "Grace", "F", "1985-06-15"),
            gedcom_data.Individual("@I9@", "Henry", "M", None)
        ]

    def test_birth_date_after_father_death_date(self):
        individual_data = self.individuals[1]
        father = self.individuals[5]
        father.death_date = "1995-01-01"
        individual_data.father = father
        self.assertIsNone(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data))

    def test_birth_date_equal_to_mother_death_date(self):
        individual_data = self.individuals[3]
        mother = self.individuals[2]
        mother.death_date = "2005-08-20"
        individual_data.mother = mother
        self.assertIsNone(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data))

    def test_birth_date_equal_to_father_death_date(self):
        individual_data = self.individuals[7]
        father = self.individuals[5]
        father.death_date = "1990-01-01"
        individual_data.father = father
        self.assertIsNone(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data))

    def test_birth_date_before_mother_and_father_death_date(self):
        individual_data = self.individuals[4]
        mother = self.individuals[2]
        mother.death_date = "2030-01-01"
        father = self.individuals[5]
        father.death_date = "2050-12-31"
        individual_data.mother = mother
        individual_data.father = father
        self.assertIsNone(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data))

    def test_birth_date_before_mother_death_date(self):
        individual_data = self.individuals[6]
        mother = self.individuals[2]
        mother.death_date = "2030-01-01"
        individual_data.mother = mother
        self.assertIsNone(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data))

    def test_birth_date_before_father_death_date(self):
        individual_data = self.individuals[8]
        father = self.individuals[5]
        father.death_date = "2050-12-31"
        individual_data.father = father
        self.assertIsNone(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data))

    def test_birth_date_after_mother_death_date(self):
        individual_data = self.individuals[0]
        mother = self.individuals[2]
        mother.death_date = "2021-01-01"
        individual_data.mother = mother
        self.assertEqual(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data),
                         f"ERROR: INDIVIDUAL: US09: @I1@: Birth date 2022-01-01 is after mother's death date 2021-01-01")

    def test_birth_date_after_both_parents_death_date(self):
        individual_data = self.individuals[0]
        mother = self.individuals[2]
        father = self.individuals[5]
        mother.death_date = "2020-01-01"
        father.death_date = "1995-01-01"
        individual_data.mother = mother
        individual_data.father = father
        self.assertEqual(gedcom_data.is_individual_birth_date_after_parent_death_date(individual_data),
                         f"ERROR: INDIVIDUAL: US09: @I1@: Birth date 2022-01-01 is after mother's death date 2020-01-01 and after father's death date 1995-01-01")


class TestFifteenOrMoreSiblings(unittest.TestCase):

    def setUp(self):
        self.individuals = {
            "@I1@": gedcom_data.Individual("@I1@", "Tyler", "M", "1999-08-31", None, "", "", 24, False, True),
            "@I2@": gedcom_data.Individual("@I2@", "John", "M", "2003-12-13", None, "", "", 20, False, True),
            "@I3@": gedcom_data.Individual("@I3@", "Jane", "F", "1997-08-23", "2018-02-12", "", "", 27, False, False),
            "@I4@": gedcom_data.Individual("@I4@", "Jill", "F", "1995-05-08", None, "", "", 29, False, True),
            "@I5@": gedcom_data.Individual("@I5@", "Jack", "M", "1987-02-12", None, "", "", 37, False, True),
            "@I6@": gedcom_data.Individual("@I6@", "Erica", "F", "2017-01-19", None, "", "", 7, False, True),
            "@I7@": gedcom_data.Individual("@I7@", "Jeffery", "M", "1997-11-17", None, "", "", 27, False, True),
            "@I8@": gedcom_data.Individual("@I8@", "Willow", "F", "1999-12-27", None, "", "", 24, False, True),
            "@I9@": gedcom_data.Individual("@I9@", "Gavin", "M", "1993-12-26", None, "", "", 31, False, True),
            "@I10@": gedcom_data.Individual("@I10@", "Hannah", "F", "1977-03-22", None, "", "", 47, False, False),
            "@I11@": gedcom_data.Individual("@I11@", "Jack", "M", "2010-02-13", None, "", "", 37, False, True),
        }

    def test_fifteen_or_more_siblings_true(self):
        individual_data = self.individuals["@I1@"]
        individual_data.child_of = "@F1@"
        for i in range(2, 17):
            sibling_id = f"@I{i}@"
            sibling = gedcom_data.Individual(sibling_id, f"Sib{i}", "M", "2000-01-01", None, "", "", 20, False, True)
            sibling.child_of = "@F1@"
            self.individuals[sibling_id] = sibling

        self.assertEqual(individual_data.fifteen_or_more_siblings(self.individuals),
                         "ERROR: INDIVIDUAL: US15: @I1@: The individual has 15 siblings or more.")

    def test_fifteen_or_more_siblings_false(self):
        individual_data = self.individuals["@I2@"]
        individual_data.child_of = "@F1@"
        for i in range(3, 17):
            sibling_id = f"@I{i}@"
            sibling = gedcom_data.Individual(sibling_id, f"Sib{i}", "M", "2000-01-01", None, "", "", 20, False, True)
            sibling.child_of = "@F1@"
            self.individuals[sibling_id] = sibling

        self.assertIsNone(individual_data.fifteen_or_more_siblings(self.individuals))

    def test_fifteen_or_more_siblings_no_child_of(self):
        individual_data = self.individuals["@I3@"]
        self.assertIsNone(individual_data.fifteen_or_more_siblings(self.individuals))

    def test_fifteen_or_more_siblings_zero_siblings(self):
        individual_data = self.individuals["@I6@"]
        individual_data.child_of = "@F3@"
        self.assertIsNone(individual_data.fifteen_or_more_siblings(self.individuals))


class TestDetectBigamy(unittest.TestCase):

    def setUp(self):
        # Set up sample data for testing
        self.marriage_info_no_marriage = []
        self.marriage_info_single_marriage = [
            {'marriage_date': '2000-01-01', 'divorce_date': None, 'spouse_death_date': None}]
        self.marriage_info_multiple_marriages_no_conflict = [
            {'marriage_date': '2000-01-01', 'divorce_date': '2010-01-01', 'spouse_death_date': None},
            {'marriage_date': '2015-01-01', 'divorce_date': None, 'spouse_death_date': None}
        ]
        self.marriage_info_bigamy_overlapping_dates = [
            {'marriage_date': '2000-01-01', 'divorce_date': None, 'spouse_death_date': None},
            {'marriage_date': '1999-01-01', 'divorce_date': None, 'spouse_death_date': None}
        ]
        self.marriage_info_bigamy_concurrent_marriage_divorce = [
            {'marriage_date': '2000-01-01', 'divorce_date': '2005-01-01', 'spouse_death_date': None},
            {'marriage_date': '2003-01-01', 'divorce_date': None, 'spouse_death_date': None}
        ]

    def test_detect_bigamy_no_marriages(self):
        # Test case where individual has no marriages
        individual = gedcom_data.Individual("@I1@", "John", "M", "1990-01-01")
        individual.marriage_info = self.marriage_info_no_marriage
        self.assertIsNone(individual.detect_bigamy())

    def test_detect_bigamy_single_marriage(self):
        # Test case where individual has only one marriage
        individual = gedcom_data.Individual("@I1@", "John", "M", "1990-01-01")
        individual.marriage_info = self.marriage_info_single_marriage
        self.assertIsNone(individual.detect_bigamy())

    def test_detect_bigamy_multiple_marriages_no_conflict(self):
        # Test case where individual has multiple marriages with no conflict
        individual = gedcom_data.Individual("@I1@", "John", "M", "1990-01-01")
        individual.marriage_info = self.marriage_info_multiple_marriages_no_conflict
        self.assertIsNone(individual.detect_bigamy())

    def test_detect_bigamy_bigamy_overlapping_dates(self):
        # Test case where individual has bigamy with overlapping marriage dates
        individual = gedcom_data.Individual("@I1@", "John", "M", "1990-01-01")
        individual.marriage_info = self.marriage_info_bigamy_overlapping_dates
        expected_error = "ERROR: INDIVIDUAL: US11: @I1@: Bigamy has been detected. John is married to multiple individuals at the same time."
        self.assertEqual(individual.detect_bigamy(), expected_error)

    def test_detect_bigamy_bigamy_concurrent_marriage_divorce(self):
        # Test case where individual has bigamy with concurrent marriage and divorce dates
        individual = gedcom_data.Individual("@I1@", "John", "M", "1990-01-01")
        individual.marriage_info = self.marriage_info_bigamy_concurrent_marriage_divorce
        expected_error = "ERROR: INDIVIDUAL: US11: @I1@: Bigamy has been detected. John is married to multiple individuals at the same time."
        self.assertEqual(individual.detect_bigamy(), expected_error)


class TestMarriageBefore14(unittest.TestCase):

    def setUp(self):
        self.husband = gedcom_data.Individual("@I1@", "John", "M", "2000-01-01")
        self.wife = gedcom_data.Individual("@I2@", "Jane", "F", "2002-02-02")
        self.family = gedcom_data.Family("@F1@", "@I1@", "John", "@I2@", "Jane", marriage_date="2016-05-20")

    def test_marriage_before_14_true(self):
        self.husband.age_at_date = lambda x: 13  # Mocking the age of husband to be less than 14
        self.wife.age_at_date = lambda x: 15  # Mocking the age of wife to be greater than 14
        individuals = {"@I1@": self.husband, "@I2@": self.wife}
        result = self.family.is_marriage_before_14(individuals)
        self.assertEqual(result,
                         "ERROR: FAMILY: US10: @F1@: Marriage occurred before one of the spouses reached 14 years of age.")

    def test_marriage_before_14_false(self):
        self.husband.age_at_date = lambda x: 16  # Mocking the age of husband to be greater than 14
        self.wife.age_at_date = lambda x: 15  # Mocking the age of wife to be greater than 14
        individuals = {"@I1@": self.husband, "@I2@": self.wife}
        result = self.family.is_marriage_before_14(individuals)
        self.assertIsNone(result)

    def test_marriage_before_14_no_marriage_date(self):
        self.family.marriage_date = None
        individuals = {"@I1@": self.husband, "@I2@": self.wife}
        result = self.family.is_marriage_before_14(individuals)
        self.assertIsNone(result)

    def test_marriage_before_14_missing_spouse(self):
        individuals = {"@I1@": self.husband}  # Missing wife in the individuals dictionary
        result = self.family.is_marriage_before_14(individuals)
        self.assertIsNone(result)


class TestMarriageandDivorceDates(unittest.TestCase):

    def setUp(self):
        self.families = [
            gedcom_data.Family("@F3@", "@I6@", "Erica", "@I7@", "Jeffery", [], "2016-11-12", "2015-11-12", []),
            gedcom_data.Family("@F4@", "@I8@", "Willow", "@I9@", "Gavin", [], None, "2010-11-12", []),
            gedcom_data.Family("@F5@", "@I10@", "Hannah", "@I5@", "Jack", [], "2010-11-12", "2015-11-12", []), ]

    def test_check_marriage_after_divorce(self):
        expected_output = 'No'

        fam = self.families[0]
        family_dict = {fam.identifier: fam}
        result = check_marriage_and_divorce_date(family_dict)
        self.assertEqual(result, expected_output)

    def test_check_no_marriagedate_but_divorcedate(self):
        expected_output = 'No'

        fam = self.families[1]
        family_dict = {fam.identifier: fam}
        result = check_marriage_and_divorce_date(family_dict)
        self.assertEqual(result, expected_output)

    def test_check_marriage_before_divorced(self):
        expected_output = 'Yes'

        fam = self.families[2]
        family_dict = {fam.identifier: fam}
        result = check_marriage_and_divorce_date(family_dict)
        self.assertEqual(result, expected_output)


class TestMarriageBeforeDeath(unittest.TestCase):

    def setUp(self):
        self.individuals = [
            gedcom_data.Individual("@I3@", "Jane", "F", "1778-07-21", "2018-02-12", "", "", 239, False, False),
            gedcom_data.Individual("@I7@", "Jessica", "F", "1996-08-23", "2019-04-10", "", "", 28, False, False),
            gedcom_data.Individual("@I8@", "Willow", "M", "2022-01-01", None, "", "", 239, False, False),
            gedcom_data.Individual("@I5@", "Jack", "M", "1987-02-12", None, "", "", 37, False, True),
            gedcom_data.Individual("@I6@", "Jeffrey", "M", "2017-01-19", "2010-05-01", "", "", 157, False, False)
        ]

        self.families = [
            gedcom_data.Family("@F3@", "@I6@", "Jeffrey", "@I7@", "Erica", [], "2016-11-12", "2015-11-12", []),
            gedcom_data.Family("@F4@", "@I8@", "Willow", "@I9@", "Gavin", [], None, "2010-11-12", []),
            gedcom_data.Family("@F5@", "@I10@", "Hannah", "@I7@", "Jessica", [], "2020-11-12", "2015-11-12", []), ]

    def test_check_marriage_before_husband_death(self):
        expected_output = 'No'

        indi = self.individuals[4]
        indi_dict = {indi.identifier: indi}

        fam = self.families[0]
        family_dict = {fam.identifier: fam}

        result = check_marriage_before_death(family_dict, indi_dict)
        self.assertEqual(result, expected_output)

    def test_check_marriage_before_wife_death(self):
        expected_output = 'No'

        indi = self.individuals[1]
        indi_dict = {indi.identifier: indi}

        fam = self.families[2]
        family_dict = {fam.identifier: fam}

        result = check_marriage_before_death(family_dict, indi_dict)
        self.assertEqual(result, expected_output)

    def test_check_marriage_after_wife_death(self):
        expected_output = 'Yes'

        indi = self.individuals[2]
        indi_dict = {indi.identifier: indi}

        fam = self.families[1]
        family_dict = {fam.identifier: fam}

        result = check_marriage_before_death(family_dict, indi_dict)
        self.assertEqual(result, expected_output)


class TestMarriedToDescendants(unittest.TestCase):

    def setUp(self):
        self.individual = gedcom_data.Individual("@I1@", "John Doe", "M", "1990-01-01")
        self.descendant = gedcom_data.Individual("@I2@", "Jane Doe", "F", "2010-01-01")
        self.descendant2 = gedcom_data.Individual("@I3@", "Jack Doe", "M", "2012-01-01")

        self.individual.descendants = [self.descendant, self.descendant2]
        self.individual.spouse_of = ["@F1@", "@F2@"]

        self.family1 = gedcom_data.Family("@F1@", "@I1@", "@I6@")
        self.family2 = gedcom_data.Family("@F2@", "@I1@", "@I7@")

        self.families = {
            "@F1@": self.family1,
            "@F2@": self.family2
        }

    def test_married_to_descendants_no_descendants(self):
        self.individual.descendants = []
        self.assertIsNone(self.individual.married_to_descendants(self.families))

    def test_married_to_descendants_descendant_married(self):
        self.family1.husband_id = "@I1@"
        self.family1.wife_id = "@I2@"
        self.assertEqual(self.individual.married_to_descendants(self.families),
                         "ERROR: INDIVIDUAL: US17: @I1@: John Doe is married to descendant Jane Doe in family @F1@")

    def test_married_to_descendants_multiple_descendants(self):
        self.family1.husband_id = "@I1@"
        self.family1.wife_id = "@I2@"
        self.assertEqual(self.individual.married_to_descendants(self.families),
                         "ERROR: INDIVIDUAL: US17: @I1@: John Doe is married to descendant Jane Doe in family @F1@")

    def test_married_to_descendants_no_families(self):
        self.assertIsNone(self.individual.married_to_descendants({}))


class TestAliveAndMarried(unittest.TestCase):

    def setUp(self):
        self.individuals = [
            gedcom_data.Individual("@I1@", "John Doe", "M", "1990-01-01", alive=True, marriage_info=[
                {"family_id": "@F1@", "marriage_date": "2010-05-20", "divorce_date": None, "spouse_id": "@I2@",
                 "spouse_death_date": None}
            ]),
            gedcom_data.Individual("@I2@", "Jane Doe", "F", "1992-03-15", alive=False, marriage_info=[
                {"family_id": "@F2@", "marriage_date": "2015-12-10", "divorce_date": None, "spouse_id": "@I3@",
                 "spouse_death_date": None}
            ]),
            gedcom_data.Individual("@I3@", "Alice Smith", "F", "1985-07-20", alive=True, marriage_info=[
                {"family_id": "@F2@", "marriage_date": "2015-12-10", "divorce_date": "2018-12-10", "spouse_id": "@I1@",
                 "spouse_death_date": None}
            ]),
            gedcom_data.Individual("@I4@", "Bob Johnson", "M", "1978-11-10", alive=False, marriage_info=[
                {"family_id": "@F2@", "marriage_date": "2015-12-10", "divorce_date": None, "spouse_id": "@I1@",
                 "spouse_death_date": "2018-12-10"}]),
            gedcom_data.Individual("@I4@", "Bob Johnson", "M", "1978-11-10", alive=False, marriage_info=[])
        ]

    def test_alive_and_married_alive_married(self):
        result = self.individuals[0].alive_and_married()
        self.assertEqual(result, "ERROR: INDIVIDUAL: US30: @I1@: John Doe is alive and married.")

    def test_alive_and_married_not_alive(self):
        result = self.individuals[1].alive_and_married()
        self.assertIsNone(result)

    def test_alive_and_married_alive_single_divorced(self):
        result = self.individuals[2].alive_and_married()
        self.assertIsNone(result)

    def test_alive_and_married_dead_single_never_married(self):
        result = self.individuals[4].alive_and_married()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()