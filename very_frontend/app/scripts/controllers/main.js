'use strict';

angular.module('suchApp')
  .controller('MainCtrl', function ($scope, WOW) {
    $scope.wow = WOW[Math.floor(Math.random() * WOW.length)];
  });
