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
              //console.log('controller themes', $scope.themes);
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
                        $scope.showRemove = function(){
                            //console.log('annotation data', $scope.annotation);
                            for( var i = 0; i < $scope.annotation.length; i++)
                                {
                                    //console.log('annotation index', i, $scope.assignmentid, $scope.submissionid, index);
                                    if ($scope.annotation[i]['assignment_id'] === $scope.assignmentid && $scope.annotation[i]['submissionID'] === $scope.submissionid && $scope.annotation[i]['sentenceIndex'] === index)
                                    {
                                       return true;
                                    }
                                 }
                            return false;
                        };
                        $scope.getAnnotationID = function(){
                            for( var i = 0; i < $scope.annotation.length; i++)
                                {
                                    if ($scope.annotation[i]['assignment_id'] === $scope.assignmentid && $scope.annotation[i]['submissionID'] === $scope.submissionid && $scope.annotation[i]['sentenceIndex'] === index)
                                    {
                                       return $scope.annotation[i]['id'];
                                    }
                                 }
                            return -1;
                        };
                        $scope.remove = function(){
                            console.log('here I am');
                            $http.get(serverURL + '/DeleteAnnotation/'+$scope.getAnnotationID(), {withCredentials: true, contentType : "application/json"})
                                // handle success
                                .success(function(data) {
                                  console.log('annotation delete success', data);
                                  for( var i = 0; i < $scope.annotation.length; i++)
                                  {
                                      if ( $scope.annotation[i]['id'] === data['id'])
                                      {
                                          $scope.annotation.splice(i, 1); //delete this annotation from scope
                                      }
                                   }
                                   console.log('success',$scope.annotation);
                                   $uibModalInstance.dismiss('remove');
                                })
                                // handle error
                                .error(function(data) {
                                  $scope.fileError = true;
                                  console.log('delete fail');
                                  $scope.fileSuccess = false;
                                });
                        };
                        $scope.save = function () {
                           console.log('selected theme', $scope.source.selectedtheme);
                           $http.post(serverURL + '/saveAnnotation', {"sentence": sentence,"submissionName": $scope.submissionname, "submissionID": $scope.submissionid, "sentenceIndex": index, "selectedTheme": $scope.source.selectedtheme, "assignment_id" : $scope.assignmentid, "annotatorID": $scope.userid,
                            "annotatorName": $scope.username}, {withCredentials: true, contentType : "application/json"})
                                // handle success
                                .success(function(data) {
                                  $scope.fileSuccess = true;
                                  console.log('annotation saved data', data);
                                  $scope.annotation.push(data);
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
              var color = "";
              angular.forEach($scope.annotation, function(x, key) {
                  //console.log($scope.assignmentID)
                 if(parseInt(x['assignment_id']) === $scope.assignmentid && parseInt(x['sentenceIndex']) === index && x['submissionID'] ===  $scope.submissionid)
                  {
                      //className = "highlightAnnotation";
                      angular.forEach($scope.themes, function(y,key){
                          if(y['id'] === x['selectedTheme']){
                              color = y['color']; //sentence theme color
                          }
                      });
                  }
              });
              return color;
          }


      }],
      //ng-class="getClass($index)"
      template = '<span  style="background-color:{{getClass($index)}};" ng-click="clickSentence($index, sentence)" ng-repeat="sentence in sentences">{{" "}} {{sentence}}</span>';
        return {
            restrict: 'EA',
            transclude: true,
            scope: {
                userid: '=',
                username: '=',
                sentences: '=',
                themes: '=',
                submissionname: '=',
                submissionid: '=',
                assignmentid: '=',
                annotation: '='
            },
            controller: controller,
            template: template
        };
    });
