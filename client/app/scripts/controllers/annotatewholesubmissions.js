'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:analyzewholesubmissionCtrl
 * @description
 * # analyzewholesubmissionCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
  .controller('annotatewholesubmissionsCtrl', ['$scope', '$http', 'serverURL', '$routeParams', 'AutoComplete', 'recommend', 'AuthService', function($scope, $http, serverURL, $routeParams, AutoComplete, recommend, AuthService) {
    $scope.submissionID = $routeParams.submissionID;
    $scope.assignmentID = parseInt($routeParams.assignmentID);
    $scope.assignment_list = [];
    $scope.colors = [];
    var index = 0;
    $scope.userid = AuthService.getUserId();
    $scope.username = AuthService.getUserName();

    $http.get(serverURL + '/assignments/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log(data);
        $scope.assignment = data;
        $scope.assignmentname = $scope.assignment.name;
      });
    $http.get(serverURL + '/annotatewholesubmissions/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log('whole submission data', data);
        $scope.data = data;
      });
      //themes_filterbyassignment/<int:assignment_id>'
      $http.get(serverURL + '/themes_filterbyassignment/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log('all themes with assignment id', data);
        $scope.themes = data;
      });

      $http.get(serverURL + '/GetAnnotation/'+ $scope.userid, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {
            console.log('get method annotation', data);
            $scope.annotation = data;
            $scope.fileSuccess = true;
            $scope.fileError = false;
            // $scope.$apply();
          })
          // handle error
          .error(function(data) {
              $scope.fileError = true;
              $scope.fileSuccess = false;
          });

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
