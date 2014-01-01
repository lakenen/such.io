'use strict';

angular.module('suchApp')
  .controller('LoginCtrl', ['$scope', '$http', '$cookies', 'User', function ($scope, $http, $cookies, User) {
    $scope.loggedIn = false;
    $scope.user = User;
    $scope.showSignup = false;
    $scope.isLoading = false;
    $scope.login = function () {
      $scope.$broadcast('autofill:update');
      $scope.isLoading = true;
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
      $scope.isLoading = true;
      $http.post('/logout')
        .finally(function () {
          User.isLogged = false;
          $scope.isLoading = false;
          $scope.loginForm.$setPristine();
          $scope.showSignup = false;
        });
    };

    function loginSuccess(data, status, headers) {
      console.log(data);
      $scope.isLoading = false;
      User.isLogged = true;
      console.log(headers('Set-Cookie'));
      $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken = getCookie('csrftoken');
      delete User.password;
    }

    function loginFail(data, status) {
      console.log(data, status);
      $scope.isLoading = false;
      User.isLogged = false;
      $scope.error = 'Invalid email or password';
    }

    function signupSuccess(data) {
      console.log(data);
      $scope.isLoading = false;
      User.isLogged = true;
      delete User.password;
    }

    function signupFail(data, status) {
      console.log(data, status);
      $scope.isLoading = false;
      User.isLogged = false;
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
