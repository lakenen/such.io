'use strict';

describe('Filter: cryptoCurrency', function () {

  // load the filter's module
  beforeEach(module('suchApp'));

  // initialize a new instance of the filter before each test
  var cryptoCurrency;
  beforeEach(inject(function ($filter) {
    cryptoCurrency = $filter('cryptoCurrency');
  }));

  it('should return the input fixed to 8 decimal places', function () {
    var input = 0.00001;
    expect(cryptoCurrency(input)).toBe('0.00001000');
  });

});
