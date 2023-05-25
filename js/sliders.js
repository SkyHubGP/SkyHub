let slideIndex = 0;

	showSlides();

	function showSlides() {
	  let i;
	  let slides1 = document.getElementsByClassName("mySlides1");
	  let slides2 = document.getElementsByClassName("mySlides2");
	  let slides3 = document.getElementsByClassName("mySlides3");
	  let slides4 = document.getElementsByClassName("mySlides4");
	  let slides5 = document.getElementsByClassName("mySlides5");
	  let dots1 = document.getElementsByClassName("dot1");
	  let dots2 = document.getElementsByClassName("dot2");
	  let dots3 = document.getElementsByClassName("dot3");
	  let dots4 = document.getElementsByClassName("dot4");
	  let dots5 = document.getElementsByClassName("dot5");

	  for (i = 0; i < slides1.length; i++) {
	    slides1[i].style.display = "none";
	    slides2[i].style.display = "none";
	    slides3[i].style.display = "none";
	    slides4[i].style.display = "none";
	    slides5[i].style.display = "none";
	  }
	  slideIndex++;
	  if (slideIndex > slides1.length) {slideIndex = 1}    
	  for (i = 0; i < dots1.length; i++) {
	    dots1[i].className = dots1[i].className.replace(" active", "");
	    dots2[i].className = dots2[i].className.replace(" active", "");
	    dots3[i].className = dots3[i].className.replace(" active", "");
	    dots4[i].className = dots4[i].className.replace(" active", "");
	    dots5[i].className = dots5[i].className.replace(" active", "");
	  }
	  slides1[slideIndex-1].style.display = "block";
	  slides2[slideIndex-1].style.display = "block";
	  slides3[slideIndex-1].style.display = "block";
	  slides4[slideIndex-1].style.display = "block";
	  slides5[slideIndex-1].style.display = "block";
	  
	  dots1[slideIndex-1].className += " active";
	  dots2[slideIndex-1].className += " active";
	  dots3[slideIndex-1].className += " active";
	  dots4[slideIndex-1].className += " active";
	  dots5[slideIndex-1].className += " active";
	  setTimeout(showSlides, 6000); // Change image every 6 seconds
}





