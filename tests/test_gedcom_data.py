import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

import gedcom_data
from gedcom_data import DatesBeforeCurrDate
import unittest


def initData():
    individuals = [gedcom_data.Individual("@I1@", "Tyler", "M","1999-08-31", None, "","", 24, False,True),
                    gedcom_data.Individual("@I2@", "John", "M","2003-12-13", None, "","", 20, False,True),
                    gedcom_data.Individual("@I3@", "Jane", "F","1997-08-23", "2018-02-12", "","", 27, False,False),
                    gedcom_data.Individual("@I4@", "Jill", "F","1995-05-08", None, "","", 29, False,True),
                    gedcom_data.Individual("@I5@", "Jack", "M","1987-02-12", None, "","", 37, False,True),
                    gedcom_data.Individual("@I6@", "Erica", "F","2017-01-19", None, "","", 7, False,True),
                    gedcom_data.Individual("@I7@", "Jeffery", "M","1997-11-17", None, "","", 27, False,True),
                    gedcom_data.Individual("@I8@", "Willow", "F","1999-12-27", None, "","", 24, False,True),
                    gedcom_data.Individual("@I9@", "Gavin", "M","1993-012-26", None, "","", 31, False,True),
                    gedcom_data.Individual("@I10@", "Hannah", "F","1977-03-22", None, "","", 47, False,False),
                    gedcom_data.Individual("@I11@", "Jack", "M","2010-02-13", None, "","", 37, False,True),
                    ]
    
    families = [gedcom_data.Family("@F1@", "@I2@", "John", "@I3@","Jane", [individuals[1], individuals[2]],"2018-11-12", None, ["@I2@", "@I3@"]),
                gedcom_data.Family("@F2@", "@I4@", "Jill", "@I5@","Jack", [individuals[5]],"2016-12-25", None, ["@I6@"]),
                gedcom_data.Family("@F3@", "@I6@", "Erica", "@I7@","Jeffery", [],"1999-11-12", "2015-11-12", []),
                gedcom_data.Family("@F4@", "@I8@", "Willow", "@I9@","Gavin", [],"2010-11-12", None, []),
                gedcom_data.Family("@F5@", "@I10@", "Hannah", "@I5@","Jack", [],"2010-11-12", "1980-11-12", []),]


    return families, individuals

class TestGedcomFamilyUniqueFamilyNames(unittest.TestCase):

    def setUp(self) : 
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

    def setUp(self) : 
        self.families, self.individuals = initData()
    
    def test_birth_before_marriage_true(self):
        family_data = self.families[0]
        print(family_data)
        self.assertTrue(family_data.children_before_marriage() !=  "")

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

    def setUp(self) : 
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
        fam.marriage_date='2030-10-12'
        families_dict = {fam.identifier: fam}

        result = DatesBeforeCurrDate(individuals_dict, families_dict)
        self.assertEqual(result, expected_output)

    def test_dates_before_curr_date_divorcedate_false(self):
    # Test case where divorce date are after the current date

        expected_output = 'No'

        indi = self.individuals[1]
        individuals_dict = {indi.identifier: indi}

        fam = self.families[1]
        fam.divorce_date='2032-11-08'
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


if __name__ == '__main__':
    unittest.main()