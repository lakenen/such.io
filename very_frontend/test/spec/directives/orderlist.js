'use strict';

describe('Directive: orderList', function () {

  // load the directive's module
  beforeEach(module('suchApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<div order-list></div>');
    element = $compile(element)(scope);
    expect(element);
  }));
});
