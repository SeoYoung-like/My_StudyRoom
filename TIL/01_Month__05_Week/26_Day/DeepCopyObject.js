var a = {
    name: "HI",
    etc: {
        go: "hihi",
        age: 12,
        sex: [1, 2, 3, 4]
    }    
}


function DeepCopy(target) {
    var result = {};
    if (typeof target === "object" && target !== null) {
        for (prop in target) {
            result[prop] = DeepCopy(target[prop]);
        }
    } else {
        result = target;
    }

    return result;
}

