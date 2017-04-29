from bamboo_request import(
    request_specific_test,
    request_specific_quarantined_test
    )
from json import dumps
import csv


class Test_suite_page(object):

    ignore_list = ['SA-LINUXSA-10']
    server_list = ['JOB1', 'HILBERT', 'OPTIMUS', 'LAPLACE', 'TURING', 'BAYES',
                   'FERMAT', 'CANTOR', 'PASCAL', 'NEWTON', 'ECHEGARAY',
                   'GALOIS', 'EULER', 'FELDMAN', 'BABELFISH', 'TESLA', 'YODA']

    # missing log links will fill that up later
    def __init__(self, uname, psswd):
        '''Initializes the required elements such as username and password.
        @param uname username of Bamboo account
        @param psswd password of Bamboo account
        '''
        self.username = uname
        self.password = psswd
        self.test_results = []

    def request_tests(self, test_key):
        '''Attempt to request the test cases of test sutie from Bamboo.
        @param test_key The plan key for the desired test suite
        @return a list of test results of the test suite
        '''
        for server in self.server_list:
            key = self.rephrase_key(test_key, server)
            self.test_results = request_specific_test(self.username,
                                                      self.password, key)

            quanantined_tests = request_specific_quarantined_test(
                self.username, self.password, key)

            if self.test_results is not None:
                break

        try:
            for i in self.test_results:
                quarantined = False
                i["className"] = i["className"].split('.')[-1]
                for k in quanantined_tests:
                    k["className"] = k["className"].split('.')[-1]
                    if i["methodName"] == k["methodName"]:
                        if i["className"] == k["className"]:
                            quarantined = True
                            break
                if quarantined is True:
                    i["quarantined"] = "True"
                else:
                    i["quarantined"] = "False"
            return self.test_results
        # sometimes there is no result
        except TypeError:
            self.test_result = None
            return self.test_result

    def rephrase_key(self, key, server):
        '''Convert the plan key to the key recongnizable by Bamboo to aquire
        tests within test suites. (ie: SA-DCDT-333 -> SA-DCDT-JOB1-333)
        @param key The original key of the test suite
        @param server The server name
        @return a modified key for test request
        '''
        splits = key.split('-')  # should use a list of all possibility
        last = splits[-1]
        splits[-1] = server  # some suite got different parts.
        splits.append(last)
        test_key = ''
        for i in splits:
            test_key += i
            if i != splits[-1]:
                test_key += '-'
        return test_key

    def get_test_status(self, test_key):
        '''Aquire the status of the tests within the test_suite.
        @param test_key The key of the test suite
        @return a list of test with their status
        '''
        self.request_tests(test_key)
        test_list = []
        if self.test_results is not None:
            for i in self.test_results:
                done = False
                for k in test_list:
                    if i["className"] == k["className"]:
                        done = True
                        k["total"] += 1
                        if i["quarantined"] == "True":
                            k["quarantined"] += 1
                        else:
                            if i["status"] == "successful":
                                k["successful"] += 1
                            elif i["status"] == "failed":
                                k["failed"] += 1
                if done is False:
                    temp = {}
                    temp["className"] = i["className"]
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

                    test_list.append(temp)
        return test_list
