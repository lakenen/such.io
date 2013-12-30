'use strict';

angular.module('suchApp')
  .controller('OrderFormCtrl', function ($scope, $rootScope, $filter) {
    var MAX_QUANTITY = 1e+8;
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

    $scope.increment = function (event) {
      var input = event.target,
        start = input.selectionStart,
        val = input.value,
        pos = start === val.length ? start - 1 : start,
        floatVal = parseFloat(val),
        num = parseInt(val[pos], 10),
        floatNum;

      console.dir(event);
      if (num > -1) {
        var v = val.replace(/\d/g, '0');
        v = v.substr(0, pos) + 1 + v.substr(pos + 1);
        console.log(v, pos, num);
        floatNum = parseFloat(v);

        switch (event.keyCode) {
          case 38: // UP
            console.log(floatVal, floatNum);
            input.value = cryptoFilter(Math.min(MAX_QUANTITY, floatVal + floatNum));
            input.selectionStart = input.selectionEnd = start;
            event.preventDefault();
            break;
          case 40: // DOWN
            input.value = cryptoFilter(Math.max(0, floatVal - floatNum));
            input.selectionStart = input.selectionEnd = start;
            event.preventDefault();
            break;
        }
      }
    };
  });