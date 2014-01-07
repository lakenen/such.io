'use strict';

angular.module('suchApp')
  .factory('UserOrder', ['$resource', function ($resource) {
    return $resource('/api/orders/:orderId', { orderId: '@id' }, {
      get: { method: 'GET' },
      query: { method: 'GET', isArray: true },
      cancel: { method: 'DELETE' }
    });
  }]);
