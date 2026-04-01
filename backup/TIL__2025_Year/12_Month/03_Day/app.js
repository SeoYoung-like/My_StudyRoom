const h1 = document.querySelector(".title");

// function handlertitleClick(){
//   const clickClass = "clicked"
//   if (h1.className === clickClass){
//     h1.className = ""
//   } else {
//     h1.className = clickClass
//   }
// }

// function handlertitleClick(){
//   const clickClass = "clicked"
//   if (h1.classList.contains(clickClass)){
//     h1.classList.remove(clickClass);
//   } else {
//     h1.classList.add(clickClass);
//   }
// }

function handlertitleClick(){
  const clickClass = "clicked"
  h1.classList.toggle(clickClass);
}


h1.addEventListener("click", handlertitleClick);
