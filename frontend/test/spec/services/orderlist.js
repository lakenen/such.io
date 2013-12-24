'use strict';

describe('Service: orderList', function () {

  // load the service's module
  beforeEach(module('suchioApp'));

  // instantiate service
  var orderList;
  beforeEach(inject(function (_orderList_) {
    orderList = _orderList_;
  }));

  it('should do something', function () {
    expect(!!orderList).toBe(true);
  });

});
