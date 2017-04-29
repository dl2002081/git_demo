import requests
import json


bamboo_url = 'http://bamboo.digi.com/rest/api/latest/'


def request(url, uname, passwd):
    '''Concat the base address with other address to aquire data
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @return requested json file or None if does not exist
    '''
    try:
        req = requests.get(bamboo_url + url, auth=(uname, passwd), timeout=10)
        if req.status_code == 200:
            try:
                result = req.json()
            except TypeError:
                result = req.json  # Some request version need this
            return result
        else:
            return None

    # sometimes it raises connection error
    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout) as e:

        print e
        return request(url, uname, passwd)


def verify_Authentication(uname, passwd):
    '''Verify if the login information is valid
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    return True if valid, false if not
    '''
    url = 'http://bamboo.digi.com/rest/api/latest/plan?os_authType=basic'
    req = requests.get(url, auth=(uname, passwd))
    if req.status_code == 200:
        return True
    else:
        return False


def request_plan_json(uname, passwd, start=0, count=100):
    '''Request the test plan of Bamboo
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param count The amount of entry of request
    @return json file of the test plan
    '''
    link = 'project/SA.json?expand=plans&start-index=' + str(start)
    link += '&max-result=' + str(count)
    return request(link, uname, passwd)


def request_all_plan_key(uname, passwd, start=0, count=99):
    '''Aquire all the plan key from Bamboo
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param start The start index of bamboo rest api
    @param count The amount of entry
    @return a list of plan key
    '''
    key_list = []
    result = request_plan_json(uname, passwd, start, count)
    size = int(result["plans"]["size"])
    max_result = int(result["plans"]["max-result"])
    start_index = int(result["plans"]["start-index"])

    plan_json = result["plans"]["plan"]
    for i in plan_json:
        key_list.append(i["planKey"]["key"])

    if (start_index + max_result) < size:
        key_list += request_all_plan_key(uname, passwd, start + max_result)
    return key_list


def request_build_json(uname, passwd, key, start=0, count=10000):
    '''Request a list of test suites from Bamboo
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param key plan key of the test suites
    @param start The start index of Bamboo rest API
    @param count The amount of entries of request
    @return a list of test suites in json format
    '''
    link = 'result/' + key + '.json'
    link += '?expand=results.result.vcsRevisions&start-index=' + str(start)
    link += '&max-result=' + str(count)
    return request(link, uname, passwd)


def request_all_build(uname, passwd, key):
    '''Request all the SA builds
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param key Plan key of test suites
    @return a list of all test suite keys
    '''
    # max_result and size of Bamboo doesnt work properly.
    # Consider doing loop and comparision
    count = 10000
    while True:
        build_list = []
        result = request_build_json(uname, passwd, key, 0, count)
        size = int(result["results"]["size"])
        max_result = int(result["results"]["max-result"])
        if max_result > size:
            break
        else:
            count *= 10
    build_list.append(result)

    return build_list


def request_latest_result(uname, passwd, start=0, count=100):
    '''Request the latest build of the test suite builds
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param start Start index of Bamboo rest API
    @count Amount of request entries
    return the latest test suite build in json
    '''
    link = 'result.json?expand=results&'
    link += 'start-index=' + str(start) + '&max-result=' + str(count)
    return request(link, uname, passwd)


def request_all_latest_result(uname, passwd, start=0, count=100):
    '''Request all the latest build of eacg test suites
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param start Start index of Bamboo rest API
    @count Amount of request entries
    return a list of latest build keys of each test suites
    '''
    result_list = []
    result = request_latest_result(uname, passwd, start, count)
    size = int(result["results"]["size"])
    max_result = int(result["results"]["max-result"])
    start_index = int(result["results"]["start-index"])

    plan_json = result["results"]["result"]
    for i in plan_json:
        if i["key"][0:3] == "SA-":
            result_list.append(i["key"])
    if (start_index + max_result) < size:
        result_list += request_all_latest_result(uname, passwd,
                                                 start + max_result)
    return result_list


def request_test(uname, passwd, test_key):
    '''Request test cases of a specific test suite
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param test_key Key of the test suite
    @return a json file that includes the test cases of the test suite
    '''
    link = 'result/' + str(test_key) + '.json?expand=testResults.allTests'
    return request(link, uname, passwd)


def request_specific_test(uname, passwd, test_key):
    '''Request test cases of a specific test suite
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param test_key Key of the test suite
    @return a list of test cases that belong to the test suite
    '''
    test_list = []
    test_results = request_test(uname, passwd, test_key)
    try:  # need to find a method to improve. tempory solution
        test_results = test_results["testResults"]["allTests"]["testResult"]
        return test_results
    except TypeError:
        return None


def request_quarantined_test(uname, passwd, test_key):
    '''Request quarantined test cases of a specific test suite
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param test_key Key of the test suite
    @return json file that has the quarantined test cases of the test suite
    '''
    link = ('result/' + str(test_key) +
            '.json?expand=testResults.quarantinedTests')

    return request(link, uname, passwd)


def request_specific_quarantined_test(uname, passwd, test_key):
    '''Request quarantined test cases of a specific test suite
    @param uname Username of Bamboo
    @param passwd Password of Bamboo
    @param test_key Key of the test suite
    @return a list of quarantined test cases that belong to the test suite
    '''
    test_list = []
    test_results = request_quarantined_test(uname, passwd, test_key)
    try:  # need to find a method to improve. tempory solution

        test_results = (test_results["testResults"]["quarantinedTests"]
                                    ["testResult"])

        return test_results
    except TypeError:
        return None
