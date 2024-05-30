import 'queue-microtask';

// Mock the queueMicrotask function globally
global.queueMicrotask = global.queueMicrotask || function (callback) {
  Promise.resolve().then(callback).catch(e => setTimeout(() => { throw e; }));
};
