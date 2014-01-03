'use strict';

angular.module('suchApp')
  .factory('UserOrders', ['$resource', function ($resource) {
    return $resource('/api/orders', {}, {
      query: {
        method: 'GET',
        isArray: true
      }
    });
  }]);
