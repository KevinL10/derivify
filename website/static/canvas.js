canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");
width = canvas.width;
height = canvas.height;

var isDrawing = false;

function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: (evt.clientX - rect.left) / (rect.right - rect.left) * canvas.width,
        y: (evt.clientY - rect.top) / (rect.bottom - rect.top) * canvas.height
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
