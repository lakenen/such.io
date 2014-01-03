'use strict';

angular.module('suchApp')
  .filter('cryptoCurrency', function () {
    return function (input, full) {
      var val = (parseFloat(input) || 0).toFixed(8);
      if (!full) {
        val = val.replace(/(\.0)0+$/, '$1');
      }
      return val;
    };
  });
