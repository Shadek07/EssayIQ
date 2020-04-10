'use strict';

/*angular.module('conceptvectorApp')
  .controller('annotatesentenceDialogCtrl' ,function($scope, $uibModalInstance) {
  $scope.ok = function (value) {
    console.log(value);
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});*/
angular.module('conceptvectorApp').controller('annotatesentenceDialogCtrl', function (data) {
  var pc = this;
  pc.data = data;
  console.log('pc.data value', pc.data)
  pc.ok = function () {
    //{...}
    alert("You clicked the ok button.");
    //$uibModalInstance.close();
  };

  pc.cancel = function () {
    //{...}
    alert("You clicked the cancel button.");
    //$uibModalInstance.dismiss('cancel');
  };
});
