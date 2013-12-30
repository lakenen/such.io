'use strict';

describe('Service: orderList', function () {

  // load the service's module
  beforeEach(module('suchApp'));

  // instantiate service
  var orderList;
  beforeEach(inject(function (OrderList) {
    orderList = OrderList;
  }));

  it('should do something', function () {
    expect(true);
  });

});
