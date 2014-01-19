'use strict';

angular.module('suchApp')
  .controller('MainCtrl', function ($scope, $rootScope, WOW) {
    $scope.wow = WOW[Math.floor(Math.random() * WOW.length)];
    function setTemplate() {
      $scope.mainTemplate = $rootScope.user.isLogged ?
        'logged-in.html' :
        'logged-out.html';
    }
    $rootScope.$on('auth:change', setTemplate);
    setTemplate();
  });
