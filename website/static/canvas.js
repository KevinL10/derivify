window.addEventListener("load", () => {
	var canvas = document.getElementById("canvas");
	var ctx = canvas.getContext("2d");
	var width = canvas.width;
	var height = canvas.height;
	var isDrawing = false;

	function getMousePos(canvas, evt) {
	    var rect = canvas.getBoundingClientRect();
	    return {
	        x: (evt.clientX - rect.left) / (rect.right - rect.left) * width,
	        y: (evt.clientY - rect.top) / (rect.bottom - rect.top) * height
	    };
	}

	function draw(e){
		if (!isDrawing) return;

		var pos = getMousePos(canvas, e);
		ctx.lineTo(pos.x, pos.y);
		ctx.stroke();
		ctx.beginPath();
		ctx.moveTo(pos.x, pos.y);
	}

	canvas.addEventListener("mousedown", function(){
		isDrawing = true;
		ctx.beginPath();
	});
	canvas.addEventListener("mouseup", function(){
		isDrawing = false;
	});
	canvas.addEventListener("mouseout", function(){
		isDrawing = false;
	});
	canvas.addEventListener("mousemove", draw);
	document.getElementById('clearCanvas').onclick = function(){
		ctx.clearRect(0, 0, width, height);
	};
});

