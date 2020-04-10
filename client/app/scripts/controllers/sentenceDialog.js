'use strict';

angular.module('conceptvectorApp')
  .controller('sentenceDialogCtrl', function($scope, $uibModalInstance, value) {

  //$scope.conceptName = conceptName;

  $scope.ok = function () {
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});
