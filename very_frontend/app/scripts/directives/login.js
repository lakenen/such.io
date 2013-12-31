'use strict';

angular.module('suchApp')
  .directive('login', function (STATIC_URL) {
    return {
      templateUrl: STATIC_URL + 'views/login.html'
    };
  });
