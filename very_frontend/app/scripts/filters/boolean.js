'use strict';

/**
 * Boolean filter definittion
 */
angular.module('suchApp')
  .filter('boolean', function () {
    return function (input, truthyName, falsyName) {
      return (input ? (truthyName || true) : (falsyName || false)).toString();
    };
  });
