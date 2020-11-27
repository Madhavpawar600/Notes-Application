var isedit=false;
var nid;
$("#addnote").click(function(){
	$("#notes").hide();
	$(this).hide();
	$('#edit').hide();
	$('#done').hide();
	$('#save').show();
	$('#allnote').show();
	$('#notepad').show();

});
$("#allnote").click(function(){
	$(this).hide();
	$('#notepad').hide();
	$('#save').hide();
	$('#done').hide();
	$('#edit').show();
	$("#notes").show();
	$('#addnote').show();
	$('.delete').css({'display':'none'});
	$('.notes').css({'width':'100%','margin-left':'0'});

});

$('#edit').click(function(){
	$(this).hide();
	$('#done').show();
	$('#save').hide();
	$('.delete').css({'display':'block'});
	$('.notes').css({'width':'72%','margin-left':'140px'});
});

$('#done').click(function(){
	$(this).hide();
	$('#edit').show();
	$('.delete').css({'display':'none'});
	$('.notes').css({'width':'100%','margin-left':'0'});
});

$('.notes').dblclick(function(event){
	event.preventDefault();
	nid=$(this).attr('id');
	var notetext=$(this).find('#notestext').text();
	isedit=true;
	console.log(notetext);
	console.log(nid);
	$('#edit').hide();
	$('#done').hide();
	$('#notes').hide();
	$('#addnote').hide();
	$('.delete').hide();
	$('#save').show();
	$('#allnote').show();
	$('#notepad').show();
	$('#notepad').html("<textarea rows='10' form='formnotepad'>"+ notetext +"</textarea>");

});

$('.delete').click(function(event){
	//prevent from loading the page
	event.preventDefault();
	var pk=$(this).next().attr('id');
	console.log(pk);
	var text=$("#formnotepad").serializeArray();
	text.push({name: 'id', value: pk});
	
	//send data to del the note
	$.ajax({
		url:"/onlinenotes/delete",
		type:'POST',
		data:text,
		success:function(data){
			if (data){
				$('#notes').html(data);
				$('.delete').css({'display':'block'});
				$('.notes').css({'width':'72%','margin-left':'140px'});
			}
		},
		error:function(){
			console.log('there is some error');
		}
	});
});

$('#save').click(function(event){
	event.preventDefault();
	var textdata=$("textarea").val();
	var text=$("#formnotepad").serializeArray();
	text.push({name: 'textdata', value: textdata});
	text.push({name: 'pk', value: nid});
	console.log(text);
	console.log(isedit);
	if (isedit==true){
		var URL='/onlinenotes/edit';
	}else{
		var URL='/onlinenotes/save';
	}
	//send data to save
	$.ajax({
		url:URL,
		type:'POST',
		data: text,
		success:function(data){
			if (data){
				$('#notes').html(data);
				$('#notepad').hide();
				$('#addnote').show();
				$('#allnote').hide();
				$('#notepad').hide();
				$('#save').hide();
				$('#done').hide();
				$('#edit').show();
				$("#notes").show();
			}
		},
		error:function(){
			console.log('there is an error')
		},
	})
});

//login form ajaxcall
$('#signupform').submit(function (e){
	//prevent page from refreshing
	e.preventDefault();
	//collect user inputs
	var datatopost=$(this).serializeArray();
	console.log(datatopost);

	//send them to signup view using ajax
	$.ajax({
		url:"/onlinenotes/signup",
		type:'POST',
		data:datatopost,
		success:function(data){
			if (data){
				$('#signupmessage').html(data)
			}
		},
		error:function(){
			$("#signupmessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
		},
	});
});

$('#loginform').submit(function(e){
	//prevent page from refreshing
	e.preventDefault();
	//collect login inputs
	var datatopost=$(this).serializeArray();
	console.log(datatopost);
	$.ajax({
		url:"/onlinenotes/login",
		type:"POST",
		data:datatopost,
		success:function(data){
			if (data){
				console.log(data);
				$('#loginmessage').html(data)
			}
		},
		error:function(){
			$("#loginmessage").html("<div class='alert alert-danger'>There was an error with the Ajax Call. Please try again later.</div>");
		},

	})

});

