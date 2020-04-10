'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:themelistCtrl
 * @description
 * # themelistCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
    .controller('themelistCtrl', ['$scope', '$http', 'serverURL', 'AuthService', '$uibModal', function($scope, $http, serverURL, AuthService, $uibModal) {
        $scope.currentPage = 1;
        $scope.pageSize = 10;

        $scope.themes = [];

        var loadThemes = function() {
            $http.get(serverURL + '/themes', {withCredentials: true, contentType : "application/json"})
                // handle success
                .success(function(data) {
                    console.log('theme data', data);
                    console.log('theme load success')
                    $scope.themes = data;
                    // $scope.$apply();
                })
                // handle error
                .error(function(data) {
                    console.log(data);
                });

        };

        $scope.isOwner = function(theme) {
            if (AuthService.isLoggedIn()) {

                /*if (AuthService.getUserId() === theme.userID) {
                    return true;
                }*/
                return true;
            }
            return false;
        };

        $scope.delete = function(assignment) {

            var modalInstance = $uibModal.open({
                templateUrl: 'deleteModal.html',
                controller: 'deleteModalCtrl',
                size: 'sm',
                resolve: {
                    assignmentName: function() {
                        return assignment.name;
                    }
                }
            });

            modalInstance.result.then(function() {

                $http.get(serverURL + '/assignment_delete/' + assignment.id, {withCredentials: true, contentType : "application/json"})
                    // handle success
                    .success(function(data) {

                        $scope.submissions = data;
                        // $scope.$apply();
                    })
                    // handle error
                    .error(function(data) {
                        console.log(data);
                    });

            }, function() {
                // $log.info('Modal dismissed at: ' + new Date());
            });

        };

        $scope.clone = function(assignment) {

            var modalInstance = $uibModal.open({
                templateUrl: 'cloneModal.html',
                controller: 'cloneModalCtrl',
                size: 'sm',
                resolve: {
                    assignmentName: function() {
                        return assignment.name;
                    }
                }
            });

            modalInstance.result.then(function(newAssignmentName) {

                var newAssignment = {};

                newAssignment = angular.copy(concept);

                newAssignment.name = newAssignmentName;

                $http.post(serverURL + '/submissions', newAssignment, {withCredentials: true, contentType : "application/json"})
                    // handle success
                    .success(function(data) {
                        console.log(data);

                        // $scope.concepts = data.data;
                        // $scope.$apply();
                        loadSubmissions();

                    })
                    // handle error
                    .error(function(data) {
                        console.log(data);
                    });


            }, function() {
                // $log.info('Modal dismissed at: ' + new Date());
            });

        };
        loadThemes();
    }]);

angular.module('conceptvectorApp')
    .controller('cloneModalCtrl', function($scope, $uibModalInstance, conceptName) {

        $scope.conceptName = 'Copy of ' + conceptName;

        $scope.ok = function() {
            $uibModalInstance.close($scope.conceptName);
        };

        $scope.cancel = function() {
            $uibModalInstance.dismiss('cancel');
        };
    });
