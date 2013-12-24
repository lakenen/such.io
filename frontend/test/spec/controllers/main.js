'use strict';

describe('Controller: MainCtrl', function () {

  // load the controller's module
  beforeEach(module('suchio'));

  var MainCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MainCtrl = $controller('MainCtrl', {
      $scope: scope
    });
  }));

  it('should attach orders and market objects to the scope', function () {
    expect(scope.orders);
  });
});
