let memoizee = require('memoizee');

export function cache() {
  return function (target: any, key: any, descriptor: any) {
    const oldFunction = descriptor.value;
    const newFunction = memoizee(oldFunction);
    descriptor.value = function () {
      return newFunction.apply(this, arguments);
    };
  };
}
