'use strict';

angular.module('suchApp')
  .directive('orderList', function (STATIC_URL) {
    return {
      templateUrl: STATIC_URL + 'views/orderlist.html'
    };
  });
