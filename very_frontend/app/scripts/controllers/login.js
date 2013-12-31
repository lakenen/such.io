'use strict';

angular.module('suchApp')
  .controller('LoginCtrl', function ($scope, $http) {
    $scope.loggedIn = false;
    $scope.user = {};
    $scope.showSignup = false;
    $scope.loading = false;
    $scope.login = function () {
      $scope.loading = true;
      $http.post('/login', $scope.user)
        .success(loginSuccess)
        .error(loginFail);
    };
    $scope.signup = function () {
      $http.post('/signup', $scope.user)
        .success(signupSuccess)
        .error(signupFail);
    };
    $scope.logout = function () {
      $scope.loginForm.$setPristine();
      $scope.loggedIn = false;
      $scope.showSignup = false;
      $scope.user = {};
    };

    function loginSuccess(data) {
      console.log(data);
      $scope.loading = false;
      $scope.loggedIn = true;
    }

    function loginFail(data, status) {
      console.log(data, status);
      $scope.loading = false;
      $scope.loggedIn = false;
      $scope.error = 'Invalid email or password';
    }

    function signupSuccess(data) {
      console.log(data);
      $scope.loading = false;
      $scope.loggedIn = true;
    }

    function signupFail(data, status) {
      console.log(data, status);
      $scope.loading = false;
      $scope.loggedIn = false;
      $scope.error = 'Invalid email or password';
    }
  });
