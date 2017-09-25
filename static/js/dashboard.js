/*
 * Author: Kouamé David
 * Date: xxxxxxxxx
 * Description:
 *      This is a demo file used only for the main dashboard (index.html)
 **/

$(function () {

  "use strict";


  	//on ferme tous les blocks
  	$(".tab-content div").each(function(index){
  		$(this).css("display","none");
	})


  	$(".tab-content div:eq(1)").css("display","block");

	$("a[data-toggle='tab'").click(function(e){
  	
	  	//recuperation de l'id
	  	var id = $(this).data("id");

	  	$(".tab-content div").each(function(index){
	  		$(this).css("display","none");
	  	})
	
	  	$(".tab-content #"+id).css("display","block");

	})


	//permet d'ajouter une autre ligne
	$("#add_row").click(function(){
		var content = '<td>1</td>'+
						+'<td style="width: 26%;"><input type="text" name="title" class="form-control title"></td>'+
						+'<td style="width: 26%;">'+
							+'<select class="form-control type_donnees">'+
								'<option>Séléctionner un type de données</option>'+
								+'{% for type in typeDonnees%}'+
									+'<option value="{{type.id}}">{{type.libelle}}</option>'+
								+'{%endfor%}'+
							+'</select>'
						+'</td>'+
						+'<td class="exemple"></td>'+
						+'<td class="option"></td>';

		$.ajax({
			'url':"/getTypeDonnees",
			"Type":"GET"
		})
		console.log(content)				;
	});

	//permet de generer les données
	$("#generate").click(function(e){
		e.preventDefault();

		//recuperate token
		var token_right = $("input[name='csrfmiddlewaretoken']").val();

		var data = {
						"csrfmiddlewaretoken" : token_right,
						"file_name"           : $("input[name='file_name']").val(),
						"is_drop_database"    : $("input[name='is_drop_database']").is(":checked"),
						"title"               : $("input[name='title']").val()
					};


		$.ajax({
			url:"/generate",
			type:"POST",
			data: data,
			success:function(data){

				//insert data
				$("#data").empty().append(data);

				//on affiche
				$("#myModal").modal({
								backdrop: 'static'
							});
			}
		});
	})

	//permet de charger les exemples associer à chaque type de données
	$(".type_donnees").change(function(e){

		var element = $(this);

		$.ajax({
			url:"/getExempleByTypeDonnees",
			type:"get",
			data: {"type_donnees":$(this).val()},
			success:function(data){

				var select_exemple = element.parent().parent().find("td.exemple");

				if (data!="[]") {
					data = JSON.parse(data);
				
					var content = '<select class="form-control">';
				    $.each(data, function(key, val){
				    	//construction du champ des exemples
				   		content = content + '<option value="'+val.pk+'">'+val.fields.libelle+'</option>';
				    })

				    content = content + "</select>";

				    select_exemple.empty().append(content)
				}else{
					select_exemple.empty();
				}
				
			}
		});
	})
})
