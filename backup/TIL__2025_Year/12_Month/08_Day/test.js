// 1.
function func() {
    console.log("hello");
}
setTimeout(func, 3500);


// 2.
const intervalID = setInterval(() => {
    console.log("2초마다 실행됩니다.");
}, 2000);
setTimeout(() => {
    clearInterval(intervalID);
}, 5000);


// 3.
const callback = () => {
    console.log("hello");
    setTimeout(callback, 1000);
};

setTimeout(callback, 1000);