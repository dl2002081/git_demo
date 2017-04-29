angular.module("general", []);

function generalCtrl($scope){

        $scope.history_show_status = '[show all results]';
        $scope.history_quantity = 10;
        $scope.history_related_show_status = '[show all results]';
        $scope.history_related_quantity = 10;
        $scope.testHistory = [];
        $scope.testHisotyRelated = [];
        $scope.testSuiteTabArray = [];
        $scope.selectedTestSuiteTab = 0;
        $scope.selectedTestTab = 0;
        $scope.selectedCaseTab = 0;
        $scope.selectedHistoryTab = 0;
        $scope.selectedRelatedHistoryTab = 0;


        $scope.relatedHistorySelect = function(value){
            $scope.selectedRelatedHistoryTab = value;
        } 

        $scope.historySelect = function(value){
            $scope.selectedHistoryTab = value;
        } 

        $scope.caseSelect = function(value){
            $scope.selectedCaseTab = value;
        }  

        $scope.testSuiteSelect = function(value){
            $scope.selectedTestSuiteTab = value;
        }        

        $scope.testSelect = function(value){
            $scope.selectedTestTab = value;
        }

        $scope.assignSelected = function(obj){
            if (obj.outCome == "success"){
                obj.outCome = "passed";
            }else if (obj.outCome == "danger"){
                obj.outCome = "failed";
            }
        }

        $scope.setOutcome = function(){
            if(this.outCome != "passed" && this.outCome != "failed"){
                if(parseInt(this.data.test_failed) === 0){
                    this.outCome = "success";
                }else{
                    this.outCome = "danger";
                }
            }
        }

        $scope.setTestOutcome = function(){
            if(this.outCome != "passed" && this.outCome != "failed"){
                if(parseInt(this.testSuiteDetail.failed) === 0){
                    this.outCome = "success";
                }else{
                    this.outCome = "danger";
                }
            }
        }

        $scope.setCaseOutcome = function(){
            if(this.outCome != "warning"){
                if(this.case.status === "successful"){
                    this.outCome = "success";
                }else{
                    this.outCome = "danger";
                }
            }
        }

        $scope.setHistoryOutcome = function(){
            if(this.outCome != "warning"){
                if(parseInt(this.test.failed) === 0){
                    this.outCome = "success";
                }else{
                    this.outCome = "danger";
                }
            }
        }

        $scope.set_history_data = function(history, related_history){
            $scope.testHistory = history;
            console.log("length");
            console.log($scope.testHistory.length);
            $scope.testHisotyRelated = related_history;
        }



        $scope.toggle_history_status = function(){
            if($scope.history_show_status === "[show all results]"){
                $scope.history_show_status = "[show top 10 results]";
                $scope.history_quantity = $scope.testHistory.length;
            }else{
                $scope.history_show_status = "[show all results]";
                $scope.history_quantity = 10;
            }
        }

        $scope.toggle_history_related_status = function(){
            if($scope.history_related_show_status === "[show all results]"){
                $scope.history_related_show_status = "[show top 10 results]";
                $scope.history_related_quantity = $scope.testHisotyRelated.length;
            }else{
                $scope.history_related_show_status = "[show all results]";
                $scope.history_related_quantity = 10;
            }
        }
}
