'use strict';

/**
 * @ngdoc directive
 * @name conceptvectorApp.directive:essayhighlight
 * @description
 * # essayhighlight
 */
 //['ui.bootstrap']

 angular.module('conceptvectorApp')
    .directive('essayhighlight', function($compile, $uibModal) {
        var controller = ['$scope', '$uibModal', '$http', 'serverURL', function ($scope, $uibModal, $http, serverURL) {

          function init() {
              console.log('controller themes', $scope.themes);
          }
          $scope.sentenceDialog =  function(index, sentence, themeid){
                  console.log('index value', index, sentence);
                  //console.log('submission name', $scope.submissionname);
                  var DialogController = ['$scope','$uibModalInstance' ,function ($scope, $uibModalInstance) {
                        console.log('modal themes', $scope.themes);
                        //console.log('selected param', $scope.$resolve.params.name);
                        $scope.source = {
                          selectedtheme: '-1',
                          selectedsentence: sentence,
                          themeid: themeid,
                          themename: $scope.thememarkers[index],
                          selectedthemesentence: $scope.ts[index],
                          submissionname: $scope.submissionname
                        };
                        $scope.$watch('source.selectedtheme', function(newValue, oldValue) {
                            console.log(newValue, oldValue);
                        });
                        $scope.DeleteThemeSentence = function () {
                            console.log('abc');
                             $http.patch(serverURL + '/deletethemesentence', {"themesentence": $scope.source.selectedthemesentence, "selectedtheme": themeid
                              }, {withCredentials: true, contentType : "application/json"})
                                .success(function(data) {
                                  $scope.fileSuccess = true;
                                  $scope.fileError = false;
                                  $uibModalInstance.dismiss('DeleteThemeSentence');
                                  $scope.callbackFunction();
                                })
                                .error(function(data) {
                                  $scope.fileError = true;
                                  $scope.fileSuccess = false;
                                });
                        };
                        $scope.AddEssaySentence = function () {
                           console.log('selected theme', $scope.source.selectedtheme);
                           $http.patch(serverURL + '/AddEssaySentence', {"essaysentence": sentence, "selectedtheme": $scope.source.selectedtheme
                            }, {withCredentials: true, contentType : "application/json"})
                                // handle success
                                .success(function(data) {
                                  $scope.fileSuccess = true;
                                  $scope.fileError = false;
                                  $uibModalInstance.dismiss('AddEssaySentence');
                                  $scope.callbackFunction();
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
                              templateUrl: 'changeTheme.html',
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
          $scope.clickSentence = function(index, sentence, themeid){
              console.log('sentence', sentence);
              $scope.sentenceDialog(index, sentence, themeid);
          };

      }],
      template = '<span ng-click="clickSentence($index, sentence, tids[$index])" style="background-color: {{colors[$index]}};" title="{{ts[$index]}}" ng-repeat="sentence in sentences"> {{" "}} {{sentence}}</span>';
        return {
            restrict: 'EA',
            transclude: true,
            scope: {
                sentences: '=',
                thememarkers: '=',
                themes: '=',
                colors: '=',
                ts: '=',
                tids: '=',
                submissionname: '=',
                callbackFunction: '&'
            },
            controller: controller,
            template: template
        };
    });

/*
angular.module('conceptvectorApp')
    .directive('essayhighlight', function($compile, $uibModal) {
    var sentenceDialog =  function(value){
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
    };
        return {
            restrict: 'E',
            transclude: true,
            scope: {
                sentences: '=',
                themes: '=',
                colors: '=',
                ts: '='
            },
            link: function postLink(scope, element, attrs) {

                scope.launch = function(which){
                    var dlg = null;
                    sentenceDialog(which);
                  };
                console.log('sentences', scope.sentences);
                scope.$watch('sentences', function(sentences) {
                    if (sentences) {
                        var inputData = sentences.map(function(d, i) {
                            return { original: d, updated: d, theme: scope.themes[i], tsentence: scope.ts[i], color: scope.colors[i], isUpdated: false }
                        });
                        inputData.forEach(function(sentence) {
                             //background={{scope.theme_colors[sentence.theme]}}
                             //sentence.updated = '<span  tooltip-placement="top" uib-tooltip="''">' + sentence.original + '</span>';
                              sentence.updated = '<span ng-click= launch("value") style="background-color:' + sentence.color + ';"' + " title=" + '"' + sentence.tsentence +'"' + '>' + sentence.original + '</span>';
                              sentence.isUpdated = true;
                        });
                        var output = inputData.map(function(d) {
                            return d.updated;
                        }).join(" ");
                        element.html(output);
                        $compile(element.contents())(scope);
                    } else {
                    	element.html(" ");
                    	$compile(element.contents())(scope);
                    }
                });
            }
        };
    });
*/
