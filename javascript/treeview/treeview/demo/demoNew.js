  		var createTextNode = function (text) {
                var span = document.createElement("span");
                span.setAttribute("style", "margin-left: 2px");
				span.setAttribute("class", "tag");
                var tx = document.createTextNode(text);
                span.appendChild(tx);
 
                return span;
            };
 		
		var folBuilder = function(obj, classesNode){
			
			$.each(obj, function (i, aClass) {  
                    var classNode = document.createElement("li");
                    classNode.className = "closed";
                    span = document.createElement("span");
                    span.className = aClass.isFolder ? "folder" : "file";
					span.id = aClass.id;
                    span.appendChild(createTextNode(aClass.text))
                    classNode.appendChild(span);

					if(aClass.isFolderLink=="true") { 
						var examesNode = document.createElement("ul"); 
                    	examesNode.className = "folder";
						var examNode = document.createElement("li");
						examNode.className = "closed";					
						span = document.createElement("span");
						span.className = "folder";
						span.id = obj.id;
						span.appendChild(createTextNode(obj.text));
						examNode.appendChild(span);
						classNode.appendChild(examesNode);
					}
					
                    	classesNode.appendChild(classNode);
					
				
					
					
					
					
                });	
			
		}
		
		
	var buildChildTree =  function(chldElem, parElem){
		
		var htm = parElem.html();
		if(!htm) {
		$.each(chldElem, function (i, aClass) {  
            var classNode = document.createElement("li");
            classNode.className = "closed";
            span = document.createElement("span");
            span.className = aClass.isFolder ? "folder" : "file";
			span.id = aClass.id;
            span.appendChild(createTextNode(aClass.text))
            classNode.appendChild(span);

             if(aClass.isFolderLink=="true") {
				var examesNode = document.createElement("ul"); 
            	examesNode.className = "folder";
				var examNode = document.createElement("li");
				examNode.className = "closed";					
				span = document.createElement("span");
				span.className = "folder";
				span.id = aClass.id;
				span.appendChild(createTextNode(aClass.text));
				examNode.appendChild(span);
				classNode.appendChild(examesNode);
			}
						
				$(classNode).prependTo(parElem);
				$(parElem).treeview({
				  add: classNode,
				  animated: "normal"
				 });
				 tagClick();
				 expandClick();
				
		});
		
		
		
	}
		
	}	
	
 	var buildNewTree = function (students) {
 
            var root = document.createElement("ul");
            root.id = "StudentTreeRoot";
            root.setAttribute("style", "margin: 15px");
            root.className = "filetree";
            $.each(students.Root, function (i, student) { 
                var studentNode = document.createElement("li");
                studentNode.className = "open";
                var span = document.createElement("span");
                span.className = "folder" ;
				span.id = "root";
                span.appendChild(createTextNode(student.Name));
                studentNode.appendChild(span);
 
                var classesNode = document.createElement("ul"); 
				if(student.isFolderLink)
				folBuilder(student.ChildSubSet, classesNode);
				
                studentNode.appendChild(classesNode);
                root.appendChild(studentNode);
            });
 
            $("#StudentTree").html("").append(root);
            $("#StudentTreeRoot").treeview({
				 animated: "normal",
				 collapsed: false
				 });
			
			
            expandClick();	 
			
			

        };
        function tagClick(){
        	$('.tag').click(function(){
				if(!$(this).parent().hasClass('file') && $(this).parent().attr('id') != 'root'){
					$('.tag').removeClass("greyBg");
					$(this).addClass("greyBg");
					$('#file').trigger('click');
					var id = $(this).parent().attr('id');
					$("#nodeid").val(id);
				}
				
			});
        	
        	
        }
        function expandClick(){
        	
        	$(".expandable-hitarea").click(function(){ 
				if($(this).parents().eq(1).attr('id') != 'StudentTreeRoot'){
					
				var parElem = $(this).nextAll().eq(1);
				
				
				var nodeId = $(this).next().attr("id");
				$.ajax({
	        		url: "getNodeDetails.php?node="+nodeId,
	        		context: document.body,
	        		dataType:"json",
					}).done(function(res) {
	        		
	        			var jsondata = res;
	        			buildChildTree(res, parElem);
	        			
	        			
	        		});
				
				
					
				
					
				
				}
				
			});
        }
        
		$(document).ready(function () {
            $("#StudentTree").html("");
            
        	$.ajax({
        		url: "getNodeDetails.php?node=Home",
        		dataType:"json",
				context: document.body
        		}).done(function(res) {
        			var jsondata = res;
        			buildNewTree(res);
					tagClick();
        			
        		});
        	
        	
				
			
			
			
            
        });
