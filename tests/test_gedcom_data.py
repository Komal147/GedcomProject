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


if __name__ == '__main__':
    unittest.main()