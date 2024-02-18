import unittest
import gedcom_data 


def initData():
    individuals = [gedcom_data.Individual("@I1@", "Tyler", "M","1999-08-31", None, "","", 24, True),
                    gedcom_data.Individual("@I2@", "John", "M","2003-12-13", None, "","", 20, True),
                    gedcom_data.Individual("@I3@", "Jane", "F","1997-08-23", None, "","", 27, True),
                    gedcom_data.Individual("@I4@", "Jill", "F","1995-05-08", None, "","", 29, True),
                    gedcom_data.Individual("@I5@", "Jack", "M","1987-02-12", None, "","", 37, True),
                    gedcom_data.Individual("@I6@", "Erica", "F","2017-01-19", None, "","", 7, True),
                    gedcom_data.Individual("@I7@", "Jeffery", "M","1997-11-17", None, "","", 27, True),
                    gedcom_data.Individual("@I8@", "Willow", "F","1999-12-27", None, "","", 24, True),
                    gedcom_data.Individual("@I9@", "Gavin", "M","1993-012-26", None, "","", 31, True),
                    gedcom_data.Individual("@I10@", "Hannah", "F","1977-03-22", None, "","", 47, False),
                    gedcom_data.Individual("@I11@", "Jack", "M","1992-02-13", None, "","", 37, True),
                    ]
    
    families = [gedcom_data.Family("@F1@", "@I2@", "John", "@I3@","Jane", [individuals[1], individuals[2]],"2018-11-12", None, ["@I2@", "@I3@"]),
                gedcom_data.Family("@F2@", "@I4@", "Jill", "@I5@","Jack", [individuals[5]],"2016-12-25", None, ["@I6@"]),
                gedcom_data.Family("@F3@", "@I6@", "Erica", "@I7@","Jeffery", [],"1999-11-12", "2015-11-12", []),
                gedcom_data.Family("@F4@", "@I8@", "Willow", "@I9@","Gavin", [],"2010-11-12", None, []),
                gedcom_data.Family("@F5@", "@I10@", "Hannah", "@I5@","Jack", [],"1975-11-12", "1980-11-12", []),]


    return families, individuals

class TestGedcomFamilyUniqueFamilyNames(unittest.TestCase):

    def setUp(self) : 
        self.families, self.individuals = initData()
    
    def test_unique_family_names_true(self):
        family_data = self.families[0]
        print(family_data)
        self.assertEqual(family_data.unique_family_names(), "NO")

    def test_unique_family_names_false(self):

        family_data = self.families[1]
        self.assertEqual(family_data.unique_family_names(), "YES")

    def test_unique_family_names_no_children(self):
        family_data = self.families[2]
        self.assertEqual(family_data.unique_family_names(), "YES")

class TestGedcomBirthBeforeMarriage(unittest.TestCase):

    def setUp(self) : 
        self.families, self.individuals = initData()
    
    def test_birth_before_marriage_true(self):
        family_data = self.families[0]
        print(family_data)
        self.assertEqual(family_data.children_before_marriage(), "YES")

    def test_birth_before_marriage_false(self):

        family_data = self.families[1]
        self.assertEqual(family_data.children_before_marriage(), "NO")

    def test_birth_before_marriage_no_children(self):
        family_data = self.families[2]
        self.assertEqual(family_data.children_before_marriage(), "NO")


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


if __name__ == '__main__':
    unittest.main()