//constantes
const canvas = document.getElementById("Canvas");
const ctx = canvas.getContext("2d");
const Div = document.getElementById("canvas");
const G = 5; //constante gravitationnelle
const M = 500000;
const deg2rad = Math.PI / 180;
const offset = 20;
//variables
let stop = 0;
let v0 = 160; //vitesse initiale
let Sat=document.getElementById("Sat");
let btn = document.getElementById("btn");
btn.addEventListener('click',drawTrajectory);
reset.addEventListener('click',Reset);
let theta=0;
let delta_time=1;
//Image Planete
let image_planete= document.getElementById("planete");
posPlanete = new Array(image_planete.style.left, image_planete.style.top);

//Image Satellite
let sat = document.getElementById("sat");
sat.classList.add("sat");
posSat = new Array(sat.style.left, sat.style.top);


//paramètre de l'ellipse

let p = document.getElementById("p").value
let e = document.getElementById("e").value
let rho0 = getRadius(); //rayon initial
let rayon = p/(1 + e * Math.cos(theta * deg2rad));
let C = rho0*v0
//let demiGrandAxe = p/(1 - e**2)
//let demiPetitAxe = p/(Math.sqrt(1 - e**2))
let sat_x = cartesianX(rho0 + 60, theta);
let sat_y = cartesianY(rho0 + 60, theta);



//repositionnement de la planète et du satellite
function reposition() {
	let x_canvas = canvas.width;
	let y_canvas = canvas.height;


	image_planete.style.position = "relative";
	image_planete.style.left = (90 + canvas.width / 2) + "px";
	image_planete.style.top = (50 - canvas.height / 2) - 20 + "px";
	
	sat.style.position = "relative";
	sat_x = cartesianX(rho0 + 60,theta);
	sat_y = cartesianY(rho0 + 60,theta);
	sat.style.left = sat_x + (sat.width / 2 + 5 + canvas.width / 2) + "px";
	sat.style.top = sat_y - (-sat.height + 5 + canvas.height / 2) - 20 + "px";
}

reposition();
window.onresize = reposition;

//récupérer la distance entre le satellite et la planète
function getRadius() {
	p = document.getElementById("p").value;
	e = document.getElementById("e").value;
	return p/(1 + e * Math.cos(theta * deg2rad));
}


//Lorsque le bouton "Lancer la simulation" est cliqué
function drawTrajectory() {
	stop = 0;
	document.getElementById("p").disabled = true;
	document.getElementById("e").disabled = true;
	ctx.beginPath();
	dessinTrajectoire();
}

function dessinTrajectoire() {
	if (stop == 0) {

		//fonctions à répéter

		//console.log("excentricité : " + e + " ; paramètre : " + p);
		theta += C * delta_time/(rayon**2);
		//console.log("rayon : " + rayon);
		//console.log("theta : " + theta);
		rayon = p/(1 + e * Math.cos(theta * deg2rad));
		sat_x = cartesianX(rayon + 60,theta);
		sat_y = cartesianY(rayon + 60,theta);
		//p = (rho0**2 * v0**2)/(G * M); //paramètre de l'ellipse
		//e = p/rho0 - 1; //excentricité de l'ellipse
		//let demiGrandAxe = p/(1 - e**2)
		//let demiPetitAxe = p/(Math.sqrt(1 - e**2))
		//let sat_x = demiGrandAxe * Math.cos(theta * deg2rad);
		//let sat_y = demiPetitAxe * Math.sin(theta * deg2rad);
		
		sat.style.left = sat_x + (sat.width / 2 + 5 + canvas.width / 2) + "px";
		sat.style.top = sat_y - (-sat.height + 5 + canvas.height / 2) - 20 + "px";
		ctx.lineTo(sat_x + (canvas.width/2 - sat.width/2) + sat.width/2,sat_y + (canvas.height/2 - sat.height/2) + sat.height/2 -22);
		ctx.stroke();
		requestAnimationFrame(dessinTrajectoire);

		//condition de fin de boucle
		if (rayon <= 0) {
			stop = 1;
		}
		if (Math.abs(rayon) >= 3000) {
			stop = 1;
		}
		if (Math.abs(sat_y) > canvas.height/2 + 20) {
			sat.style.opacity = "0";
		}
		else {
			sat.style.opacity = "1";
		}
		if (Math.abs(sat_x) > canvas.width/2) {
			sat.style.opacity = "0";
		}
	}
}


function Reset() {
	ctx.clearRect(0,0,canvas.width,canvas.height);
	sat.style.opacity = "1";
	stop = 1;
	theta = 0;
	reposition();
	document.getElementById("p").disabled = false;
	document.getElementById("e").disabled = false;
}


function cartesianX(r, theta) {
    return (r * Math.cos(theta * deg2rad));
}

function cartesianY(r, theta) {
    return (r * Math.sin(theta * deg2rad));
}

function pChange(p) {
	document.getElementById("pLabel").innerHTML = "Parametre: " + p ;	
	 
	e = p/rho0 - 1; //excentricité de l'ellipse
	rho0 = getRadius();
	reposition();
}
function eChange(e) {
	document.getElementById("eLabel").innerHTML = "Exentricité : " + e;

	p = (rho0**2 * v0**2)/(G * M);
	rho0 = getRadius();
	reposition();
}
