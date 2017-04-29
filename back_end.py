from flask import (Flask, jsonify, request, Response, render_template,
                   send_from_directory)
from functools import wraps
from bamboo_request import verify_Authentication
from home_page_material import Homepage
from test_suite_page import Test_suite_page
from test_page import Test_page
from json import dumps
import time


app = Flask(__name__)


def server_init(uname, psswd):
    '''Initialize the required objects for server
    @param uname Username of Bamboo
    @param pssed Password of Bamboo
    '''

    print "test push"
    global home_page
    home_page = Homepage(uname, psswd)
    global test_suite_page
    test_suite_page = Test_suite_page(uname, psswd)
    global test_page
    test_page = Test_page(uname, psswd, home_page)


def server_run(uname, psswd):
    '''Check login information. If valid, run server.
    @param uname Username of Bamboo
    @param pssed Password of Bamboo
    '''
    print "Varifying Login Information..."
    if verify_Authentication(uname, psswd) is True:
        print "\033[A                             \033[A"
        print "Varifying Login Information...[Valid]"
        server_init(uname, psswd)
        app.run(host='0.0.0.0')
    else:
        print "\033[A                             \033[A"
        print "Varifying Login Information...[Invalid]"


@app.route('/favicon.ico')
def favicon():
    '''Favicon for webpage
    @return a icon for webpage
    '''
    return send_from_directory(os.path.join(app.root_path, 'static/favicon'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/date')
def get_date_list():
    '''Aquires all the dates that has test runs
    @return all the dates that has test runs in json
    '''
    global home_page
    date = home_page.get_all_dates()
    json_result = {}
    json_result["date"] = date
    return jsonify(json_result)


@app.route('/home')
def display_default_home():
    '''Display homepage
    @return render a home page
    '''
    return render_template('home.html')


@app.route('/home/date/<date_target>')
def display_home_with_target_date(date_target):
    '''Display all test suites performed on a specific date
    @param date_target The target date to look for test suites
    @return date and tests that is performed on the day in json
    '''
    global home_page
    date_list = home_page.get_all_dates()
    result = home_page.display_suites_for_given_date(str(date_target))
    json_result = {}
    json_result["result"] = result
    json_result["date"] = date_list
    return jsonify(json_result)


@app.route('/testsuite/<plan_key>')
def display_test_suite(plan_key):
    '''Display all the test status of a given test suite
    @param plan_key The key of the test suite
    @return the test status of the tests of the test suite in json
    '''
    global test_suite_page
    result = test_suite_page.get_test_status(str(plan_key))
    json_result = {}
    json_result["result"] = result
    return jsonify(json_result)


@app.route('/test/<plan_key>/<test_name>')
def display_test_case(plan_key, test_name):
    '''Display the test cases of the test and test suite
    @param plan_key The key of the test suite
    @param test_name The test name that need to look for
    @return test cases of the test and test suite in json
    '''
    global test_page
    test_page.update_test_case_data()  # to ensure the data is newest
    result = test_page.get_cases_from_testsuite(str(plan_key), str(test_name))

    history_self = test_page.get_test_history(str(plan_key),
                                              str(test_name),
                                              "self")

    history_others = test_page.get_test_history(str(plan_key),
                                                str(test_name),
                                                "related")

    json_result = {}
    json_result["result"] = result
    json_result["history_self"] = history_self
    json_result["history_others"] = history_others
    return jsonify(json_result)
