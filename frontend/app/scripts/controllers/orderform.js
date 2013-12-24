'use strict';

angular.module('suchio')
  .controller('OrderFormCtrl', ['$scope', '$filter', function ($scope, $filter) {
    $scope.market = {
      market: 'DOGE',
      base: 'BTC',
      price: $filter('number')(0.000000791, 8)
    };
    $scope.order = {
      action: 'Buy',
      quantity: 0,
      market: $scope.market.market,
      price: $scope.market.price,
      place: function () {
        console.log(this.quantity);
      }
    };
  }]);
