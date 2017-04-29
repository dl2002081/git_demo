import unittest
import sys
import getpass
sys.path.append("../")
import home_page_material


class TestSequenceFunctions(unittest.TestCase):

    ClassIsSetup = False

    def setUp(self):
        print ' '
        if not self.ClassIsSetup:
            print '[Unit Test]: initializing required resources...'
            self.__class__.ClassIsSetup = True
            self.username = raw_input("Bamboo username: ")
            self.password = getpass.getpass("Bamboo password: ")

            self.__class__.homepage = home_page_material.Homepage(
                self.username,
                self.password)

            self.__class__.homepage.update_suite_data()

    def test_consistency_of_test_suite_list(self):
        # tests if the received test suites are equal to the list getting from
        # bamboo
        # All of the test_suite builds are expected from the result
        print '[Unit Test]: test_consistency_of_test_suite_list'

        list_to_be_tested = self.__class__.homepage.get_test_suite_list()

        sample_list = [
            "SA-DCDT", "SA-DCTM", "SA-LINUXSA", "SA-XMLTEST",
            "SA-T03",
            ]

        self.assertEqual(list_to_be_tested.sort(), sample_list.sort())

    def test_consistency_of_date_list(self):
        # check if all the test suites's date is included in the result
        print '[Unit Test]: test_consistency_of_date_list'

        list_to_be_tested = self.__class__.homepage.get_all_dates()

        sample_list = [
            '2014-07-31', '2014-07-30', '2014-07-29', '2014-07-28',
            '2014-07-27', '2014-07-26', '2014-07-25', '2014-07-21',
            '2014-07-20', '2014-07-19', '2014-07-18', '2014-07-17',
            '2014-06-30', '2014-06-29', '2014-06-28', '2014-06-27',
            '2014-06-26', '2014-06-25', '2014-06-24', '2014-06-23',
            '2014-06-22', '2014-06-05', '2014-05-09', '2014-05-08',
            '2014-04-30', '2014-02-10', '2014-02-09', '2014-02-08',
            '2014-02-07', '2014-02-06', '2014-02-05', '2014-02-04',
            '2014-02-03',
            ]

        # check the list includes all the dates in sample
        for i in sample_list:
            self.assertTrue(i in list_to_be_tested)

    def test_invalid_date_list(self):
        # it should not return date that has no tests
        print '[Unit Test]: test_invalid_date_list'

        list_to_be_tested = self.__class__.homepage.get_all_dates()

        sample_list = [
            '2014-07-24', '2014-07-23', '2014-07-22', '2014-06-18',
            '2014-06-21', '2014-06-20', '2014-06-19', '2014-06-17',
            ]

        # check the list includes all the dates in sample
        for i in sample_list:
            self.assertFalse(i in list_to_be_tested)

    def test_consistency_of_date_specified_test_suite_list(self):
        # check if the date specified suite request only return the suite
        # at that date
        print '[Unit Test]: test_consistency_of_date_specified_test_suite_list'

        sample_list = [
            '2014-07-31', '2014-07-30', '2014-07-29', '2014-07-28',
            '2014-07-27', '2014-07-26', '2014-07-25', '2014-07-21',
            '2014-07-20', '2014-07-19', '2014-07-18', '2014-07-17',
            '2014-06-26', '2014-06-25', '2014-06-24', '2014-06-23',
            '2014-06-22', '2014-06-05', '2014-05-09', '2014-05-08',
            '2014-04-30', '2014-02-10', '2014-02-09', '2014-02-08',
            '2014-02-07', '2014-02-06', '2014-02-05', '2014-02-04',
            '2014-02-03',
            ]

        for date in sample_list:
            # amount of result should match amount of specific date

            test_list = self.__class__.homepage.display_suites_for_given_date(
                date)

            for suite in test_list:
                self.assertEqual(suite["start_date"], date)

    def test_invalid_date_specified_test_suite_list(self):
        # it should return None for date with no tests
        print '[Unit Test]: test_invalid_date_specified_test_suite_list'

        sample_list = [
            '2014-07-24', '2014-07-23', '2014-07-22', '2014-06-18',
            '2014-06-21', '2014-06-20', '2014-06-19', '2014-06-17',
            ]

        for date in sample_list:
            # amount of result should match amount of specific date

            test_list = self.__class__.homepage.display_suites_for_given_date(
                date)

            self.assertEqual(0, len(test_list))

    def test_true_check_if_need_update(self):
        # should return true indicating update is required
        # when the key in current is not newest
        # and when current list is empty
        print '[Unit Test]: test_true_check_if_need_update'

        sample_current_build = [{"plan_key": "SA-DCTM-291"},
                                {"plan_key": "SA-DCTM-290"},
                                {"plan_key": "SA-DCTM-289"}]

        sample_latest_build = "SA-DCTM-292"

        result = self.__class__.homepage.check_if_need_update(
            "SA-DCTM",
            sample_current_build,
            sample_latest_build)

        self.assertTrue(result)
        sample_current_build = []

        result = self.__class__.homepage.check_if_need_update(
            "SA-DCTM",
            sample_current_build,
            sample_latest_build)

        self.assertTrue(result)

    def test_false_check_if_need_update(self):
        # should return true indicating update is required
        # when the key in current is newest
        print '[Unit Test]: test_false_check_if_need_update'

        sample_current_build = [{"plan_key": "SA-DCTM-291"},
                                {"plan_key": "SA-DCTM-290"},
                                {"plan_key": "SA-DCTM-289"}]

        sample_latest_build = "SA-DCTM-291"

        result = self.__class__.homepage.check_if_need_update(
            "SA-DCTM",
            sample_current_build,
            sample_latest_build)

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
