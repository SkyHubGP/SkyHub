//constantes
const canvas = document.getElementById("Canvas");
const ctx = canvas.getContext("2d");
const Div = document.getElementById("canvas");
const g = 9.81;
const deg2rad = Math.PI / 180;

//variables
let angle = 45; //angle de départ
let k = 1.2; //coefficient de frottements de l'air
let X = new Array();
let Y = new Array();
let stop = 0;
let x = 0;
let y = 0;
let v0 = document.getElementById("vit").value; //vitesse initiale
let m = document.getElementById("poids").value; //masse d'un boulet de canon en kg
let n=0; //numéro du tracé
let trace = document.getElementById("trace");
let erase = document.getElementById("reset");
erase.addEventListener("click",eraseTrajectory);

let btn = document.getElementById("btn");
btn.addEventListener('click',drawTrajectory);

let cb = document.getElementById("frott");

//changement d'origine pour être au bout du canon
ctx.save(); //sauvegarde des paramètres de base
ctx.translate(40*Math.cos(angle*deg2rad) + 42,-40*Math.sin(angle*deg2rad) + canvas.offsetHeight - 47);


//Image Canon
let image_canon = document.getElementById("canon");

image_canon.classList.add("Canon");
image_canon.style.transform = "rotate(-15deg)";


//repositionnage du canon
function reposition() {
  let x_canvas = canvas.offsetLeft;
  let y_canvas = canvas.offsetTop;

  image_canon.style.position = "relative";
  image_canon.style.left = image_canon.width + "px";
  image_canon.style.top = 0 + "px";
}
reposition();
window.onresize = reposition;

//tourner le canon
function rotate(téta) {
	ctx.restore();
	ctx.save();

	document.getElementById("angleLabel").innerHTML = "Angle : " + Math.abs(téta - 90) + "°";
	image_canon.style.transform = "rotate(" + (téta - 60) + "deg)";
	angle = Math.abs(téta-90);

	ctx.translate(40*Math.cos(angle*deg2rad) + 42,-40*Math.sin(angle*deg2rad) + canvas.offsetHeight - 47);
}


//Lorsque le bouton "Lancer la simulation" est cliqué
function drawTrajectory() {
	X = new Array();
	Y = new Array();
	m = document.getElementById("poids").value;
	v0 = document.getElementById("vit").value;
	x = 0;
	y = 0;
	//désactive le curseur du choix d'angle durant le tracé
	document.getElementById("angle").disabled = true;

	ctx.beginPath();

	if (!cb.checked){ //sans frottement
		k = 0;
		dessinTrajectoire();
	}
	else { //frottements laminaires
		k = 1.2;
		dessinTrajectoire();
	}
}


//effacer les tracés
function eraseTrajectory(){
	//efface les tracés sur le canvas
	ctx.restore();
	ctx.save();
	ctx.clearRect(0,0,canvas.width,canvas.height);
	ctx.translate(40*Math.cos(angle*deg2rad) + 42,-40*Math.sin(angle*deg2rad) + canvas.offsetHeight - 47);
}


function dessinTrajectoire() {
	if (stop == 0) {

		//fonctions à répéter

		if (k == 0) { //sans frottement
			ctx.moveTo(Math.abs(x), y);
			x += 3;
			if (y == 90) {

			} else {
				y = (g * x ** 2) / (v0 * Math.cos(angle * deg2rad)) ** 2 - (v0 * Math.sin(angle * deg2rad) * x) / (v0 * Math.cos(angle * deg2rad));
			}
			ctx.lineTo(Math.abs(x), y);
			ctx.stroke();

		} else { //avec frottements
			ctx.moveTo(Math.abs(x), y);
			x += 3;
			a = ((m/k) * (v0 * Math.sin(angle * deg2rad) + (m * g)/k));
			y = a * ((x - m/k * v0 *
			Math.cos(angle * deg2rad))/(- m/k * v0 * Math.cos(angle * deg2rad))) - (m**2 * g)/(k**2) *
			Math.log((x - m/k * v0 * Math.cos(angle * deg2rad))/(- m/k * v0 * Math.cos(angle * deg2rad)))
			- a;
			ctx.lineTo(Math.abs(x), y);
			ctx.stroke();
		}

		//tableau pour les données du graphique
		if (y <= 0) {
			X.push(x);
			Y.push(-y);
		}

		requestAnimationFrame(dessinTrajectoire);

		//condition de fin de boucle
		if (y >= 75) {
			stop = 1;
		}
	} else {
		stop = 0;
		document.getElementById("angle").disabled = false;
	}
}