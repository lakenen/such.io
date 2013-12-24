'use strict';

angular.module('suchio')
  .filter('cryptoCurrency', function () {
    return function (input) {
      return input.toFixed(8);
    };
  });
