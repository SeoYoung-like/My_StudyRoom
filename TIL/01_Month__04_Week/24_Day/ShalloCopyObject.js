var user = {
    name: 'Jaenam',
    gender: 'male'
};

var ShallCopyObject = function(target) {
    result = {};
    for (var prop in target) {
        result[prop] = target[prop];
    }
    return result;
}