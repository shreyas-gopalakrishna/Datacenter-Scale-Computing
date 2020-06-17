
urlTry = "http://35.203.175.54:5000/"

window.masterData = {};

$(document).ready(function(){


	// set username
	masterData.name = "Shreyas Gopalakrishna"

	$("#pName").text(masterData.name);	
	$("#sName").text(masterData.name);	
	$("#name").text(masterData.name);

	masterData.username = "sg@mail.com"


	// get documents of user
	dataToGetCategories = new FormData();

	dataToGetCategories.append("username", masterData.username);	
	$.post({
	        url: urlTry+"user",
	        data: dataToGetCategories,
	        success: function (response) {
	            populateCategories(response);
	        },
	        cache: false,
	        contentType: false,
	        processData: false
    });	


  $("#documentsNavigation").click(function(){
    $("#uploadTab").hide();
    $("#documentsTab").show();
  });

  $("#uploadNavigation").click(function(){
    $("#documentsTab").hide();
    $("#uploadTab").show();
    $("#uploadFile")[0].reset();
    $("#uploadSpinner").show();
	$("#ocr-content").html('');
  });

  // code source - https://stackoverflow.com/questions/4220126/run-javascript-function-when-user-finishes-typing-instead-of-on-key-up

  //setup before functions
	var typingTimer;                //timer identifier
	var doneTypingInterval = 2000;  //time in ms, 5 second for example
	var $input = $('#searchInput');

	//on keyup, start the countdown
	$input.on('keyup', function () {
	  clearTimeout(typingTimer);
	  typingTimer = setTimeout(searchKeywordsInAllDocuments, doneTypingInterval);
	});

	//on keydown, clear the countdown 
	$input.on('keydown', function () {
	  clearTimeout(typingTimer);
	});

	//user is "finished typing," do something
	function searchKeywordsInAllDocuments () {
	  //do something

	  	searchKeywords = $('#searchInput').val().trim().split(' ')

	  	dataToGetCategories = new FormData();

    	dataToGetCategories.append("username", masterData.username);
		dataToGetCategories.append("keywords", searchKeywords);

		$.post({
		        url: urlTry+"keywords",
		        data: dataToGetCategories,
		        success: function (response) {
		        	console.log(response)
		        	updateDocumentsOnSearch(response);		        	
		        },
		        cache: false,
		        contentType: false,
		        processData: false
	    });

	}

});

function populateCategories(data) {
	// add to masterData

	console.log(data)

	masterData.documents = data

	categories = new Map()

	for(var i = 0; i < data.documents.length; i++) {

		for(var j = 0; j < data.documents[i].categories.length; j++){

			var a = categories.get(data.documents[i].categories[j].name)
			if(!a){
				a = [data.documents[i]]
			}else{
				a.push(...[data.documents[i]])
			}

			categories.set(data.documents[i].categories[j].name, a)
		}

	}

	masterData.categories = categories

	categoriesTab = document.getElementById("categoriesTab")

	i = 0
	for (let [k, v] of masterData.categories) {
		categoryName = k.replace("\/","");
		documentsInCategory = v

		categoryBox = document.getElementById("categoryBox").cloneNode(true);
		categoryBox.id = "categoryBox" + i
		categoryBox.style.display = 'block';

		categoryBox.childNodes[1].childNodes[3].childNodes[1].childNodes[1].innerHTML = categoryName
		categoryBox.childNodes[1].childNodes[3].childNodes[3].innerHTML = documentsInCategory.length

		categoryBox.childNodes[1].childNodes[3].childNodes[1].childNodes[1].setAttribute("data-target", "#modal-default"+i);

		categoryBox.childNodes[1].childNodes[5].id= "modal-default"+i


		categoryBox.childNodes[1].childNodes[5].childNodes[1].childNodes[1].childNodes[1].childNodes[3].innerHTML = "Documents - " + categoryName

		tBody = document.createElement("tbody");

		var tr = document.createElement('tr')
		var thSl = document.createElement('th')
		thSl.innerHTML = "No."
		var thDI = document.createElement('th')
		thDI.innerHTML =  "Document ID"
		var thFn = document.createElement('th')
		thFn.innerHTML = "Filename"
		var thFd = document.createElement('th')
		thFd.innerHTML = "File Description"

		tr.appendChild(thSl)
		tr.appendChild(thDI)
		tr.appendChild(thFn)
		tr.appendChild(thFd)

		tBody.appendChild(tr)

		categoryBox.childNodes[1].childNodes[5].childNodes[1].childNodes[1].childNodes[3].childNodes[5].childNodes[1].appendChild(tBody);

	    categoryBox.childNodes[1].childNodes[5].childNodes[1].childNodes[1].childNodes[3].childNodes[7].id = "ocrContentQuote" + categoryName.replace(/\s/g,'')
	    categoryBox.childNodes[1].childNodes[5].childNodes[1].childNodes[1].childNodes[3].childNodes[7].childNodes[1].childNodes[1].id = "ocrContent" + categoryName.replace(/\s/g,'')


		for (var k1 = 0; k1 < documentsInCategory.length; k1++) {
		    var trB = document.createElement('tr');

		    var thSlB = document.createElement('td')
		    thSlB.innerHTML = k1+1
			var thDIB = document.createElement('td')
			var ancDI = document.createElement('a')
			ancDI.innerHTML = documentsInCategory[k1].documentId;
			ancDI.setAttribute('ocrContentQuote',"ocrContentQuote" + categoryName.replace(/\s/g,''));
			ancDI.setAttribute('ocrContent',"ocrContent" + categoryName.replace(/\s/g,''));
			ancDI.addEventListener("click", getAndShowOcrContentToTable, false);

			thDIB.appendChild(ancDI)
			var thFnB = document.createElement('td')
			thFnB.innerHTML = documentsInCategory[k1].filename
			var thFdB = document.createElement('td')
			thFdB.innerHTML = documentsInCategory[k1].fileDescription

			trB.appendChild(thSlB)
			trB.appendChild(thDIB)
			trB.appendChild(thFnB)
			trB.appendChild(thFdB)

		    tBody.appendChild(trB);


		    // create a modal for each document

		    ocrP = document.createElement('p');
		    ocrP.id = documentsInCategory[k1].documentId
		    ocrP.style.display = 'none';


		    categoryBox.childNodes[1].childNodes[5].childNodes[1].childNodes[1].childNodes[3].childNodes[5].appendChild(ocrP);
		}

		i++
		categoriesTab.appendChild(categoryBox)
	}



	// All documents tab starts here
	allDocumentsTab = document.getElementById("allDocuments");

	table = document.createElement("table")
	table.setAttribute("class", "table table-hover");

	tBody = document.createElement("tbody");

	var tr = document.createElement('tr')
	var thSl = document.createElement('th')
	thSl.innerHTML = "No."
	var thDI = document.createElement('th')
	thDI.innerHTML =  "Document ID"



	var thFn = document.createElement('th')
	thFn.innerHTML = "Filename"
	var thFd = document.createElement('th')
	thFd.innerHTML = "File Description"

	tr.appendChild(thSl)
	tr.appendChild(thDI)
	tr.appendChild(thFn)
	tr.appendChild(thFd)

	tBody.appendChild(tr)

	table.appendChild(tBody)

	for (var k1 = 0; k1 < masterData.documents.documents.length; k1++) {
		console.log("lknjbhv")
	    var trB = document.createElement('tr');

	    var thSlB = document.createElement('td')
	    thSlB.innerHTML = k1+1
		var thDIB = document.createElement('td')

		var ancDIB = document.createElement('a')
		ancDIB.innerHTML = masterData.documents.documents[k1].documentId;
		ancDIB.addEventListener("click", getAndShowOcrContentToTableAllDoc, false);

		thDIB.appendChild(ancDIB)


		var thFnB = document.createElement('td')
		thFnB.innerHTML = masterData.documents.documents[k1].filename
		var thFdB = document.createElement('td')
		thFdB.innerHTML = masterData.documents.documents[k1].fileDescription

		trB.appendChild(thSlB)
		trB.appendChild(thDIB)
		trB.appendChild(thFnB)
		trB.appendChild(thFdB)

		tBody.appendChild(trB)

	}

	allDocumentsTab.appendChild(table);


}


function uploadDocument() {
	console.log("click!")

	$('#ocr-modal-default').modal('show');

	$("form#uploadFile").submit(function(e) {
    	e.preventDefault();
	});

	filename = document.getElementById("filename").value;
	fileDescription = document.getElementById("fileDescription").value;

	file = document.getElementById("file").files[0];
	formData = new FormData();

	formData.append("username", masterData.username);
	formData.append("filename", filename);
	formData.append("fileDescription", fileDescription);
	formData.append("file", file);

	console.log(formData)

    // Display the key/value pairs
	for (var pair of formData.entries()) {
	    console.log(pair[0]+ ', ' + pair[1]); 
	}

	$.post({
	        url: urlTry+"upload/" +filename,
	        type: 'POST',
	        data: formData,
	        success: function (data) {
	            console.log(data)
	            myTimer = setInterval(getAndShowOcrContent,3000,data);
	        },
	        cache: false,
	        contentType: false,
	        processData: false
    	});
}

function getAndShowOcrContentToTable() {
	console.log("getAndShowOcrContentToTable");

	ocrcontent = this.getAttribute('ocrcontent');
	ocrContentQuote = this.getAttribute('ocrContentQuote');

	console.log($("a[ocrcontent='" + ocrcontent + "']"));


    documentId = this.innerHTML
    // get documents of user
	dataToGetCategories = new FormData();

	dataToGetCategories.append("username", masterData.username);	
	$.post({
	        url: urlTry+"document/" + documentId,
	        data: dataToGetCategories,
	        success: function (response) {
	        	if(typeof response.documentContent != "undefined" 
	        		&& response.documentContent.length > 0){
	        		console.log(response.documentContent)
	        		$("p[id='" + ocrcontent + "']").html(response.documentContent);
	        		$("div[id='" + ocrContentQuote + "']").show();	        		
	        	}
	        },
	        cache: false,
	        contentType: false,
	        processData: false
    });
    
}


function getAndShowOcrContentToTableAllDoc() {
	console.log("getAndShowOcrContentToTableAllDoc");

    documentId = this.innerHTML
    // get documents of user
	dataToGetCategories = new FormData();

	dataToGetCategories.append("username", masterData.username);	
	$.post({
	        url: urlTry+"document/" + documentId,
	        data: dataToGetCategories,
	        success: function (response) {
	        	if(typeof response.documentContent != "undefined" 
	        		&& response.documentContent.length > 0){
	        		console.log(response.documentContent)
	        		$("#ocrContentAllDoc").html(response.documentContent);
	        		$("#ocrContentQuoteAllDoc").show();	        		
	        	}
	        },
	        cache: false,
	        contentType: false,
	        processData: false
    });
    
}

function getAndShowOcrContent(data) {
	console.log("getAndShowOcrContent")
    console.log(data.documentId);
    // get documents of user
	dataToGetCategories = new FormData();

	dataToGetCategories.append("username", masterData.username);	
	$.post({
	        url: urlTry+"document/" + data.documentId,
	        data: dataToGetCategories,
	        success: function (response) {
	        	console.log(response)
	        	if(response.error != "Could not process"){
	        		console.log("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
	        		clearInterval(myTimer)
	        		$("#uploadSpinner").hide();
	        		$("#ocr-content").html(response.documentContent);
	        	}
	        },
	        cache: false,
	        contentType: false,
	        processData: false
    });
    
}

function updateDocumentsOnSearch(argument) {

	matchingDocuments = argument.documents

	if(matchingDocuments.length <= 0){
		return;
	}

	// All documents tab starts here
	searchTab = document.getElementById("searchTab");
	searchTab.innerHTML = '';

	table = document.createElement("table")
	table.setAttribute("class", "table table-hover");

	tBody = document.createElement("tbody");

	var tr = document.createElement('tr')
	var thSl = document.createElement('th')
	thSl.innerHTML = "No."
	var thDI = document.createElement('th')
	thDI.innerHTML =  "Document ID"
	var thFn = document.createElement('th')
	thFn.innerHTML = "Filename"
	var thFd = document.createElement('th')
	thFd.innerHTML = "File Description"

	tr.appendChild(thSl)
	tr.appendChild(thDI)
	tr.appendChild(thFn)
	tr.appendChild(thFd)

	tBody.appendChild(tr)

	table.appendChild(tBody)

	slNo = 0

	for (var k1 = 0; k1 < masterData.documents.documents.length; k1++) {

		for(var m=0; m < matchingDocuments.length; m++){

			// if matching document 
			if(masterData.documents.documents[k1].documentId == matchingDocuments[m]){

				console.log("lknjbhv")
			    var trB = document.createElement('tr');

			    var thSlB = document.createElement('td')
			    thSlB.innerHTML = slNo+1
				var thDIB = document.createElement('td')

				var ancDIB = document.createElement('a')
				ancDIB.innerHTML = masterData.documents.documents[k1].documentId;
				ancDIB.addEventListener("click", getAndShowOcrContentToTableSearch, false);

				thDIB.appendChild(ancDIB)


				var thFnB = document.createElement('td')
				thFnB.innerHTML = masterData.documents.documents[k1].filename
				var thFdB = document.createElement('td')
				thFdB.innerHTML = masterData.documents.documents[k1].fileDescription

				trB.appendChild(thSlB)
				trB.appendChild(thDIB)
				trB.appendChild(thFnB)
				trB.appendChild(thFdB)

				tBody.appendChild(trB)

				slNo++;

			}

		}
		

	}

	searchTab.appendChild(table);
}



function getAndShowOcrContentToTableSearch() {
	console.log("getAndShowOcrContentToTableSearch");

    documentId = this.innerHTML
    // get documents of user
	dataToGetCategories = new FormData();

	dataToGetCategories.append("username", masterData.username);	
	$.post({
	        url: urlTry+"document/" + documentId,
	        data: dataToGetCategories,
	        success: function (response) {
	        	if(typeof response.documentContent != "undefined" 
	        		&& response.documentContent.length > 0){
	        		console.log(response.documentContent)
	        		$("#ocrContentAllDocSearch").html(response.documentContent);
	        		$("#ocrContentQuoteAllDocSearch").show();	        		
	        	}
	        },
	        cache: false,
	        contentType: false,
	        processData: false
    });
    
}