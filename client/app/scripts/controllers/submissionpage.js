'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:submissionpageCtrl
 * @description
 * # submissionpageCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
  .controller('submissionpageCtrl', ['$scope', '$http', 'serverURL', '$routeParams', 'AutoComplete', 'recommend', 'AuthService', function($scope, $http, serverURL, $routeParams, AutoComplete, recommend, AuthService) {

    $scope.submissionId = $routeParams.submissionId;
    $scope.assignment_list = []
    if ($scope.submissionId === 'new') {
      //get name of all assignments
      $http.get(serverURL + '/assignments', {withCredentials: true, contentType : "application/json"})
                // handle success
                .success(function(data) {
                    console.log(data);
                    console.log('assignment load success in submission page')
                    $scope.assignment_list = data;
                    // $scope.$apply();
                })
                // handle error
                .error(function(data) {
                    console.log(data);
                });
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

    $scope.submitAssignment = function() {
      console.log('submission body', $scope.submission_body)
      var newSubmission = {
        "submissionName" : $scope.submission_name,
        "submissionBody": $scope.submission_body,
        "assignmentID": $scope.selectedAssignment
      };
      if ($scope.submissionId === 'new') {
        $http.post(serverURL + '/submissions', newSubmission, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {
            $scope.assignment = data;
            console.log('essay submitted', data)
            $scope.fileSuccess = true;
            $scope.fileError = false;
            $scope.submissionId = data.submissionID;
            // $scope.$apply();
          })
          // handle error
          .error(function(data) {
            console.log(data);
            $scope.fileError = true;
            $scope.fileSuccess = false;
          });

      } else {

        $http.patch(serverURL + '/submissions/' + $scope.submissionId, newSubmission, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {
            $scope.fileSuccess = true;
            $scope.fileError = false;
            // $scope.$apply();
          })
          // handle error
          .error(function(data) {
            console.log(data);
            console.log('error patch')
            $scope.fileError = true;
            $scope.fileSuccess = false;
          });

      }
    };
  }]);
