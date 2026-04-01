const clock = document.querySelector("h2#clock");
const body_element  = document.querySelector("body");

function sayHello() {
    console.log("hello");
}

function changeColor() {
    let randomColor = '#' + Math.floor(Math.random() * 16777215).toString(16);
    body_element.style.backgroundColor = randomColor;
}

function getClock(){
    const date = new Date();
    const date_hour = String(date.getHours()).padStart(2, "0");
    const date_minute = String(date.getMinutes()).padStart(2, "0");
    const date_second = String(date.getSeconds()).padStart(2, "0");
    clock.innerText = `${date_hour}:${date_minute}:${date_second}`;
}


// setInterval(changeColor, 1000

getClock();
setInterval(getClock, 1000);
// setInterval(changeColor, 1000);




// -------------------------------

// interval = 매번 일어나야 하는 무언가!
// setInterval(실행할 함수, 실행할 함수의 주기)!

// const date = new Date();
// clock.innerText = `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;

// const date = new Date();
// const date_hour = String(date.getHours()).padStart(2, "0");
// const date_minute = String(date.getMinutes()).padStart(2, "0");
// const date_second = String(date.getSeconds()).padStart(2, "0");
// clock.innerText = `${date_hour}:${date_minute;