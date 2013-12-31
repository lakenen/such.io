'use strict';

angular.module('suchApp')
  .controller('LoginCtrl', function ($scope, $http) {
    $scope.loggedIn = false;
    $scope.user = {};
    $scope.showSignup = false;
    $scope.loading = false;
    $scope.login = function () {
      $scope.$broadcast('autofill:update');
      console.dir($scope.loginForm);
      // might have been autocompleted...
      if (!$scope.user.email || !$scope.user.password) {
        //$scope.user.email = $scope.loginForm.email;

      }
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
