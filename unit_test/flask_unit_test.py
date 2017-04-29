import os
import sys
import unittest
import tempfile
import getpass
sys.path.append("../")
import back_end
import ast


class FlaskrTestCase(unittest.TestCase):

    ClassIsSetup = False

    def setUp(self):
        print ' '
        if not self.ClassIsSetup:
            print '[Unit Test]: initializing required resources...'
            self.__class__.ClassIsSetup = True
            self.db_fd, back_end.app.config['DATABASE'] = tempfile.mkstemp()
            back_end.app.config['TESTING'] = True
            self.__class__.app = back_end.app.test_client()
            self.username = raw_input("Bamboo username: ")
            self.password = getpass.getpass("Bamboo password: ")
            back_end.server_init(self.username, self.password)

    def test_date_page(self):
        # the list should at least contain the following date
        print "[Unit Test]: test_date_page"

        sample = ["2014-07-27", "2014-07-26", "2014-07-25", "2014-07-21",
                  "2014-07-20", "2014-07-19", "2014-07-18", "2014-07-17",
                  "2014-07-16", "2014-07-15", "2014-07-14", "2014-07-13",
                  "2014-07-12", "2014-07-11", "2014-07-10", "2014-07-09",
                  "2014-07-08", "2014-07-07", "2014-07-06", "2014-07-05",
                  ]

        rv = self.__class__.app.get('/date')
        result = ast.literal_eval(rv.data)["date"]

        for date in sample:
            assert date in result

    def test_homepage(self):
        # should get 200 for response code
        print "[Unit Test]: test_homepage"

        rv = self.__class__.app.get('/date')
        result = rv.status_code
        assert result == 200

    def test_home_date_page(self):
        # should get the corresponding test suites for the given date
        print "[Unit Test]: test_home_date_page"

        sample = [{"end_date": "2014-07-27", "end_time": "03:23",
                   "name": "Device Cloud Daily - Test-Dev",
                   "plan_key": "SA-DCDT-308",
                   "start_date": "2014-07-27",
                   "start_time": "03:00",
                   "test_failed": 27,
                   "test_passed": 276,
                   "test_quarantined": 10,
                   "total_test": 313},
                  {"end_date": "2014-07-27", "end_time": "04:34",
                   "name": "Device Cloud Daily - Test-My",
                   "plan_key": "SA-DCTM-415",
                   "start_date": "2014-07-27",
                   "start_time": "04:00",
                   "test_failed": 3,
                   "test_passed": 305,
                   "test_quarantined": 11,
                   "total_test": 319}
                  ]

        rv = self.__class__.app.get('/home/date/2014-07-27')
        results = ast.literal_eval(rv.data)["result"]
        assert sample == results

    def test_test_suite_page(self):
        # should contain the following test information
        print "[Unit Test]: test_test_suite_page"

        sample = [{"className": "TestDataPointTZ", "failed": 0,
                   "quarantined": 0, "successful": 1, "total": 1},
                  {"className": "TestPushReplay", "failed": 0,
                   "quarantined": 0, "successful": 1, "total": 1},
                  {"className": "TestEPDeviceVendor", "failed": 0,
                   "quarantined": 0, "successful": 1, "total": 1},
                  {"className": "TestTriggerAlarm", "failed": 0,
                   "quarantined": 0, "successful": 2, "total": 2},
                  ]

        rv = self.__class__.app.get('/testsuite/SA-DCTM-415')
        results = ast.literal_eval(rv.data)["result"]

        for tests in sample:
            assert tests in results

    def test_related_history_test_case_page(self):
        # the page should contain the following history, related history
        # and test cases
        print "[Unit Test]: test_related_history_test_case_page"

        sample_related_history = [{"date": "2014-08-08", "failed": 0,
                                   "plan_key": "SA-DCTM-428",
                                   "quarantined": 1, "successful": 8,
                                   "time": "04:00", "total": 9},
                                  ]

        rv = self.__class__.app.get(
            '/test/SA-DCDT-320/TestDataStream')

        results_history_related = ast.literal_eval(rv.data)["history_others"]

        for history in sample_related_history:
            assert history in results_history_related

    def test_case_test_case_page(self):
        # the page should contain the following test cases
        print "[Unit Test]: test_case_test_case_page"

        sample_case = [
            {"className": "TestAutoProvisionDisabled",
             "date": "2014-08-05",
             "methodName": "test_add_device_from_autoprovision_account",
             "plan_key": "SA-DCDT-317",
             "quarantined": "False",
             "status": "successful",
             "time": "08:26"},
            {"className": "TestAutoProvisionDisabled",
             "date": "2014-08-05",
             "methodName": "test_connected_device_not_provisioned",
             "plan_key": "SA-DCDT-317",
             "quarantined": "False",
             "status": "successful",
             "time": "08:26"},
            ]

        rv = self.__class__.app.get(
            '/test/SA-DCDT-317/TestAutoProvisionDisabled')

        results_cases = ast.literal_eval(rv.data)["result"]

        for cases in sample_case:
            assert cases in results_cases

    def test_self_history_test_case_page(self):
        # the page should contain the following history data
        print "[Unit Test]: test_self_history_test_case_page"

        sample_self_history = [{"date": "2014-08-05", "failed": 0,
                                "plan_key": "SA-DCDT-316", "quarantined": 0,
                                "successful": 2, "time": "08:04", "total": 2},
                               {"date": "2014-08-04", "failed": 0,
                                "plan_key": "SA-DCDT-315", "quarantined": 0,
                                "successful": 2, "time": "01:28", "total": 2},
                               {"date": "2014-08-02", "failed": 0,
                                "plan_key": "SA-DCDT-314", "quarantined": 0,
                                "successful": 2, "time": "03:00", "total": 2},
                               ]

        rv = self.__class__.app.get(
            '/test/SA-DCDT-317/TestAutoProvisionDisabled')

        results_history_self = ast.literal_eval(rv.data)["history_self"]

        for history in sample_self_history:
            assert history in results_history_self

if __name__ == '__main__':
    unittest.main()
