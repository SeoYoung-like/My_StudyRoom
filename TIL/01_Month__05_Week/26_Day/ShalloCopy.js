var a = {
    name: "HI",
    age: 12,
}


function shalloCopy(target) {
    var result = {}
    if (typeof target === "object" && target !== null) {
        for (prop in target) {
            result[prop] = target[prop]
        }
    } else {
        result = target
    }

    return result
}