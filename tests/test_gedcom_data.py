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

        
if __name__ == '__main__':
    unittest.main()