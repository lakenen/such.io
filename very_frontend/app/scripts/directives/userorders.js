'use strict';

angular.module('suchApp')
  .directive('userOrders', function (UserOrder, STATIC_URL) {
    return {
      templateUrl: STATIC_URL + 'views/userorders.html',
      link: function ($scope) {
        function refresh() {
          $scope.orders = UserOrder.query();
        }
        $scope.$on('userorder:add', refresh);
        $scope.requestCancel = function (id) {
          UserOrder.cancel({ orderId: id }, refresh);
        };
        refresh();
      }
    };
  });
