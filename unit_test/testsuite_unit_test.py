import unittest
import sys
import getpass
sys.path.append("../")
import test_suite_page


class TestSequenceFunctions(unittest.TestCase):

    ClassIsSetup = False

    def setUp(self):
        print ' '
        if not self.ClassIsSetup:
            print '[Unit Test]: initializing required resources...'
            self.__class__.ClassIsSetup = True
            self.username = raw_input("Bamboo username: ")
            self.password = getpass.getpass("Bamboo password: ")

            self.__class__.testsuite = test_suite_page.Test_suite_page(
                self.username,
                self.password)

    def test_consistency_of_successful_test(self):
        # Should return success for all the cases included in the following
        # tests contained in the test suites
        print "[Unit Test]: test_consistency_of_successful_test"

        key = ["SA-DCDT-313", "SA-DCDT-312", "SA-DCDT-311", "SA-DCTM-419"]
        sample_test = ["TestDeviceCoreGet", "TestDeviceCoreGroup"]

        for build in key:
            list_to_be_tested = self.__class__.testsuite.request_tests(build)
            for test in list_to_be_tested:
                if test["className"] in sample_test:
                    self.assertEqual("successful", test["status"])

    def test_consistency_of_failed_test(self):
        # Should return fail status for the following tests
        print "[Unit Test]: test_consistency_of_failed_test"

        sample_test = [
            {"key": "SA-DCDT-313", "test": "TestRollup",
             "case": "test_rollup_max"},
            {"key": "SA-DCDT-313", "test": "TestRollup",
             "case": "test_rollup_count"},
            {"key": "SA-DCDT-313", "test": "TestRollup",
             "case": "test_rollup_sum"},
            {"key": "SA-DCDT-313", "test": "TestSimulatedSMUDP",
             "case": "test_asynchronous_ping"},
            {"key": "SA-DCTM-416", "test": "TestDCADMessaging",
             "case": "upload_files"},
            {"key": "SA-DCTM-416", "test": "TestDCADMessaging",
             "case": "upload_files_with_contents"},
            ]

        count = 0

        for test in sample_test:

            list_to_be_tested = self.__class__.testsuite.request_tests(
                test["key"])

            for test_case in list_to_be_tested:
                if test_case["className"] == test["test"]:
                    if test_case["methodName"] == test["case"]:
                        self.assertEqual(test_case["status"], "failed")
                        count += 1
        self.assertEqual(count, len(sample_test))

    def test_consistency_of_quarantined_test(self):
        # Should return quarantined status for the following tests
        print "[Unit Test]: test_consistency_of_quarantined_test"

        sample_test = [
            {"key": "SA-DCTM-419", "test": "TestAutoProvisionEnabled",
             "case": "provisioned_device_connected"},
            {"key": "SA-DCTM-419", "test": "TestCarrierAuth",
             "case": "negative_carrier_auth_put_with_bad_id"},
            {"key": "SA-DCDT-312", "test": "TestAutoProvisionEnabled",
             "case": "provisioned_device_connected"},
            {"key": "SA-DCDT-302", "test": "TestDeviceCorePush",
             "case": "group_scoping"},
            {"key": "SA-DCDT-302", "test": "TestDeviceCorePush",
             "case": "operation_scoping"},
            {"key": "SA-T03-4", "test": "DeviceCorePush",
             "case": "operation_scoping"},
            ]

        count = 0

        for test in sample_test:

            list_to_be_tested = self.__class__.testsuite.request_tests(
                test["key"])

            for test_case in list_to_be_tested:
                if test_case["className"] == test["test"]:
                    if test_case["methodName"] == test["case"]:
                        self.assertEqual(test_case["quarantined"], "True")
                        count += 1
        self.assertEqual(count, len(sample_test))

    def test_functionality_of_rephrase_key(self):
        # Should transfer plan key to keys that can be used to get test cases
        # ie: SA-DCTM-419 to SA-DCTM-JOB1-419
        print "[Unit Test]: test_functionality_of_rephrase_key"

        sample_key = ["SA-DCTM-419", "SA-DCDT-302"]

        for key in sample_key:
            to_be_tested = self.__class__.testsuite.rephrase_key(key, "JOB1")
            self.assertTrue("JOB1" == to_be_tested.split('-')[2])

        for key in sample_key:
            to_be_tested = self.__class__.testsuite.rephrase_key(key,
                                                                 "HILBERT")
            self.assertTrue("HILBERT" == to_be_tested.split('-')[2])

    def test_consistency_of_get_test_status(self):
        # the amount of each test in terms of pass fail quarantined and titak
        # should match with the sample
        print "[Unit Test]: test_consistency_of_get_test_status"

        sample_test = [
            {"key": "SA-T03-4", "test": "DeviceCorePush",
             "total": 3, "passed": 1, "failed": 0, "Quarantined": 2},
            {"key": "SA-DCDT-280", "test": "TestGeoAssetParameters",
             "total": 8, "passed": 8, "failed": 0, "Quarantined": 0},
            {"key": "SA-DCTM-386", "test": "TestDeviceCorePush",
             "total": 3, "passed": 0, "failed": 1, "Quarantined": 2},
            {"key": "SA-DCTM-386", "test": "TestDataStream",
             "total": 9, "passed": 8, "failed": 0, "Quarantined": 1},
            {"key": "SA-XMLTEST-81", "test": "TransformDeviceTest",
             "total": 1, "passed": 0, "failed": 1, "Quarantined": 0},
            ]

        for test in sample_test:

            to_be_tested = self.__class__.testsuite.get_test_status(
                test["key"])

            for testcase in to_be_tested:
                if testcase["className"] == test["test"]:
                    self.assertEqual(testcase["total"], test["total"])
                    self.assertEqual(testcase["successful"], test["passed"])
                    self.assertEqual(testcase["failed"], test["failed"])
                    self.assertEqual(testcase["quarantined"],
                                     test["Quarantined"])

    def test_amount_of_get_test_status(self):
        # the amount of each test in terms of pass fail quarantined and titak
        # should match with the sample
        print "[Unit Test]: test_amount_of_get_test_status"

        sample_test = [
            {"key": "SA-DCDT-293", "total": 313, "passed": 306, "failed": 0,
             "Quarantined": 7},
            {"key": "SA-DCTM-399", "total": 319, "passed": 308, "failed": 3,
             "Quarantined": 8},
            {"key": "SA-XMLTEST-81", "total": 1, "passed": 0, "failed": 1,
             "Quarantined": 0},
            {"key": "SA-DCDT-308", "total": 313, "passed": 276, "failed": 27,
             "Quarantined": 10},
            {"key": "SA-DCTM-401", "total": 319, "passed": 311, "failed": 0,
             "Quarantined": 8},
            ]
        for test in sample_test:

            to_be_tested = self.__class__.testsuite.get_test_status(
                test["key"])

            total = 0
            passed = 0
            failed = 0
            quarantined = 0
            for testcase in to_be_tested:
                total += testcase["total"]
                passed += testcase["successful"]
                failed += testcase["failed"]
                quarantined += testcase["quarantined"]
            self.assertEqual(total, test["total"])
            self.assertEqual(passed, test["passed"])
            self.assertEqual(failed, test["failed"])
            self.assertEqual(quarantined, test["Quarantined"])

if __name__ == '__main__':
    unittest.main()
