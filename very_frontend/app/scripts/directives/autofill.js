'use strict';

angular.module('suchApp')
  .directive('autofill', function () {
    return {
      require: 'ngModel',
      link: function ($scope, element, attrs, ngModel) {
        $scope.$on('autofill:update', function() {
          ngModel.$setViewValue(element.val());
        });
      }
    };
  });