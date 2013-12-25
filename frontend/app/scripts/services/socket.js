'use strict';

angular.module('suchApp')
  .factory('socket', function ($rootScope) {
    var socket = new WebSocket($rootScope.wsUrl);
    return {
      on: function (eventName, callback) {
        socket.addEventListener(eventName, function () {
          var args = arguments;
          $rootScope.$apply(function () {
            callback.apply(socket, args);
          });
        });
      },
      send: function (data) {
        socket.send(data);
      }
    };
  });
