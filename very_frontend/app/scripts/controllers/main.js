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
  })
  .controller('APITestCtrl', function ($scope, $http) {
    $scope.url = '';
    $scope.method = 'GET';
    $scope.data = '';
    $scope.submit = function () {
      $http({
        url: $scope.url,
        method: $scope.method,
        data: $scope.data
      }).success(function (e) {
        $scope.response = e;
      }).error(function (e, s) {
        $scope.response = s;
      });
    };
  });
