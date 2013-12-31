'use strict';

angular.module('suchApp', ['ngCookies', 'ngResource', 'ngSanitize', 'ngRoute'])
  .constant('WOW', ['wow', 'very trade', 'many exchange', 'such DOGE', 'to the moon'])
  .config(function($routeProvider, $locationProvider, STATIC_URL) {
    if (window.history && window.history.pushState){
      $locationProvider.html5Mode(true);
    }
    $routeProvider
      .when('/', {
        templateUrl: STATIC_URL + 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/login', {
        templateUrl: STATIC_URL + 'views/login.html',
        controller: 'LoginCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
