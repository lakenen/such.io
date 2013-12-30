'use strict';

angular.module('suchApp')
  .factory('OrderList', ['$resource', function ($resource) {
    return {
      fetch: function (market, base) {
        return $resource('/orders/:market/:base.json', {}, {
          query: {
            method:'GET',
            params: {
              market: market,
              base: base
            }
          }
        }).query();
      }
    };
  }]);
