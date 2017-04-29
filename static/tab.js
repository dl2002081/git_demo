var app = angular.module("app", ['nvd3ChartDirectives', 'chart', 'general']);

    app.controller("tabCtrl", function($scope, $http) {
        $scope.myData = {};
        $scope.myDate = {};
        $scope.homeTab = true;
        $scope.testSuiteTab = false;
        $scope.testSuiteTab = false;
        $scope.testTable = false;
        $scope.testsuite_sort = 'name';
        $scope.test_sort = 'className';
        $scope.case_sort = 'methodName';
        $scope.history_sort = 'date';
        $scope.historyRelated_sort = 'date';
        $scope.chart_title = "Daily Results";
        $scope.total = 0;
        $scope.pass = 1;
        $scope.fail = 0;
        $scope.quarantine = 0;
        $scope.currentState = 0;

        $scope.setState = function(value, revert_data){
            //state 0 => tab 1 on, others off
            //state 1 => not used yet
            //state 2 => tab 2 on, tab 1 partial on, others off
            //state 3 => tab 3 on, tab 1/2 partial on     
            state = [false, false, false, false];
            for (i = value - 1; i < value + 1; i++){
                if (i - 1 >= 0){
                    state[i] = true;
                }
                state[i + i] = true;
            }
                $scope.homeTab = state[0];
                $scope.testSuiteTab = state[1];
                $scope.testSuiteTable = state[2];
                $scope.testTable = state[3];
                $scope.currentState = value;
            if (revert_data != null){
                $scope.revertChartData();
            }
        }

        $scope.revertChartData = function(){
            if($scope.currentState === 0){
                $scope.chart_title = "Daily Results";
                $scope.pass = $scope.old_testSuiteData[0];
                $scope.fail = $scope.old_testSuiteData[1];
                $scope.total = $scope.old_testSuiteData[2];
                $scope.quarantine = $scope.old_testSuiteData[3];
            }else if($scope.currentState === 2){
                $scope.chart_title = "Suite Results";
                $scope.pass = $scope.old_testData[0];
                $scope.fail = $scope.old_testData[1];
                $scope.total = $scope.old_testData[2];
                $scope.quarantine = $scope.old_testData[3];
            }
        }

        $scope.assignChartData = function(data){
            if ($scope.currentState === 0){
                $scope.pass = 0;
                $scope.fail = 0;
                $scope.total = 0;
                $scope.quarantine = 0;
                for (i = 0; i < data.length; i++){
                    $scope.pass += data[i].test_passed;
                    $scope.fail += data[i].test_failed;
                    $scope.total += data[i].total_test;
                    $scope.quarantine += data[i].test_quarantined;
                    $scope.old_testSuiteData = [];
                    $scope.old_testSuiteData = [$scope.pass, $scope.fail, $scope.total, $scope.quarantine];  // for going back               
                }
            }else{
                $scope.pass = $scope.selected_pass;
                $scope.fail = $scope.selected_fail;
                $scope.total = $scope.selected_total;
                $scope.quarantine = $scope.selected_quarantine;
                if ($scope.currentState === 2){
                    $scope.old_testData = [$scope.pass, $scope.fail, $scope.total, $scope.quarantine];  // for going back  
                }
            }
        }

        $scope.getData = function(date){

            if (date === null){ //if null, get today's date
                var tmp = new Date();
                date = tmp.getFullYear() + '-' + ('0' + (tmp.getMonth() + 1)).slice(-2) + '-' + ('0' + tmp.getDate()).slice(-2);
            }

            var url = window.location.origin;
            url = url.concat("/home/date/");
            url = url.concat(date);
            $scope.load = true;
            $scope.setState(0);
            $scope.myData = [];
            var responsePromise = $http.get(url);

            responsePromise.success(function(data, status, headers, config) {
                $scope.load = false;         
                $scope.myData = data.result;
                $scope.myDate = data.date;
                $scope.things = $scope.myDate[0];
                $scope.testSuiteSelect(0);
                $scope.chart_title = "Daily Results";
                $scope.assignChartData($scope.myData);
            });

            responsePromise.error(function(data, status, headers, config) {
                $scope.load = false;
                console.log("Get Error");
            });
       }
 
        $scope.getData(null);


        $scope.expandTestSuite = function(){
            $scope.selected_testsuite = this.data.plan_key;
            //dummy assignments for chart
            $scope.selected_pass = this.data.test_passed;
            $scope.selected_fail = this.data.test_failed;
            $scope.selected_total = this.data.total_test;
            $scope.selected_quarantine = this.data.test_quarantined;

            if($scope.lastSelectedTestSuite){
                $scope.lastSelectedTestSuite.outCome = $scope.lastSelectedTestSuiteOutCome;
            }
            $scope.lastSelectedTestSuiteOutCome = this.outCome;
            $scope.lastSelectedTestSuite = this;
            $scope.assignSelected(this);

            var url = window.location.origin;
            url = url.concat("/testsuite/");
            url = url.concat(this.data.plan_key);
            $scope.load = true;
            $scope.setState(2);
            $scope.testSuite = [];
            var responsePromise = $http.get(url);

            responsePromise.success(function(data, status, headers, config) {
                $scope.load = false;
                $scope.testSuite = data.result;
                $scope.testSelect(0);
                $scope.chart_title = "Suite Results";
                $scope.assignChartData(null);
            });

            responsePromise.error(function(data, status, headers, config) {
                $scope.load = false
                console.log("error3");
            });
        }

        $scope.expandTest = function(){
            console.log($scope.selected_testsuite)
            console.log(this.testSuiteDetail.className)
            $scope.test = {};

            $scope.selected_pass = this.testSuiteDetail.successful;
            $scope.selected_fail = this.testSuiteDetail.failed;
            $scope.selected_total = this.testSuiteDetail.total;
            $scope.selected_quarantine = this.testSuiteDetail.quarantined;

            if($scope.lastSelectedTest){
                $scope.lastSelectedTest.outCome = $scope.lastSelectedTestOutCome;
            }
            $scope.lastSelectedTestOutCome = this.outCome;
            $scope.lastSelectedTest = this;

            $scope.assignSelected(this);

            $scope.load = true
            //$scope.setState(2);

            var url = window.location.origin;
            url = url.concat("/test/");
            url = url.concat($scope.selected_testsuite)
            url = url.concat('/')
            url = url.concat(this.testSuiteDetail.className)
            $scope.setState(3);
            $scope.set_history_data([], []);
            $scope.testCases = [];

            var responsePromise = $http.get(url);


            responsePromise.success(function(data, status, headers, config) {
                console.log("ok")
                $scope.testCases = data.result;
                $scope.set_history_data(data.history_self, data.history_others);
                console.log("after")
                $scope.load = false
                $scope.caseSelect(0);
                $scope.historySelect(0);
                $scope.relatedHistorySelect(0);
                $scope.setState(3);
                $scope.chart_title = "Test Results";
                $scope.assignChartData(null);
            });

            responsePromise.error(function(data, status, headers, config) {
                $scope.load = false
                console.log("error3");
            });
        }

    });
