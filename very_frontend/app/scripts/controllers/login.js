'use strict';

angular.module('suchApp')
  .controller('LoginCtrl', ['$scope', '$rootScope', '$http', '$cookies', function ($scope, $rootScope, $http, $cookies) {
    var user = $rootScope.user;

    $scope.showSignup = false;
    $scope.isLoading = false;
    $scope.login = function () {
      $scope.$broadcast('autofill:update');
      $scope.isLoading = true;
      $http.post('/login', user)
        .success(loginSuccess)
        .error(loginFail);
    };
    $scope.signup = function () {
      $http.post('/signup', user)
        .success(signupSuccess)
        .error(signupFail);
    };
    $scope.logout = function () {
      $scope.isLoading = true;
      $http.post('/logout')
        .finally(function () {
          user.isLogged = false;
          $scope.isLoading = false;
          $scope.loginForm.$setPristine();
          $scope.showSignup = false;
        });
    };

    function loginSuccess() {
      $scope.isLoading = false;
      user.isLogged = true;
      // update the csrftoken
      $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken = getCookie('csrftoken');
      delete user.password;
    }

    function loginFail() {
      $scope.isLoading = false;
      user.isLogged = false;
      $scope.error = 'Invalid email or password';
    }

    function signupSuccess() {
      $scope.isLoading = false;
      user.isLogged = true;
      delete user.password;
    }

    function signupFail() {
      $scope.isLoading = false;
      user.isLogged = false;
      $scope.error = 'Invalid email or password';
    }

    function getCookie(name) {
      var value = '; ' + document.cookie;
      var parts = value.split('; ' + name + '=');
      if (parts.length === 2) {
        return parts.pop().split(';').shift();
      }
    }
  }]);
