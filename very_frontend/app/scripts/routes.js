'use strict';

angular.module('suchApp')
  .config(function($routeProvider, $locationProvider) {
    if (window.history && window.history.pushState){
      $locationProvider.html5Mode(true);
    }
    $routeProvider
      .when('/', {
        templateUrl: 'main.html',
        controller: 'MainCtrl'
      })
      .when('/market/:marketId', {
        templateUrl: 'main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });