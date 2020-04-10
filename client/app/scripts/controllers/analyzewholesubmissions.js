'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:analyzewholesubmissionCtrl
 * @description
 * # analyzewholesubmissionCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
  .controller('analyzewholesubmissionsCtrl', ['$scope', '$http', 'serverURL', '$routeParams', 'AutoComplete', 'recommend', 'AuthService', function($scope, $http, serverURL, $routeParams, AutoComplete, recommend, AuthService) {

    $scope.submissionID = $routeParams.submissionID;
    $scope.assignmentID = $routeParams.assignmentID;
    $scope.assignment_list = [];
    $scope.colors = [];
    var index = 0;
    $scope.updatecount = 0;
    $http.get(serverURL + '/wholesubmissions/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log('whole submission data', data);
        $scope.data = data;
      });
      //themes_filterbyassignment/<int:assignment_id>'
      $http.get(serverURL + '/themes_filterbyassignment/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log('all themes with assignment id', data);
        $scope.themes = data;
      });

      $scope.$watch('updatecount', function(newValue) { //watching $scope.myResource for changes
            $http.get(serverURL + '/wholesubmissions/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
                console.log('whole submission data', data);
                $scope.data = data;
              });
              //themes_filterbyassignment/<int:assignment_id>'
              $http.get(serverURL + '/themes_filterbyassignment/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
                console.log('all themes with assignment id', data);
                $scope.themes = data;
              });
      })


     $scope.callback = function(){
            $scope.updatecount = 1^ ($scope.updatecount);
     };

    $scope.isOwner = function() {

      if (AuthService.isLoggedIn()) {
        if ("assignment" in $scope && AuthService.getUserId() === $scope.assignment.creator_id) {
          return true;
        }
        if ($scope.assignmentId === 'new') {
          return true;
        }
      }

      return false;

    };
    }
]);
