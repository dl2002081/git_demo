from bamboo_request import request_specific_test
from json import dumps
import csv
from home_page_material import Homepage
from test_suite_page import Test_suite_page
import os


class Test_page(object):

    ignore_list = ['SA-LINUXSA-10']
    # the list has several tests. But those tests are never shown or recorded.
    # ignore to improve performance

    def __init__(self, uname, psswd, homepage):
        '''Initializes the required elements such as username and password.
        @param uname Username of Bamboo account
        @param psswd Password of Bamboo account
        @param homepage The homepage object
        '''
        self.username = uname
        self.password = psswd
        self.home_page = homepage
        self.tests = []
        self.update_test_case_data()

    def update_test_case_data(self):
        '''Ensure the existing test case data is the lastest result.
        '''
        builds = self.home_page.get_test_suite_list()
        count = 1  # used to see the progress of initialization
        for i in builds:

            print ("Initializing required data..." +
                   str(count) + "/" +
                   str(len(builds)))

            self.retrieve_list(i)
            print "\033[A \033[A"
            count += 1
        print ("Initializing required data...[Completed] ")

    def retrieve_list(self, build):
        '''Check if the existing list contains latest data. If not, update
        @param build Data of a test suite which contains the test amounts
        '''
        key = build["plan_key"]
        test_count = build["total_test"]
        date = build["start_date"]
        time = build["start_time"]
        status = self.check_if_need_update(key, int(test_count))
        if status is True:
            self.update_test_cases(key, date, time, build)

    def check_if_need_update(self, key, test_count):
        '''Check if the current list of data requires an update
        @param key The plan key of selected
        @param test_count The test count of the selected test suite
        @return True is an update is needed. False if not
        '''
        if key in self.ignore_list:
            return False
        if test_count == 0:
            return False
        if self.tests is not None:
            count = 0
            for i in self.tests:
                if i["plan_key"] == key:
                    count += 1
            if count == test_count:
                return False
        return True

    def update_test_cases(self, key, date, time, build):
        '''Check for test cases and ensure the data contains the latest result
        @param key The key pf test suite
        @param date The data the test suite is performed
        @param time The time the test suite is performed
        @param build The object contains the info of the test suite
        '''
        temp = Test_suite_page(self.username, self.password)
        test = temp.request_tests(key)
        if test is not None:  # some test suites have no tests shown
            for k in test:
                k["date"] = date
                k["time"] = time
                k["plan_key"] = build["plan_key"]
            self.update_test_lists(test, build)

    def update_test_lists(self, current_result, build):
        '''Update the test cases and remove outdated elements
        @param current_result The current result of the test cases
        @param build The info of the test suite
        '''
        if self.tests is not None:
            for i in self.tests[:]:
                if i["plan_key"] == build["plan_key"]:
                    print 'removing tests of ' + i["plan_key"]
                    self.tests.remove(i)
        self.tests += current_result

    def get_cases_from_testsuite(self, plan_key, test_name):
        '''Retrieve all the cases in a specific test suite and test
        @param plan_key Plan key of the test suite
        @param test_name The name of the test
        @return a list of cases in the tests and test suite
        '''
        temp_list = []
        for i in self.tests:
            if i["className"] == test_name:
                if i["plan_key"] == plan_key:
                    temp_list.append(i)
        return temp_list

    def get_cases_from_test(self, test_name):
        '''Retrieve all the test cases of a specific test
        @param test_name The name of the tests
        @return a list of cases that belong to a test
        '''
        temp_list = []
        for i in self.tests:
            if i["className"] == test_name:
                temp_list.append(i)
        return temp_list

    def get_test_history(self, plan_key, test_name, option="self"):
        '''Aquire the history of a test run. Self or related
        @param plan_key The plan key of the test suite
        @param test_name The name of the test
        @param option whether to get the self history or related history
        @return a list of test run history
        '''
        current_list = self.get_cases_from_test(test_name)
        temp_list = []
        target_date = self.home_page.get_date_from_plan_key(plan_key)
        key = self.rephrase_plan_key(plan_key)
        for i in current_list:
            done = False
            for k in temp_list:
                if i["plan_key"] == k["plan_key"]:
                    k["total"] += 1
                    if i["quarantined"] == "True":
                        k["quarantined"] += 1
                    else:
                        if i["status"] == "successful":
                            k["successful"] += 1
                        elif i["status"] == "failed":
                            k["failed"] += 1
                    done = True
                    break
            if done is False:
                temp = {}
                temp["plan_key"] = i["plan_key"]
                temp["date"] = i["date"]
                temp["time"] = i["time"]
                temp["total"] = 1
                temp["successful"] = 0
                temp["failed"] = 0
                temp["quarantined"] = 0
                if i["quarantined"] == "True":
                    temp["quarantined"] += 1
                else:
                    if i["status"] == "successful":
                        temp["successful"] += 1
                    elif i["status"] == "failed":
                        temp["failed"] += 1
                if option == "self":
                    if key in temp["plan_key"]:
                        temp_list.append(temp)
                elif option == "related":
                    if target_date == i["date"]:
                        if key not in temp["plan_key"]:
                            temp_list.append(temp)
        return temp_list

    def rephrase_plan_key(self, plan_key):
        '''Rephrase the plan key to the one recongnizable by Bamboo
        @param The plan key of test suite
        @return a modified plan key
        '''
        key = plan_key.split('-')
        result = key[0] + "-" + key[1]
        return result
