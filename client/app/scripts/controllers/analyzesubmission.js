'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:analyzesubmissionCtrl
 * @description
 * # analyzesubmissionCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
  .controller('analyzesubmissionCtrl', ['$scope','$http', 'serverURL', '$routeParams', 'AutoComplete', 'recommend', 'AuthService', '$uibModal', function($scope, $http, serverURL, $routeParams, AutoComplete, recommend, AuthService, $uibModal) {

    $scope.submissionID = $routeParams.submissionID;
    $scope.assignmentID = $routeParams.assignmentID;
    $scope.assignment_list = [];
    $scope.colors = [];
    var index = 0;
    $http.get(serverURL + '/submissions/' + $routeParams.submissionID + '/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log(data);
        $scope.data = data;
      });
      //themes_filterbyassignment/<int:assignment_id>'
      $http.get(serverURL + '/themes_filterbyassignment/' + $routeParams.assignmentID, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log('all themes with assignment id', data);
        $scope.themes = data;
      });

      /*$scope.sentenceDialog = function(value) {

            var modalInstance = $uibModal.open({
                templateUrl: 'sentenceDialog.html',
                controller: 'sentenceDialogCtrl',
                size: 'sm',
                resolve: {
                    value: function() {
                        return value;
                    }
                }
            });

            modalInstance.result.then(function() {
                console.log("inside.............");
                /*$http.get(serverURL + '/concept_delete/' + concept.id, {withCredentials: true, contentType : "application/json"})
                    // handle success
                    .success(function(data) {

                        $scope.concepts = data;
                        // $scope.$apply();
                    })
                    // handle error
                    .error(function(data) {
                        console.log(data);
                    });*/

            /*}, function() {
                // $log.info('Modal dismissed at: ' + new Date());
            });

        };*/

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
