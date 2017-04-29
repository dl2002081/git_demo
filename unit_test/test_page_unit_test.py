import unittest
import sys
import getpass
sys.path.append("../")
from home_page_material import Homepage
from test_page import Test_page


class TestSequenceFunctions(unittest.TestCase):

    ClassIsSetup = False

    def setUp(self):
        print ' '
        if not self.ClassIsSetup:
            print '[Unit Test]: initializing required resources...'
            self.__class__.ClassIsSetup = True
            self.username = raw_input("Bamboo username: ")
            self.password = getpass.getpass("Bamboo password: ")
            self.__class__.homepage = Homepage(self.username, self.password)
            self.__class__.test = Test_page(self.username, self.password,
                                            self.__class__.homepage)
            self.test_results = []

    def test_false_check_if_need_update(self):
        # should return false if existing key/count combination is in the list
        print "[Unit Test]: test_false_check_if_need_update"

        sample = {"key": "SA-DCDT-315", "total": 313}

        result = self.__class__.test.check_if_need_update(sample["key"],
                                                          sample["total"])

        self.assertFalse(result)

    def test_true_check_if_need_update(self):
        # should return true if existing key/count combination
        # is not in the list
        print "[Unit Test]: test_true_check_if_need_update"

        sample = {"key": "SA-9999", "total": 313}

        result = self.__class__.test.check_if_need_update(sample["key"],
                                                          sample["total"])

        self.assertTrue(result)

    def test_ignore_check_if_need_update(self):
        # should return false if existing key/count combination
        # is in ignore list
        print "[Unit Test]: test_ignore_check_if_need_update"

        sample = {"key": "SA-LINUXSA-10", "total": 313}

        result = self.__class__.test.check_if_need_update(sample["key"],
                                                          sample["total"])
        self.assertFalse(result)

    def test_ignore_check_if_need_update(self):
        # should return true if existing key/count combination is invalid
        print "[Unit Test]: test_ignore_check_if_need_update"

        sample = {"key": "SA-DCDT-315", "total": 222}

        result = self.__class__.test.check_if_need_update(sample["key"],
                                                          sample["total"])

        self.assertTrue(result)

    def test_valid_get_cases_from_testsuite(self):
        # should contain the sample list's use cases
        print "[Unit Test]: test_valid_get_cases_from_testsuite"

        sample = {"key": "SA-DCDT-315", "Test": "TestAutpProvisionDisabled",
                  "Case": ["test_add_device_from_autoprovision_account",
                           "test_connected_device_not_provisioned"]
                  }

        result = self.__class__.test.get_cases_from_testsuite(sample["key"],
                                                              sample["Test"])

        sample_case = sample["Case"].sort()
        result.sort()
        for cases in result:
            for test_case in sample_case[:]:
                if test_case == cases["methodName"]:
                    sample_case.remove(test_case)  # remove element if found
        self.assertEqual(None, sample_case)  # the list should be empty now

    def test_consistency_get_cases_from_testsuite(self):
        # should contain and match the sample list's use cases
        print "[Unit Test]: test_consistency_get_cases_from_testsuite"

        sample = {"key": "SA-DCDT-315", "Test": "TestAutpProvisionDisabled",
                  "Case": [
                      {"Name": "test_add_device_from_autoprovision_account",
                       "Status": "successful"},
                      {"Name": "test_connected_device_not_provisioned",
                       "Status": "successful"}
                      ]
                  }

        result = self.__class__.test.get_cases_from_testsuite(sample["key"],
                                                              sample["Test"])

        sample_case = sample["Case"].sort()
        for cases in result:
            for test_case in sample_case:
                if test_case["Name"] == cases["methodName"]:
                    self.assertEqual(test_case["Status"], cases["status"])

    def test_consistency_self_get_test_history(self):
        # the content of the cases in a test should match
        print "[Unit Test]: test_consistency_self_get_test_history"

        test_key = "SA-DCDT-315"
        sample = [{"key": "SA-DCDT-315", "Test": "TestRollup",
                   "Total": 6, "Passed": 0, "Failed": 6, "Quarantined": 0},
                  {"key": "SA-DCDT-314", "Test": "TestRollup",
                   "Total": 6, "Passed": 0, "Failed": 6, "Quarantined": 0},
                  {"key": "SA-DCDT-313", "Test": "TestRollup",
                   "Total": 6, "Passed": 0, "Failed": 6, "Quarantined": 0},
                  {"key": "SA-DCDT-312", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCDT-297", "Test": "TestRollup",
                   "Total": 6, "Passed": 2, "Failed": 4, "Quarantined": 0},
                  {"key": "SA-DCDT-296", "Test": "TestRollup",
                   "Total": 6, "Passed": 3, "Failed": 3, "Quarantined": 0},
                  ]

        result = self.__class__.test.get_test_history(test_key,
                                                      sample[0]["Test"],
                                                      "self")

        for history in result:
            for tests in sample:
                if history["plan_key"] == tests["key"]:
                    self.assertEqual(tests["Total"], history["total"])
                    self.assertEqual(tests["Passed"], history["successful"])
                    self.assertEqual(tests["Failed"], history["failed"])

                    self.assertEqual(tests["Quarantined"],
                                     history["quarantined"])

    def test_consistency_related_get_test_history(self):
        # the content of the cases in a test should match
        print "[Unit Test]: test_consistency_related_get_test_history"

        test_key = "SA-DCDT-315"
        sample = [{"key": "SA-DCTM-419", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCTM-418", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCTM-417", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCTM-416", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCTM-415", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCTM-414", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  {"key": "SA-DCTM-413", "Test": "TestRollup",
                   "Total": 6, "Passed": 6, "Failed": 0, "Quarantined": 0},
                  ]

        result = self.__class__.test.get_test_history(test_key,
                                                      sample[0]["Test"],
                                                      "related")

        for history in result:
            for tests in sample:
                if history["plan_key"] == tests["key"]:
                    self.assertEqual(tests["Total"], history["total"])
                    self.assertEqual(tests["Passed"], history["successful"])
                    self.assertEqual(tests["Failed"], history["failed"])

                    self.assertEqual(tests["Quarantined"],
                                     history["quarantined"])

if __name__ == '__main__':
    unittest.main()
