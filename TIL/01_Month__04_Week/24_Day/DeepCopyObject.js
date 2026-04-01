var user = {
    name: 'Jaenam',
    urls: {
      portfolio: 'http://github.com/abc',
      blog: 'http://blog.com/abc',
      facebook: 'http://facebook.com/abc'
    }
  };

var DeepCopyObject = function(target) {
    var result = {};

    if (typeof target === "object" && target != null) {
        for (var prop in target){
            result[prop] = DeepCopyObject(target[prop])
        }
    } else {
        result = target;
    }

    return result;
}