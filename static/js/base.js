$(document).ready(function(){
	$("#sidebar-trending-div").click(function(){
		if($("#trending-div").attr("data-toggle") == "closed"){
			$("#trending-div").slideDown("medium");
			$("#trending-div").attr("data-toggle", "open")
		}
		else{
			$("#trending-div").slideUp("medium");
			$("#trending-div").attr("data-toggle", "closed")
		}
	});

	$("#sidebar-most-div").click(function(){
		if($("#most-div").attr("data-toggle") == "closed"){
			$("#most-div").slideDown("medium");
			$("#most-div").attr("data-toggle", "open")
		}
		else{
			$("#most-div").slideUp("medium");
			$("#most-div").attr("data-toggle", "closed")
		}
	})

});