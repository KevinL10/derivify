window.addEventListener("load", () => {
	var canvas = document.getElementById("canvas");
	var ctx = canvas.getContext("2d");
	var width = canvas.width;
	var height = canvas.height;
	var isDrawing = false;

	ctx.fillStyle = "white";
	ctx.fillRect(0, 0, canvas.width, canvas.height);  

	function getMousePos(canvas, evt) {
		var rect = canvas.getBoundingClientRect();
		return {
			x: (evt.clientX - rect.left) / (rect.right - rect.left) * width,
			y: (evt.clientY - rect.top) / (rect.bottom - rect.top) * height
		};
	}

	function draw(e) {
		if (!isDrawing) return;

		var pos = getMousePos(canvas, e);
		ctx.lineTo(pos.x, pos.y);
		ctx.stroke();
		ctx.beginPath();
		ctx.moveTo(pos.x, pos.y);
	}

	// https://stackoverflow.com/questions/12168909/blob-from-dataurl
	function dataURItoBlob(dataURI) {
		var byteString = atob(dataURI.split(',')[1]);
		var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
		var ab = new ArrayBuffer(byteString.length);
		var ia = new Uint8Array(ab);
		for (var i = 0; i < byteString.length; i++) {
			ia[i] = byteString.charCodeAt(i);
		}
		var blob = new Blob([ab], {
			type: mimeString
		});
		return blob;
	}

	canvas.addEventListener("mousedown", function() {
		isDrawing = true;
		ctx.beginPath();
	});
	canvas.addEventListener("mouseup", function() {
		isDrawing = false;
	});
	canvas.addEventListener("mouseout", function() {
		isDrawing = false;
	});
	canvas.addEventListener("mousemove", draw);
	document.getElementById('clearCanvas').onclick = function() {
		ctx.clearRect(0, 0, width, height);
	};
	
	document.getElementById('uploadCanvas').onclick = function(){
		var dataURI = canvas.toDataURL();
		const blob = dataURItoBlob(dataURI);

		var formData = new FormData();
		formData.append("file", blob);

		var request = new XMLHttpRequest();
		request.open('POST', '/derivify', true);
		request.send(formData);
	};
});