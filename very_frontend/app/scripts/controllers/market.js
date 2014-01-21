'use strict';

angular.module('suchApp')
  .controller('MarketCtrl', function ($scope, $rootScope, $route, Market) {
    if ($route.current.params.marketId) {
      $rootScope.market = Market.get({ marketId: $route.current.params.marketId }, function () {

      });
    } else {
      $scope.markets = Market.query();
    }
  });