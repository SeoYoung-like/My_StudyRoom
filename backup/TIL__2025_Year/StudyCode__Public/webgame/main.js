const number = parseInt(prompt("참가자는 몇명인가요?"));

const $input = document.querySelector("#text");
const $button = document.querySelector("button");
let newWord  = "";

const onInputHandler = (event) => {
    newWord = $input.value;    
}