# Uranus

## Description

Uranus is a web that requests data from Bamboo server and presents them to the user in a user-friendly UI.

## Installation

        sudo pip install Flask
        clone this repo
        python run_server.py
        input the username and password for Bamboo

## API

Uranus serves a webpage as its interface and also utilizes a RESTful API. The basic idea is that it serves a home page which performs GET request to the RESTful API of itself to acquire the required data and present them in the UI. Below are some of the examples:

### /home

The /home path serves the homepage which contains the UI.

### /date

A [GET] will return a list of dates which contain at least one test runs in json format.

##### Response Object:

    {
        "date": [
            "date 1", 
            "date 2", 
            "date 3", 
            ...,
        ]
    }

### /home/date/{str:date_target}

A [GET] will return a list of test suites that was performed on the date defined by {str:date_target} in "yyyy-mm-dd" format. A list of dates which contain at least one test runs are also contained in the returned resources to minimize the amount of GET operation. The returned resources is in json format.

##### Response Object:

    {
        "date": 
            [
                "date 1", 
                "date 2", 
                "date 3", 
                ...,
            ],
        "result": 
            [
                {
                    "end_date":            The date the test suite is completed, 
                    "end_time":            The time the test suite is completed, 
                    "name":                The name of the test suite, 
                    "plan_key":            The plan key of the corresponding test suite, 
                    "start_date":          The date the test suite is started, 
                    "start_time":          The time the test suite is started, 
                    "test_failed":         The amount of failures in the test suite, 
                    "test_passed":         The amount passes in the test suite, 
                    "test_quarantined":    The amount of quarantined tests in the test suite, 
                    "total_test":          The total amount of the tests
                }
            ]
    }

### /testsuite/{str:plan_key}

A [GET] will return a list of tests contained in the selected test suite defined by the {str:plan_key} parameter in json format.

##### Response Object:

    {
        "result": 
            [
                {
                    "className":      The name of the test, 
                    "failed":         The amount of failed cases in the test, 
                    "quarantined":    The amount of quarantined cases in the test, 
                    "successful":     The amount of successful cases in the test, 
                    "total":          The total amount of the cases in the test
                }, 
            ]
    }

### /test/{str:plan_key}/{str:test_name>}

A [GET] will return a list of cases contained in the selected test defined by the {str:plan_key} and {str:test_name} parameter. Test histories and related tests of the day is also included in the returned data. The returned data is in json format.

##### Response Object:

    {
        "history_others": 
            [
                {
                    "date":           The date of which the related test is performed, 
                    "failed":         The amount of failure of the related test, 
                    "plan_key":       The plan key corresponding to the related test, 
                    "quarantined":    The amount of quarantined cases of the related test, 
                    "successful":     The amount of successful cases of the related test, 
                    "time":           The time that the related test begins, 
                    "total":          The total amount of cases in the related test
                }, 
            ], 
        "history_self": 
            [
                {
                    "date":           The date of which the test history is performed, 
                    "failed":         The amount of failure of the test history, 
                    "plan_key":       The plan key corresponding to the test history, 
                    "quarantined":    The amount of quarantined cases of the test history, 
                    "successful":     The amount of successful cases of the test history, 
                    "time":           The time that the test history begins, 
                    "total":          The total amount of cases in the test history
                }, 
            ], 
        "result": 
            [
                {
                    "className":      The name of the test, 
                    "date":           The date the test is performed, 
                    "methodName":     The name of the case, 
                    "plan_key":       The test suite key that the case belongs, 
                    "quarantined":    Whether the case is quarantined, 
                    "status":         Whether the case is successful or failed, 
                    "time":           The time in which the case is performed
                }, 
            ]
        }

