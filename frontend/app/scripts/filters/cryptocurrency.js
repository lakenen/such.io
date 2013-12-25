'use strict';

angular.module('suchApp')
  .filter('cryptoCurrency', function () {
    return function (input) {
      return (parseFloat(input) || 0).toFixed(8).replace(/^([0-9]*)\.00+$/, '$1');
    };
  });
