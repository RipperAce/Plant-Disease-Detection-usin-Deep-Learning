// Initialize Cloud Firestore through Firebase
var db = firebase.firestore();
// Disable deprecated features
db.settings({
  timestampsInSnapshots: true
});
function submitClick()
{
	var inputText = document.getElementById("name1").value;
	var inputText1 = document.getElementById("phone1").value;
	var inputText2 = document.getElementById("message1").value;
	var clear1=document.getElementById("name1").value='';
	var clear2=document.getElementById("phone1").value='';
	var clear3=document.getElementById("message1").value='';
	// Add a new document in collection "cities"
	db.collection("Feedbacks").doc().set({
		Name: inputText,
		Mobile: inputText1,
		Message: inputText2,
	})
	.then(function() {
		console.log("Document successfully written!");
	})
	.catch(function(error) {
		console.error("Error writing document: ", error);
	});
}