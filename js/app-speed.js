//constantes
const canvas = document.getElementById("Canvas");
const ctx = canvas.getContext("2d");
const Div = document.getElementById("canvas");
const G = 5; //constante gravitationnelle
const M = 500000;
const deg2rad = Math.PI / 180;
const offset = 20;

//Image Planete
let image_planete= document.getElementById("planete")
posPlanete = new Array(image_planete.style.left, image_planete.style.top);

//Image Satellite
let sat= document.getElementById("sat");
posSat = new Array(sat.style.left, sat.style.top);


//variables
let stop = 0;
let v0 = document.getElementById("vit").value; //vitesse initiale
let Sat=document.getElementById("Sat");
let btn = document.getElementById("btn");
btn.addEventListener('click',drawTrajectory);
reset.addEventListener('click',Reset);
let theta=270;
let delta_time = 2;

//paramètre de l'ellipse
let rho0 = document.getElementById("rho").value; //rayon initial
let C = rho0*v0;
let p = (rho0**2 * v0**2)/(G * M); //paramètre de l'ellipse
let e = p/rho0 - 1; //excentricité de l'ellipse
let rayon = p/(1 + e * Math.cos(theta * deg2rad + Math.PI/2));
console.log("rho0 : " + rho0 + "\n p : " + p + "\n e : " + e + "\n rayon : " + rayon);
//let demiGrandAxe = p/(1 - e**2)
//let demiPetitAxe = p/(Math.sqrt(1 - e**2))
let sat_x = cartesianX(rayon, theta);
let sat_y = cartesianY(rayon, theta);



//repositionnement de la planète et du satellite
function reposition() {
	image_planete.style.position = "relative";
	image_planete.style.left = (90 + canvas.width / 2) + "px";
	image_planete.style.top = (50 - canvas.height / 2) + "px";

	sat.style.position = "relative";
	sat_x = cartesianX(rayon, theta);
	sat_y = cartesianY(rayon, theta);
	sat.style.left = sat_x + (sat.width / 2 + 5 + canvas.width / 2) + "px";
	sat.style.top = sat_y - (-sat.height / 2 - 9 + canvas.height / 2) + "px";
	/*
	sat.style.left = sat_x + offset + (canvas.width/2 - sat.width/2) + "px";
	sat.style.top = sat_y + (canvas.height/2 - sat.height/2) + offset + "px";
	*/
}

reposition();
window.onresize = reposition;

//récupérer la distance entre le satellite et la planète
function getRadius() {
	posPlanete = new Array(parseFloat(image_planete.style.left), parseFloat(image_planete.style.top));
	posSat = new Array(parseFloat(sat.style.left), parseFloat(sat.style.top));
	return ((posSat[0]-posPlanete[0])**2+(posSat[1]-posPlanete[1])**2)**(1/2);
}
console.log("rayon : " + rayon)

//Lorsque le bouton "Lancer la simulation" est cliqué
function drawTrajectory() {
	ctx.beginPath();
	document.getElementById("vit").disabled = true;
	document.getElementById("rho").disabled = true;
	stop = 0;
	dessinTrajectoire();
}

function dessinTrajectoire() {
	if (stop == 0) {

		//fonctions à répéter

		//console.log("excentricité : " + e + " ; paramètre : " + p);
		console.log("rayon : " + rayon);
		rayon = p/(1 + e * Math.cos(theta * deg2rad + Math.PI/2));
		sat_x = cartesianX(rayon,theta);
		sat_y = cartesianY(rayon,theta);
		v0 = document.getElementById("vit").value;
		theta += C * delta_time/(rayon**2);
		//p = (rho0**2 * v0**2)/(G * M); //paramètre de l'ellipse
		//e = p/rho0 - 1; //excentricité de l'ellipse
		//let demiGrandAxe = p/(1 - e**2)
		//let demiPetitAxe = p/(Math.sqrt(1 - e**2))
		//let sat_x = demiGrandAxe * Math.cos(theta * deg2rad);
		//let sat_y = demiPetitAxe * Math.sin(theta * deg2rad);
		console.log(sat_x, sat_y);
		console.log(rayon);

		sat.style.left = sat_x + (sat.width / 2 + 5 + canvas.width / 2) + "px";
		sat.style.top = sat_y - (-sat.height / 2 - 9 + canvas.height / 2) + "px";
		ctx.lineTo(sat_x + (canvas.width/2 - sat.width/2) + sat.width/2,sat_y + (canvas.height/2 - sat.height/2) + sat.height/2);
		ctx.stroke();
		requestAnimationFrame(dessinTrajectoire);

		//condition de fin de boucle
		if (rayon <= 57) {
			stop = 1;
		}
		if (Math.abs(sat_y) > canvas.height/2) {
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
	theta = 270;
	rho0 = document.getElementById("rho").value; //rayon initial
	p = (rho0**2 * v0**2)/(G * M); //paramètre de l'ellipse
	e = p/rho0 - 1; //excentricité de l'ellipse
	rayon = p/(1 + e * Math.cos(theta * deg2rad + Math.PI/2));
	sat_x = cartesianX(rayon, theta);
	sat_y = cartesianY(rayon, theta);
	reposition();
	document.getElementById("vit").disabled = false;
	document.getElementById("rho").disabled = false;
}


function cartesianX(r, theta) {
    return (r * Math.cos(theta * deg2rad));
}

function cartesianY(r, theta) {
    return (r * Math.sin(theta * deg2rad));
}

function speedChange(v) {
	document.getElementById("vitesseLabel").innerHTML = "Vitesse : " + v + "m/s";
	v0 = v;
	p = (rho0**2 * v0**2)/(G * M); //paramètre de l'ellipse
	e = p/rho0 - 1; //excentricité de l'ellipse
	console.log(rho0, v0, p ,e);
}

function rhoChange(rho) {
	document.getElementById("rhoLabel").innerHTML = "Rayon initial : " + rho + "km";
	//reposition satellite
	sat.style.left = sat_x + (sat.width / 2 + 5 + canvas.width / 2) + "px";
	sat.style.top = parseFloat(image_planete.style.top) - parseFloat(rho) - sat.height / 2 - 5 + "px";

	rho0 = rho;
	p = (rho0**2 * v0**2)/(G * M); //paramètre de l'ellipse
	e = p/rho0 - 1; //excentricité de l'ellipse
	console.log(rho0, v0, p ,e);
}