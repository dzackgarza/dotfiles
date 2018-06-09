
var resolveIn500 = new Promise((resolve, _) =>
  setTimeout(_ => resolve('resolveIn500'), 500));
var resolveIn700 = new Promise((resolve, _) =>
  setTimeout(_ => resolve('resolveIn700'), 700));
var resolveIn1000 = new Promise((resolve, _) =>
  setTimeout(_ => resolve('resolveIn1000'), 1000));

var rejectIn200 = new Promise((_, reject) =>
  setTimeout(_ => reject('rejectIn200'), 200));
var rejectIn300 = new Promise((_, reject) =>
  setTimeout(_ => reject('rejectIn300'), 300));
var rejectIn1600 = new Promise((_, reject) =>
  setTimeout(_ => reject('rejectIn1600'), 1600));

Promise.any([rejectIn200, rejectIn300, rejectIn1600,
             resolveIn500, resolveIn700, resolveIn1000])
       .then(maybe  => console.log('should be resolveIn500', maybe))
       .catch(wrong => console.error('shouldnt happen', wrong));

Promise.any([rejectIn1600, rejectIn200, rejectIn300])
       .then(wrong  => console.error('shouldnt happen', wrong))
       .catch(maybe => console.log('should be rejectIn1600', maybe));  

Promise.preferred([rejectIn200, rejectIn300, resolveIn700,
                   rejectIn1600, resolveIn500, resolveIn1000])
       .then(maybe  => console.log('should be resolveIn700', maybe))
       .catch(wrong => console.error('shouldnt happen', wrong));

Promise.preferred([resolveIn1000, rejectIn200, rejectIn300, 
                   resolveIn700, rejectIn1600, resolveIn500])
       .then(maybe  => console.log('should be resolveIn1000', maybe))
       .catch(wrong => console.error('shouldnt happen', wrong));

Promise.preferred([rejectIn1600, rejectIn200, rejectIn300])
       .then(wrong  => console.error('shouldnt happen', wrong))
       .catch(maybe => console.log('should be rejectIn1600', maybe));  
