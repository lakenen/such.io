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
      .otherwise({
        redirectTo: '/'
      });
  })
  // .factory('myHttpInterceptor', function() {
  //   return {
  //     // optional method
  //     request: function(cfg) {
  //       // do something on success
  //       console.log(cfg);
  //       return cfg;
  //     }
  //   };
  // })
  .run(function ($http, $cookies, $rootScope) {
    // For CSRF token compatibility with Django
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    // $http.interceptors = [];
    // $http.interceptors.push('myHttpInterceptor');
    $rootScope.user = $rootScope.user || {
      isLogged: false,
      email: ''
    };
  });
