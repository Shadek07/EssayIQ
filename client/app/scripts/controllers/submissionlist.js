'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:SubmissionlistCtrl
 * @description
 * # SubmissionlistCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
    .controller('SubmissionlistCtrl', ['$scope', '$http', 'serverURL', 'AuthService', '$uibModal', function($scope, $http, serverURL, AuthService, $uibModal) {
        $scope.currentPage = 1;
        $scope.pageSize = 10;

        $scope.submissions = [];
        $scope.assignments = [];

        var loadSubmissions = function() {
            $http.get(serverURL + '/submissions', {withCredentials: true, contentType : "application/json"})
                // handle success
                .success(function(data) {
                    console.log(data);
                    console.log('submission load success')
                    $scope.submissions = data;

                    var map = new Map();
                    for (const item of $scope.submissions) {
                        if(!map.has(item.assignmentID)){
                            map.set(item.assignmentID, true);    // set any value to Map
                            $scope.assignments.push({
                                'assignmentID': item.assignmentID,
                                'name': item.name});
                        }
                    }
                    // $scope.$apply();
                })
                // handle error
                .error(function(data) {
                    console.log(data);
                });
        };
        $scope.checkIfAssignmentSelected = function(){
            if($scope.selectedAssignment !== "")
                return true;
             else
                return false;

        };
        $scope.isOwner = function(submission) {

            if (AuthService.isLoggedIn()) {

                if (AuthService.getUserId() === submission.userID) {
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
        loadSubmissions();
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
