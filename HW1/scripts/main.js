const myImage = document.querySelector("img");

let myButton = document.querySelector("button");

myButton.onclick = () => {
  const mySrc = myImage.getAttribute("src");
  if (mySrc === "images/countries.png") {
    myImage.setAttribute("src", "images/states.png");
	myButton.textContent = 'show countries';
  } else {
    myImage.setAttribute("src", "images/countries.png");
	myButton.textContent = 'show US states';
  }
};

myImage.addEventListener("click", function () {
  alert("secret message under construction");
});
