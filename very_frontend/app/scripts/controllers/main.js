'use strict';

angular.module('suchApp')
  .controller('MainCtrl', function ($scope, $rootScope, WOW, STATIC_URL) {
    $scope.wow = WOW[Math.floor(Math.random() * WOW.length)];
    function setTemplate() {
      $scope.mainTemplate = $rootScope.user.isLogged ?
        STATIC_URL + 'views/logged-in.html' :
        STATIC_URL + 'views/logged-out.html';
    }
    $rootScope.$on('auth:change', setTemplate);
    setTemplate();
  });
