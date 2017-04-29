import bamboo_request
import csv
from json import dumps


class Homepage(object):

    def __init__(self, uname, psswd):
        '''Initializes the required elements such as username and password.
        @param uname Username of Bamboo account
        @param psswd Password of Bamboo account
        '''
        self.username = uname
        self.password = psswd
        self.suite_list = []

    def update_suite_data(self):
        '''Ensure the existing test suite data is the latest result.
        '''
        self.key_list = bamboo_request.request_all_plan_key(
            self.username, self.password)

        latest_result = bamboo_request.request_all_latest_result(
            self.username, self.password)

        count = 1
        for keys in self.key_list:

            print ("Aquiring plan keys..." +
                   str(count) + "/" +
                   str(len(self.key_list)))

            for latest in latest_result:
                if keys in latest:
                    # to ensure that the ket/latest pair
                    self.retrieve_list(keys, latest)
                    break
            count += 1
            print "\033[A \033[A"
        print "Aquiring plan keys...[Completed]"

    def get_test_suite_list(self):
        ''' Aquires the current list of tests suites.
        @return a list of test suites
        '''
        self.update_suite_data()
        return self.suite_list

    def display_suites_for_given_date(self, date):
        '''Attempt to extract the test suite performed on the give date.
        @param date string of date in yyyy-mm-dd format
        @return a list of test suite data of the given date
        '''
        self.update_suite_data()
        output_list = []
        for i in self.suite_list:
            if i["start_date"] == date:
                output_list.append(i)
        return output_list

    def get_all_dates(self):
        '''Attempt to aquire the dates that contains test runs.
        @return a list of date that contains test runs
        '''
        dates = []
        for i in self.suite_list:
            if i["start_date"] not in dates:
                dates.append(i["start_date"])
        dates = sorted(dates, reverse=True)
        return dates

    # check if latest build is within the result
    def check_if_need_update(self, key, current_build, latest_build):
        '''Check if the current stored data requires an update.
        @param key The plan key
        @param current_build A list of test suites corresponding to the key
        @param latest_build The key og latest build in the catagory
        @return True if the data is outdated, False if the data is latest.
        '''
        if current_build is not None:
            for i in current_build:
                if i["plan_key"] == latest_build:  # if found, do nothing
                    return False
        return True

    def retrieve_list(self, key, latest_build):
        '''Aquire the latest data if an update is required.
        @param key The plan key
        @param latest_build The key of latest build in the catagory
        '''
        temp_list = self.suite_list
        status = self.check_if_need_update(key, temp_list, latest_build)
        if status is True:
            self.get_result_from_bamboo(key)

    def get_result_from_bamboo(self, key):
        '''Request the related json file from bamboo and extract each suite.
        @param key The key for the test suites
        '''
        current_result = []

        result = bamboo_request.request_all_build(
            self.username, self.password, key)

        for i in result:
            json_result = i["results"]["result"]
            for n in json_result:
                current_result.append(self.assign_properties(n))
        self.update_suite_list(current_result, key)

    def update_suite_list(self, current_result, key):
        '''Remove duplicated data and append the new test suite data.
        @param current_result A list of latest test suite data
        @param key The key for the test suites
        '''
        if self.suite_list is not None:
            for i in self.suite_list[:]:
                if key in i["plan_key"]:
                    print 'removing outdated element of ' + i["plan_key"]
                    self.suite_list.remove(i)
        self.suite_list += current_result

    def assign_properties(self, json_result):
        '''Extract the data from json and group them into a new dict.
        @param json_result The json result for each test suite
        '''
        suite_dict = {}
        suite_dict["plan_key"] = json_result["buildResultKey"]
        suite_dict["name"] = json_result["planName"]
        suite_dict["start_date"] = json_result["buildStartedTime"][0:10]
        suite_dict["end_date"] = json_result["buildCompletedTime"][0:10]
        suite_dict["start_time"] = json_result["buildStartedTime"][11:16]
        suite_dict["end_time"] = json_result["buildCompletedTime"][11:16]
        suite_dict["test_passed"] = int(json_result["successfulTestCount"])
        suite_dict["test_failed"] = int(json_result["failedTestCount"])

        suite_dict["test_quarantined"] = int(
            json_result["quarantinedTestCount"])

        suite_dict["total_test"] = (suite_dict["test_passed"] +
                                    suite_dict["test_failed"] +
                                    suite_dict["test_quarantined"])

        return suite_dict

    def get_date_from_plan_key(self, key):
        '''Attempt to get the date for test suite corresponds to the key.
        @param key The plan key for the test suite
        @return the date that the test suite is performed
        '''
        for i in self.suite_list:
            if i["plan_key"] == key:
                return i["start_date"]
