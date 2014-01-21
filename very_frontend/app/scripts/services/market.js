'use strict';

angular.module('suchApp')
  .factory('Market', ['$http', '$resource', '$filter', function ($http, $resource, $filter) {
    var cryptoFilter = $filter('cryptoCurrency');
    return $resource('/api/markets/:marketId', { marketId: '@id' }, {
      get: {
        method: 'GET',
        transformResponse: $http.defaults.transformResponse.concat([
          function (response) {
            var buyOrders = response.aggregated_open_orders.buy,
              sellOrders = response.aggregated_open_orders.sell;
            return {
              market: response.market_currency.symbol,
              base: response.base_currency.symbol,
              buyRate: sellOrders.length && cryptoFilter(sellOrders[0].rate),
              sellRate: buyOrders.length && cryptoFilter(buyOrders[0].rate)
            };
          }
        ])
      },
      query: { method: 'GET', isArray: true }
    });
  }]);
