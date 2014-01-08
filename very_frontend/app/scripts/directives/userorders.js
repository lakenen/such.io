'use strict';

angular.module('suchApp')
  .directive('userOrders', function (UserOrder) {
    return {
      templateUrl: 'userorders.html',
      link: function ($scope) {
        function refresh() {
          $scope.orders = UserOrder.query();
        }
        $scope.$on('userorder:add', refresh);
        $scope.requestCancel = function (id) {
          UserOrder.cancel({ orderId: id })
            .$promise
            .then(function () {
              alert('cancel requested');
            })
            .catch(function (res) {
              alert(res.data.error);
            })
            .finally(function () {
              refresh();
            });
        };
        refresh();
      }
    };
  });
