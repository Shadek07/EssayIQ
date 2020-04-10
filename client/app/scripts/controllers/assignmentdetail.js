'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:AssignmentdetailCtrl
 * @description
 * # AssignmentdetailCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
  .controller('AssignmentdetailCtrl', ['$scope', '$http', 'serverURL', '$routeParams', 'AutoComplete', 'recommend', 'AuthService', function($scope, $http, serverURL, $routeParams, AutoComplete, recommend, AuthService) {

    $scope.assignmentId = $routeParams.assignmentId;
    $scope.download_url = "/#/download_concepts/" + $routeParams.conceptId;

    var newPositiveWords = [];
    var newNegativeWords = [];

    if ($scope.assignmentId === 'new') {
      $scope.assignment_title = '';
      $scope.assignment_name = '';
      $scope.assignment_desc = '';
    } else {

      $http.get(serverURL + '/assignments/' + $routeParams.assignmentId, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log(data);
        $scope.assignment = data;
        $scope.assignment_name = $scope.assignment.name;
        $scope.assignment_title = $scope.assignment.title;
        $scope.assignment_desc = $scope.assignment.description;
      });

    }

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

    $scope.saveAssignment = function() {

      var newAssignment = {
        "name": $scope.assignment_name,
        "title": $scope.assignment_title,
        "description": $scope.assignment_desc
      };

      if ($scope.assignmentId === 'new') {

        $http.post(serverURL + '/assignments', newAssignment, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {
            $scope.assignment = data;
            console.log('assignment saved', data)
            $scope.fileSuccess = true;
            $scope.fileError = false;
            $scope.assignmentId = data.id;
            // $scope.$apply();
          })
          // handle error
          .error(function(data) {
            console.log(data);
            $scope.fileError = true;
            $scope.fileSuccess = false;
          });

      } else {

        $http.patch(serverURL + '/assignments/' + $scope.assignmentId, newAssignment, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {

            $scope.fileSuccess = true;
            $scope.fileError = false;
            // $scope.$apply();
          })
          // handle error
          .error(function(data) {
            console.log(data);
            $scope.fileError = true;
            $scope.fileSuccess = false;
          });

      }
    };
  }]);
