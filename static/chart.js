angular.module("chart", []);

function chartCtrl($scope) {

    $scope.chartData = [{ key: "Passed",y: 1}, {key: "Quarantined", y: 0}];

    $scope.xFunction = function() {
      return function(d) {
        return d.key;
      };
    }
    $scope.yFunction = function() {
      return function(d) {
        return d.y;
      };
    }

    $scope.descriptionFunction = function() {
      return function(d) {
        return d.key;
      }
    }

    var colorArray = ["#00ff60", "Yellow", "Red"];

    $scope.colorFunction = function(){
        return function(d, i) {
            return colorArray[i];
    };
    }

    $scope.toolTipContentFunction = function(){
        return function(key, x, y, e, graph) {
        return "<h4>" + key + ": " + String(parseInt(x)) + "</h4>"
        }
    }

    $scope.$watchGroup(['pass', 'fail', 'total', 'quarantine'], function(){
            $scope.chartData = [{ key: "Passed",y: $scope.pass}, {key: "Quarantined", y: $scope.quarantine},
                                {key: "Failed", y: $scope.fail}];
    })

  }
