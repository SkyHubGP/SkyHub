let slideIndex = 0;

	showSlides();

	function showSlides() {
	  let i;
	  let slides1 = document.getElementsByClassName("mySlides1");
	  let slides2 = document.getElementsByClassName("mySlides2");
	  let dots1 = document.getElementsByClassName("dot1");
	  let dots2 = document.getElementsByClassName("dot2");

	  for (i = 0; i < slides1.length; i++) {
	    slides1[i].style.display = "none";
	    slides2[i].style.display = "none";
	  }
	  slideIndex++;
	  if (slideIndex > slides1.length) {slideIndex = 1}    
	  for (i = 0; i < dots1.length; i++) {
	    dots1[i].className = dots1[i].className.replace(" active", "");
	    dots2[i].className = dots2[i].className.replace(" active", "");
	  }
	  slides1[slideIndex-1].style.display = "block";
	  slides2[slideIndex-1].style.display = "block";
	  dots1[slideIndex-1].className += " active";
	  dots2[slideIndex-1].className += " active";
	  setTimeout(showSlides, 6000); // Change image every 2 seconds
}





