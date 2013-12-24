'use strict';

describe('Controller: OrderformCtrl', function () {

  // load the controller's module
  beforeEach(module('suchioApp'));

  var OrderformCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    OrderformCtrl = $controller('OrderformCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
