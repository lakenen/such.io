'use strict';

/**
 * Capitalize filter definittion
 */
angular.module('suchApp')
  .filter('capitalize', function () {
    /**
     * Capitalize the first letter of the given string
     * @param   {string} str The string
     * @returns {string}     The string with the first letter capitalized
     */
    function capitalize(str) {
      return str.charAt(0).toUpperCase() + str.substr(1);
    }
    return function (input, allWords) {
      if (allWords) {
        return input.split(' ').map(capitalize).join(' ');
      }
      return capitalize(input);
    };
  });
