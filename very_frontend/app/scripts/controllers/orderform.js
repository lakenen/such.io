'use strict';

angular.module('suchApp')
  .controller('OrderFormCtrl', function ($scope, $rootScope, $filter, UserOrder) {
    var MAX_QUANTITY = 1e+8;
    var cryptoFilter = $filter('cryptoCurrency');
    var market = {
      market: 'DOGE',
      base: 'BTC',
      buyRate: cryptoFilter(0.00000070),
      sellRate: cryptoFilter(0.00000069),
    };
    var order = {
      type: 'buy',
      quantity: cryptoFilter(0),
      market: market.market,
      rate: market.buyRate
    };

    $scope.market = market;
    $scope.order = order;
    $scope.txFee = $rootScope.txFee;
    $scope.showRequired = true;

    $scope.placeOrder = function () {
      var quantity = order.quantity;
      if (order.market === market.base) {
        quantity /= order.rate;
      }
      var o = new UserOrder({
        type: order.type,
        amount: quantity,
        rate: order.rate,
        market: 1
      });
      o.$save(saveSuccess, saveFail);
    };

    function saveSuccess(response) {
      $rootScope.$broadcast('userorder:add', response);
      $scope.order.quantity = cryptoFilter(0);
      console.log('order placed!', response);
    }

    function saveFail(response) {
      console.error('order failed', response.data);
      if (response.data.non_field_errors) {
        response.data.non_field_errors.forEach(alert);
      } else {
        for (var p in response.data) {
          response.data[p].forEach(alert);
        }
      }
    }

    $scope.updateQuantity = function () {
      var qty = parseFloat(order.quantity),
        rate = parseFloat(order.rate);
      qty = order.market === market.base ?
        qty * rate :
        qty / rate;
      order.quantity = cryptoFilter(qty);
      updateInfo();
    };

    function updateInfo() {
      if (order.market === market.market) {
        $scope.showRequired = order.type === 'buy';
      } else {
        $scope.showRequired = order.type === 'sell';
      }
    }

    $scope.setType = function (type) {
      order.type = type;
      updateInfo();
    };

    $scope.increment = function (event) {
      var input = event.target,
        start = input.selectionStart,
        val = input.value,
        pos = start === val.length ? start - 1 : start,
        floatVal = parseFloat(val),
        num = parseInt(val[pos], 10),
        floatNum;

      //console.dir(event);
      if (num > -1) {
        var v = val.replace(/\d/g, '0');
        v = v.substr(0, pos) + 1 + v.substr(pos + 1);
        floatNum = parseFloat(v);

        switch (event.keyCode) {
          case 38: // UP
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
