'use strict';

angular.module('suchApp')
  .directive('userOrders', function (UserOrders, STATIC_URL) {
    return {
      templateUrl: STATIC_URL + 'views/userorders.html',
      link: function (scope) {
        scope.orders = UserOrders.query();
      }
    };
  });
