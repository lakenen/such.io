'use strict';

angular.module('suchio')
  .controller('OrderListCtrl', ['$scope', 'OrderList', function ($scope, OrderList) {
    $scope.orders = OrderList.fetch('DOGE', 'BTC');
    $scope.market = {
      market: 'DOGE',
      base: 'BTC'
    };
  }]);

