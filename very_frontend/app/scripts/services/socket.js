'use strict';

angular.module('suchApp')
  .factory('socket', function ($rootScope, WS_URL) {
    var socket;
    socket = new WebSocket(WS_URL);
    // socket.addEventListener('error', handleError);
    // socket.addEventListener('close', handleClose);
    // socket.addEventListener('open', handleOpen);
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
        if (typeof data !== 'string') {
          data = JSON.stringify(data);
        }
        socket.send(data);
      }
    };
  });
