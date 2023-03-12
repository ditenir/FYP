const dropdown = document.getElementById("myDropdown");
const dropdownContents = document.querySelectorAll(".dropdown-content");

dropdown.addEventListener("change", function() {
  for (let i = 0; i < dropdownContents.length; i++) {
    dropdownContents[i].style.display = "none";
  }

  const selectedOption = document.getElementById(this.value + "Content");
  selectedOption.style.display = "block";
});


function changeDivs() {
  var ponctual = document.getElementById("ponctual");
  var ponctualReverse = document.getElementById("ponctualReverse");
  var togglePonctual = document.getElementById("togglePonctual");

  if (ponctualReverse.style.display == "none") {
    ponctual.style.display = "none";
    ponctualReverse.style.display = "block";
    togglePonctual.innerHTML = "Want to calculate the number of staff required to reach an agreed service level?";
  }

  else {
    ponctualReverse.style.display = "none";
    ponctual.style.display = "block";
    togglePonctual.innerHTML = "Want to calculate the number of calls with the current service level?";

  }
}


const periodTypeDropdown = document.getElementById("periodTypeDropdown");
const selectedType = periodTypeDropdown.options[periodTypeDropdown].value;

periodTypeDropdown.addEventListener("change", function() {
  const selectedType = periodTypeDropdown.options[periodTypeDropdown].value;
  console.log(selectedType);
});
