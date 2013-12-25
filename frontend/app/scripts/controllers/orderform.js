'use strict';

angular.module('suchApp')
  .controller('OrderFormCtrl', function ($scope, $rootScope, $filter) {
    var cryptoFilter = $filter('cryptoCurrency');
    var market = {
      market: 'DOGE',
      base: 'BTC',
      buyPrice: cryptoFilter(0.00000070),
      sellPrice: cryptoFilter(0.00000069),
    };
    var order = {
      action: 'Buy',
      quantity: 0,
      market: market.market,
      price: market.buyPrice,
      place: function () {
        console.log(this.quantity);
      }
    };

    $scope.updateQuantity = function () {
      var qty = parseFloat(order.quantity),
        price = parseFloat(order.price);
      qty = order.market === market.base ?
        qty * price :
        qty / price;
      order.quantity = cryptoFilter(qty);
    };
    $scope.market = market;
    $scope.order = order;
    $scope.txFee = $rootScope.txFee;
  });
