'use strict';

describe('Controller: OrderFormCtrl', function () {

  // load the controller's module
  beforeEach(module('suchApp'));

  var OrderformCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    OrderformCtrl = $controller('OrderFormCtrl', {
      $scope: scope
    });
  }));

  it('should to the scope', function () {
    expect(scope);
  });
});
