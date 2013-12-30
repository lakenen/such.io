'use strict';

angular.module('suchApp')
  .controller('LoginCtrl', function ($scope) {
    $scope.loggedIn = false;
    $scope.user = {
      name: '',
      password: ''
    };
    $scope.login = function () {
      console.log($scope.user);
      $scope.loggedIn = true;
    };
    $scope.logout = function () {

    };
  });
