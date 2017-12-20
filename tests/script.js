//The data for my line
var lineData = [{
    "x": 10,
    "y": 5,
    "t": 700
}, {
    "x": 200,
    "y": 20,
    "t": 800
}, {
    "x": 400,
    "y": 10,
    "t": 900
}, {
    "x": 250,
    "y": 40,
    "t": 100
}, {
    "x": 350,
    "y": 200,
    "t": 1000
}, {
    "x": 200,
    "y": 500,
    "t": 1100
}, {
    "x": 120,
    "y": 80,
    "t": 900
}, {
    "x": 100,
    "y": 500,
    "t": 900
}, {
    "x": 100,
    "y": 50,
    "t": 800
}];


var ss = d3.select('#chart')
	.select('svg')	
	.append('svg')
	.attr('width', 760)
	.attr('height', 690)
	.style('background', "#93A1A1");


/*
//Function to draw line
var lineFunction = d3.svg.line()
			.x(function (d) {
				return d.x;})
			.y(function (d) {
				return d.y;});

var temp = [];

var tottime = 0;
var wait = {};
var ipath = 0;

 var circle = ss.append("circle")
    .attr("r", 13)
    .attr("transform", function () {
		return "translate(" + lineData[0].x + "," +lineData[0].y + ")";
	});


for (var i = 0; i < lineData.length - 1; ++i) {

    wait[i] = tottime;
    tottime += lineData[i].t;

    (function(line,i, ipath, wait, ss){
    setTimeout(function() {
		console.log(tottime,line,wait, ss)

	}, wait);})(lineData, i, ipath, wait[i], ss)
}
*/
