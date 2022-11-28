var ContinuousVisualization = function(height, width, context, canvas_element) {

	var canvas = {  
		width: width,  
		height: height,  
		halfWidth: width / 2,  
		lineWith: 2,  
		background: { Default: "#08a107", Orange: "#f60", Green: "#f80" },  
		borderColor: { White: "#fff", Green: "#f80" },  
		colorMap: { Orange: "#f60", Green: "#f80" }  
	};  

	var common = {  
		fillColor: { Default: "#0d5f0c", Green: "green", Red: "red", Orange: "#f60", White: "#fff" },  
		borderColor: "#fff",    
		lineWidth: { Pixel1: 1, Pixel2: 2, Pixel3:3, Pixel4: 4, Pixel5: 5 } 
	};  
	
	var penaltyArea = {  
		height: Math.ceil((canvas.height * 70) / 100),  
		width: Math.ceil((canvas.width * 12) / 100),  
		yPosition: Math.ceil(((canvas.height * 30) / 100) / 2),  
		xPosition: { TeamA: 0, TeamB: canvas.width - Math.ceil((canvas.width * 12) / 100) }  
	};  

	var goalArea = {  
		height: Math.ceil((penaltyArea.height * 60)/100),  
		width: Math.ceil(penaltyArea.width / 2),  
		yPositon: (canvas.height - penaltyArea.height),  
		xPosition: { TeamA: 0, TeamB: Math.ceil(canvas.width - (penaltyArea.width / 2)) }  
	};  
	var penaltyArc = {  
		xPosition: { TeamA: penaltyArea.width - goalArea.width / 4, TeamB: canvas.width - penaltyArea.width + goalArea.width / 4 },  
		yPosition: canvas.height/2,  
		radius:goalArea.height/3  
	};  
	
	var groundCorner={  
		radius:Math.ceil((canvas.height*2)/100)  
	};  



	var context = context;
    context.transform(1, 0, 0, -1, 0, height);

	function playground() {  
  
	}  
	
	playground.prototype.setGroundStyles = function () {  
		canvas_element.setAttribute("width", canvas.width);  
		canvas_element.setAttribute("height", canvas.height);  
		canvas_element.style.border = "2px solid " + canvas.borderColor.White;  
		canvas_element.style.margin = "auto 25px";  
		canvas_element.style.background = canvas.background.Default;  
	}  

	playground.prototype.drawCenterSpot = function (xAxis, yAxis, radius) {  
		context.beginPath();  
		context.arc(xAxis, yAxis, radius, 0, 2 * Math.PI);  
		context.fillStyle = common.fillColor.Default;  
		context.fill();  
		context.lineWidth = common.lineWidth.Pixel2;  
		context.strokeStyle = common.borderColor;  
		context.stroke();  
	}  
	  
	playground.prototype.drawCorner = function (xAxis, yAxis) {  
		context.beginPath();  
		context.arc(xAxis, yAxis, groundCorner.radius, 0, 2 * Math.PI);  
		context.fillStyle = common.fillColor.Default;  
		context.fill();  
		context.lineWidth = common.lineWidth.Pixel2;  
		context.strokeStyle = common.borderColor;  
		context.stroke();  
		  
	}  

	//Rectangular Area  
	playground.prototype.drawPenaltyArea = function (xAxis, yAxis) {  
		context.beginPath();  
		context.fillStyle = common.fillColor.Default;  
		context.fill();  
		context.fillRect(xAxis, yAxis, penaltyArea.width, penaltyArea.height);  
		context.lineWidth = common.lineWidth.Pixel2;  
		context.strokeStyle = common.borderColor;  
		context.strokeRect(xAxis, yAxis, penaltyArea.width, penaltyArea.height);  
	}  

	playground.prototype.drawGoalArea = function (xAxis, yAxis) {  
		context.beginPath();  
		context.fillStyle = common.fillColor.Default;  
		context.fill();  
		context.fillRect(xAxis, yAxis, goalArea.width, goalArea.height);  
		context.lineWidth = common.lineWidth.Pixel1;  
		context.strokeStyle = common.borderColor;  
		context.strokeRect(xAxis, yAxis, goalArea.width, goalArea.height);  
	}  

	playground.prototype.drawPenaltyArc = function (xAxis, yAxis, radius) {  
		context.beginPath();  
		context.arc(xAxis, yAxis, radius, 0, 2 * Math.PI);  
		context.fillStyle = common.fillColor.Default;  
		context.fill();  
		context.lineWidth = common.lineWidth.Pixel2;  
		context.strokeStyle = common.borderColor;  
		context.stroke();  
	}  

	playground.prototype.drawPenaltySpot = function (xAxis, yAxis, radius) {  
		context.beginPath();  
		context.arc(xAxis, yAxis, radius, 0, 2 * Math.PI);  
		context.fillStyle = common.fillColor.Default;  
		context.fill();  
		context.lineWidth = common.lineWidth.Pixel3;  
		context.strokeStyle = common.borderColor;  
		context.stroke();  
	}  
	    
	playground.prototype.drawLine = function (x1, y1, x2, y2) {  
		context.beginPath();  
		context.moveTo(x1, y1);  
		context.lineTo(x2, y2);  
		context.stroke();  
		context.lineWidth = common.lineWidth;  
		context.fillStyle = common.fillColor.White;  
		context.fill();  
	}  
	
	this.drawfield = function() {
		var ground = new playground();  
    	ground.setGroundStyles();  
        //First draw all corners  
        ground.drawCorner(5, 5);//Left Top  
        ground.drawCorner(5, canvas.height - 5); //Bottom Left      
        ground.drawCorner(canvas.width - 5, 5); //Top Right  
        ground.drawCorner(canvas.width - 5, canvas.height - 5); //Bottom Right  
  
        //Now draw ground devider   
        //Half-way line  
        ground.drawLine(canvas.width / 2, 0, canvas.width / 2, canvas.height);  
   
  
        //Now draw center spot  
   
   		ground.drawCenterSpot(canvas.width / 2, canvas.height / 2, penaltyArc.radius);  
        ground.drawPenaltySpot(canvas.width / 2, canvas.height / 2, 2);  
  
        //Draw Penaly Areas  
		// Team A
		ground.drawPenaltyArc(penaltyArc.xPosition.TeamA, penaltyArc.yPosition, penaltyArc.radius);  
        ground.drawPenaltyArea(penaltyArea.xPosition.TeamA, penaltyArea.yPosition);  
        ground.drawGoalArea(goalArea.xPosition.TeamA, goalArea.yPositon);  
        ground.drawPenaltySpot(goalArea.width / 2, canvas.height / 2, 2);  
 
        //Team*B  
		ground.drawPenaltyArc(penaltyArc.xPosition.TeamB, penaltyArc.yPosition, penaltyArc.radius);  
        ground.drawPenaltyArea(penaltyArea.xPosition.TeamB, penaltyArea.yPosition);  
        ground.drawGoalArea(goalArea.xPosition.TeamB, goalArea.yPositon);  
        ground.drawPenaltySpot(canvas.width - (goalArea.width / 2), canvas.height / 2, 2);  
  
             
    }


	this.draw = function(objects) {
		for (var i in objects) {
			var l = objects[i];
			for (var j in l){
			    var p = l[j]
                if (p.Shape == "circle")
                    this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled);
                if (p.Shape == "line")
                    this.drawLine(p.from_x, p.from_y, p.to_x, p.to_y, p.width, p.Color);
                if (p.Shape =="arrowHead")
                    this.drawArrrowHead(p.x,p.y,p.angle,p.s,p.Color,p.Filled);
    		};
		};
	};

	this.drawCircle = function(x, y, radius, color, fill) {
		var cx = x * width;
		var cy = y * height;
		var r = radius;

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = color;
		context.stroke();
		if (fill == "true") {
			context.fillStyle = color;
			context.fill();
		}

	};

    this.drawLine = function(fx,fy,tx,ty, w, color){
		context.beginPath();
		var fromX = fx * width;
		var fromY = fy * height;
		var toX = tx * width;
		var toY= ty * height;

		context.moveTo(fromX,fromY);
		context.lineTo(toX,toY);
		context.lineWidth = w;
		context.strokeStyle = color;
		context.stroke();
	};

    this.drawArrrowHead = function(x,y,angle,s,color,fill){
		var xc=x*width;
		var yc=y*height;
        context.lineWidth = 1;
        context.strokeStyle = color;
        context.fillStyle = color;

        context.save();
        context.translate(xc,yc);
        context.rotate(angle);
        context.scale(s,s);

        context.beginPath();
        context.moveTo(-5,-5);
        context.lineTo(5,0);
        context.lineTo(-5,5);
 	    context.closePath();

        if(fill == "true")
            context.fill();
                context.stroke();
        context.restore();
	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, height, width);
		context.beginPath();
	};
};

var Simple_Continuous_Module = function(canvas_width, canvas_height, ids) {
	// Create the element
	// ------------------

	// Create the tag:
	var canvas_tag = "<canvas id='" + ids + "' width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px dotted'></canvas>";
	// Append it to body:
	var canvas = $(canvas_tag)[0];
	$("#elements").append(canvas);

	// Create the context and the drawing controller:
	var context = canvas.getContext("2d");
	var canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context, canvas);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.drawfield();
		canvasDraw.draw(data);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};

};
