'use strict';

angular.module('suchApp')
  .directive('orderForm', function (STATIC_URL) {
    return {
      templateUrl: STATIC_URL + 'views/orderform.html'
    };
  });
