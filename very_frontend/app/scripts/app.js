'use strict';

angular.module('suchApp', ['ngCookies', 'ngResource', 'ngSanitize', 'ngRoute'])
  .constant('WOW', ['wow', 'very trade', 'many exchange', 'such DOGE', 'to the moon'])
  .config(function($routeProvider, $httpProvider, $locationProvider, STATIC_URL) {
    if (window.history && window.history.pushState){
      $locationProvider.html5Mode(true);
    }
    $routeProvider
      .when('/', {
        templateUrl: 'main.html',
        controller: 'MainCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
    $httpProvider.interceptors.push(function() {
      return {
        request: function(cfg) {
          // look for views in 'views/...'
          if (cfg.url.match(/\.html$/i)) {
            cfg.url =  STATIC_URL + 'views/' + cfg.url;
          }
          return cfg;
        }
      };
    });
  })
  .run(function ($http, $cookies, $rootScope) {
    // For CSRF token compatibility with Django
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    $rootScope.user = $rootScope.user || {
      isLogged: false,
      email: ''
    };
  });
