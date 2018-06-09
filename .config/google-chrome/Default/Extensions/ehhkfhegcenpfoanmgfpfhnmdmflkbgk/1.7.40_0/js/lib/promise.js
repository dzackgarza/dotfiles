(() => { // make sure arrow functions work

// Promises are started in parallel.
// Resolves with the first resolved value in time. 
// If there's no winner, it rejects with last rejection.
Promise.any = function (promises) {
  return new Promise((resolve, reject) => {
    var rejectedCount = 0;
    function onMemberResolved(value) {
      resolve(value);
    }
    function onMemberRejected(reason) {
      if (++rejectedCount == promises.length)
        reject(reason);
    }
    function observeSettled(promise) { 
      promise.then(onMemberResolved)
             .catch(onMemberRejected);
    }
    promises.forEach(observeSettled);
  });
};
Promise.fastest = Promise.any;

// Promises are started in parallel.
// Resolves with the first resolved value in array order.
// If there's no winner, it rejects with last rejection.
Promise.preferred = function (promisesOrdered) {
  return new Promise((resolve, reject) => {
    var resolvedValues = new WeakMap();
    var resolvables = promisesOrdered.slice(); // copy
    function onMemberResolved(value, member) {
      resolvedValues.set(member, value);
      if (member == resolvables[0])
        resolve(value);
    }
    function onMemberRejected(reason, member) {
      resolvables.splice(resolvables.indexOf(member), 1);
      var firstValue = resolvedValues.get(resolvables[0]);
      if (firstValue)
        resolve(firstValue)
      else if (!resolvables.length)
        reject(reason);
    }
    function observeSettled(promise) { 
      promise.then(v => onMemberResolved(v, promise))
             .catch(r => onMemberRejected(r, promise));
    }
    promisesOrdered.forEach(observeSettled);
  });
};
Promise.firstInOrder = Promise.preferred;

})();