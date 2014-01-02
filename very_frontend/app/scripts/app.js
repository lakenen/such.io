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
  .run(function ($http, $cookies, $rootScope) {
    // For CSRF token compatibility with Django
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $rootScope.user = $rootScope.user || {
      isLogged: false,
      email: ''
    };
  });
