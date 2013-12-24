'use strict';

describe('Directive: orderform', function () {

  // load the directive's module
  beforeEach(module('suchioApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<orderform></orderform>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the orderform directive');
  }));
});
