'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:AssignmentlistCtrl
 * @description
 * # AssignmentlistCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
    .controller('AssignmentlistCtrl', ['$scope', '$http', 'serverURL', 'AuthService', '$uibModal', function($scope, $http, serverURL, AuthService, $uibModal) {
        $scope.currentPage = 1;
        $scope.pageSize = 10;

        $scope.assignments = [];

        var loadAssignments = function() {
            $http.get(serverURL + '/assignments', {withCredentials: true, contentType : "application/json"})
                // handle success
                .success(function(data) {
                    //console.log(data);
                    console.log('assignment load success')
                    $scope.assignments = data;
                    // $scope.$apply();
                })
                // handle error
                .error(function(data) {
                    console.log(data);
                });

        };
        $scope.isOwner = function(assignment) {

            if (AuthService.isLoggedIn()) {

                if (AuthService.getUserId() === assignment.creator_id) {
                    return true;
                }
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

                        $scope.assignments = data;
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

                $http.post(serverURL + '/assignments', newAssignment, {withCredentials: true, contentType : "application/json"})
                    // handle success
                    .success(function(data) {
                        console.log(data);

                        // $scope.concepts = data.data;
                        // $scope.$apply();
                        loadAssignments();

                    })
                    // handle error
                    .error(function(data) {
                        console.log(data);
                    });


            }, function() {
                // $log.info('Modal dismissed at: ' + new Date());
            });

        };
        loadAssignments();
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
