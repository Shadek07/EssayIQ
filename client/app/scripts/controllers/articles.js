'use strict';

/**
 * @ngdoc function
 * @name conceptvectorApp.controller:ArticlesCtrl
 * @description
 * # ArticlesCtrl
 * Controller of the conceptvectorApp
 */
angular.module('conceptvectorApp')
    .controller('ArticlesCtrl', ['$scope', '$http', 'serverURL', function($scope, $http, serverURL) {

        $scope.articles = ['hello'];
        $scope.currentPage = 1;
        $scope.pageSize = 10;

        $scope.concepts = [];

        var loadArticles = function() {
            $scope.loadingPromise = $http.get(serverURL + '/articles', {withCredentials: true, contentType : "application/json"})
                // handle success
                .success(function(data) {
                    console.log(data);

                    $scope.articles = data;
                    // $scope.$apply();
                })
                // handle error
                .error(function(data) {
                    console.log(data);
                });

        };

        loadArticles();

    }]);
