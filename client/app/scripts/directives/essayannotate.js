'use strict';

/**
 * @ngdoc directive
 * @name conceptvectorApp.directive:essayannotate
 * @description
 * # essayannotate
 */
 //['ui.bootstrap']
angular.module('conceptvectorApp')
    .directive('essayannotate', function($compile, $uibModal) {
        var controller = ['$scope', '$uibModal', '$http', 'serverURL', function ($scope, $uibModal, $http, serverURL) {

          function init() {
              console.log('controller themes', $scope.themes);
          }
          $scope.sentenceDialog =  function(index, sentence){
                  console.log('index value', index, sentence);
                  console.log('submission name', $scope.submissionname);
                  var DialogController = ['$scope','$uibModalInstance' ,function ($scope, $uibModalInstance) {
                        console.log('modal themes', $scope.themes);
                        //console.log('selected param', $scope.$resolve.params.name);
                        $scope.source = {
                          selectedtheme: '-1',
                          selectedsentence: sentence,
                          submissionname: $scope.submissionname
                        };
                        $scope.$watch('source.selectedtheme', function(newValue, oldValue) {
                            console.log(newValue, oldValue);
                        });
                        $scope.cancel = function () {
                            $uibModalInstance.dismiss('cancel');
                        };
                        $scope.save = function () {
                           console.log('selected theme', $scope.source.selectedtheme);
                           $http.post(serverURL + '/saveAnnotation', {"submissionname": $scope.submissionname, "sentenceindex": index, "selectedtheme": $scope.source.selectedtheme, "assignmentid" : $scope.assignmentid
                            }, {withCredentials: true, contentType : "application/json"})
                                // handle success
                                .success(function(data) {
                                  $scope.fileSuccess = true;
                                  $scope.annotation.push({'assignmentid': $scope.assignmentid, 'submissionname': $scope.submissionname, 'sentenceindex': index, 'selectedtheme': $scope.source.selectedtheme});
                                  $scope.fileError = false;
                                  $uibModalInstance.dismiss('save');
                                })
                                .error(function(data) {
                                  $scope.fileError = true;
                                  $scope.fileSuccess = false;
                                });
                        };
                        var vm = this;
                    }];
                    $scope.themechange = function(value){
                        console.log('theme value',value);
                    };
                    var modalInstance = $uibModal.open({
                              templateUrl: 'annotateSentence.html',
                              controller: DialogController,
                              controllerAs: 'vm',
                              size: 'md',
                              scope: $scope,
                              bindToController: true,
                              resolve: {
                                  params: function () {
                                      return {
                                         name: "John",
                                         age: 32
                                      };
                                   }
                              }
                          });
           };
          init();
          $scope.clickSentence = function(index, sentence){
              console.log('scope sentences', $scope.sentences);
              console.log('sentence', sentence);
              $scope.sentenceDialog(index, sentence);
          };
          $scope.getClass = function(index){
              var className = "";
              angular.forEach($scope.annotation, function(x, key) {
                  //console.log($scope.assignmentID)
                 if(parseInt(x['assignmentid']) === parseInt($scope.assignmentid) && parseInt(x['sentenceindex']) === index && x['submissionname'] ===  $scope.submissionname)
                  {
                      className = "highlightAnnotation";
                  }
              });
              return className;
          }
      }],

      template = '<span ng-class="getClass($index)" ng-click="clickSentence($index, sentence)" ng-repeat="sentence in sentences">{{" "}} {{sentence}}</span>';
        return {
            restrict: 'EA',
            transclude: true,
            scope: {
                sentences: '=',
                themes: '=',
                submissionname: '=',
                assignmentid: '=',
                annotation: '='
            },
            controller: controller,
            template: template
        };
    });
