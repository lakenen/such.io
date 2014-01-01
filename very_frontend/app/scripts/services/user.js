'use strict';

angular.module('suchApp')
  .factory('User', function() {
    return {
      isLogged: false,
      email: ''
    };
  });