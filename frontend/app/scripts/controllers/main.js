'use strict';

angular.module('suchio')
  .controller('MainCtrl', function ($scope) {
    $scope.year = (new Date()).getFullYear();
  });
