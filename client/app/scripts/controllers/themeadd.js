'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:submissionpageCtrl
 * @description
 * # submissionpageCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
  .controller('themeAddCtrl', ['$scope', '$http', 'serverURL', '$routeParams', 'AutoComplete', 'recommend', 'AuthService', function($scope, $http, serverURL, $routeParams, AutoComplete, recommend, AuthService) {

    $scope.themeId = $routeParams.themeId;
    $scope.assignment_list = []

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
    if ($scope.themeId === 'new') {

    } else {
      $http.get(serverURL + '/themes/' + $routeParams.themeId, {withCredentials: true, contentType : "application/json"}).success(function(data) {
        console.log('specific theme data',data);
        $scope.theme_name = data.themeName
        $scope.selectedAssignment = data.assignment_id;
        $scope.selectedColor = data.color;
        $scope.theme_sentences = data.themeSentences;
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

    $scope.saveTheme = function() {
      var newTheme = {
        "themeName": $scope.theme_name,
        "themeSentences": $scope.theme_sentences,
        "assignment_id" : $scope.selectedAssignment,
        "color" : $scope.selectedColor
      };
      if ($scope.themeId === 'new') {
        $http.post(serverURL + '/themes', newTheme, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {
            $scope.theme = data;
            console.log('theme saved', data)
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
        $http.patch(serverURL + '/themes/' + $scope.themeId, newTheme, {withCredentials: true, contentType : "application/json"})
          // handle success
          .success(function(data) {
            $scope.fileSuccess = true;
            $scope.fileError = false;
            // $scope.$apply();
          })
          // handle error
          .error(function(data) {
            console.log(data);
            console.log('error patch in theme add')
            $scope.fileError = true;
            $scope.fileSuccess = false;
          });

      }
    };
  }]);
