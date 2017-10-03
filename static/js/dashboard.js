/*
 * Author: Kouamé David
 * Date: xxxxxxxxx
 * Description:
 * This is a demo file used only for the main dashboard (index.html)
 **/

$(function () {

  "use strict";

  	//on ferme tous les blocks
  	$(".tab-content div").each(function(index){
  		//$(this).css("display","none");
	   })

  	//$(".tab-content div:eq(1)").css("display","block");

	$("a[data-toggle='tab'").click(function(e){

	  	//recuperation de l'id
	  	var id = $(this).data("id");

	  	$(".tab-content div").each(function(index){
	  		//$(this).css("display","none");
	  	})

	  	//$(".tab-content #"+id).css("display","block");

	})


	//permet d'ajouter une autre ligne
	$("#add_row").click(function(e){

		e.preventDefault();

		$.ajax({
			'url':"/getTypeDonnees",
			"Type":"GET",
			success: function(data){
				if (data!="[]") {
					data = JSON.parse(data);

					//recupération du nombre de champs
					var number_champ = $(".table-data tr").length;

					//recuperation du nombre de ligne demandé
					var row = $("input[name='row']").val();

					for (var i = 0; i < row; i++) {

						var content = '<tr><td class="ordre">'+(number_champ+i)*1+'</td>\
						<td style="width: 26%;"><input type="text" name="title[]" class="form-control title" required></td>';

						var select = '<td><select class="form-control type_donnees" required><option value="">Sélectionner un type de données</option>';
					    $.each(data, function(key, val){
					    	//construction du champ des exemples
					   		select = select + '<option value="'+val.pk+'">'+val.fields.libelle+'</option>';
					    })

					    select = select + '</select>';
					    content = content + select;

					    content= content +' </td>\
								<td class="exemple"></td>\
								<td class="delete"><input type="checkbox" name="delete[]" class="delete-row"></td></tr>';

						$(".table-data tbody").append(content);
					}
				}
			}
		})
	});

	//permet de generer les données
	$("#form-generate").submit(function(e){




		//ajout du loader du btn
        $("#generate").addClass("buttonload").empty().append('<i class="fa fa-spinner fa-spin"></i>Loading');

		var donnees = new Array();

		$("input[name='title[]']").each(function(element){

			var that = $(this);
			var parent = that.parent("td").parent("tr");

			var donnee = {};

			donnee.title   = that.val();
			donnee.type    = parent.find(".type_donnees").val();
			donnee.exemple = parent.find(".exemple select").val();

			donnees.push(donnee);
		})

		e.preventDefault();

		//recuperate token
		var token_right = $("input[name='csrfmiddlewaretoken']").val();

		var data = {
						"csrfmiddlewaretoken" : token_right,
						"file_name"           : $("input[name='file_name']").val(),
						"is_drop_database"    : $("input[name='is_drop_database']").is(":checked"),
						"title"               : $("input[name='title']").val(),
            "nombre_de_ligne"     : $("input[name='nombre_de_ligne']").val(),//nombre de ligne à générer
						"donnees"             : JSON.stringify(donnees),
					};


		$.ajax({
			url:"/generate",
			type:"POST",
			data: data,
			success:function(data){

				//on supprime le loader
				$("#generate").empty().append("generate");

				//insert data
				$("#data").empty().append(data);

				//on affiche
				$("#myModal").modal({
								backdrop: 'static'
							});

			},
			error:function(msg){
				alert("error");
			}
		});
	});



	//permet de charger les exemples associer à chaque type de données
	$(document).on('change', '.type_donnees', function() {

		var element = $(this);

		$.ajax({
			url:"/getExempleByTypeDonnees",
			type:"get",
			data: {"type_donnees":$(this).val()},
			success:function(data){

				var select_exemple = element.parent().parent().find("td.exemple");

				if (data!="[]") {
					data = JSON.parse(data);

					var content = '<select class="form-control" required><option value="">Sélectionner un exemple</option>';
				    $.each(data, function(key, val){
				    	//construction du champ des exemples
				   		content = content + '<option value="'+val.pk+'">'+val.fields.libelle+'</option>';
				    })

				    content = content + "</select>";

				    select_exemple.empty().append(content)
				}else if(element.val() != "" && data == "[]"){
					select_exemple.empty().append("aucun exemple disponible");
				}
			}
		});

		if(element.val() == ""){
			var select_exemple = element.parent().parent().find("td.exemple");
			select_exemple.empty();
		}
	})

	//permet d'activer la suppression
	$(document).on('change', '.delete-row', function() {
		var restant = $(".delete-row").length - $(".delete-row:checked").length;
		if($(".delete-row:checked").length>0){
			if( restant == 0){
				$("#button_delete").attr("disabled","disabled");
			}else{
				$("#button_delete").removeAttr("disabled");
			}
		}

	});

	$("#button_delete").click(function(e){
		e.preventDefault();

		var restant = $(".delete-row").length - $(".delete-row:checked").length;
		if($(".delete-row:checked").length > 0){
			if(restant > 0){
				$(".delete-row:checked").each(function(element){
					$(this).parent("td").parent("tr").remove();
				})

				$("#button_delete").attr("disabled","disabled");

				//on range l'odre au niveau du tableau
				$(".table-data tr").each(function(element){
					$(this).find(".ordre").text(element);
				})
			}

		}


	})
})
