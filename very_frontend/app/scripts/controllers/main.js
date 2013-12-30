'use strict';

angular.module('suchApp')
  .controller('MainCtrl', function ($scope, WOW) {
    $scope.year = (new Date()).getFullYear();
    $scope.wow = WOW[Math.floor(Math.random() * WOW.length)];
  });
