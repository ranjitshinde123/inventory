<script>
function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
const cookies = document.cookie.split(';');
for (let i = 0; i < cookies.length; i++) {
const cookie = cookies[i].trim(); // Does this cookie string begin with the name we want?
if (cookie.substring(0, name.length + 1) === (name + '=')) {
cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
break;
 }
 }
 }
 return cookieValue;
 }
 const csrftoken = getCookie('csrftoken');
 let category_field = document.getElementById("id_category")
 let subcategory_field = document.getElementById("id_subcategory")
 category_field.addEventListener("change", pickState)
 function pickState(e){
 category_id = e.target.value
 const data = { id: category_id}
 let url = " {% url 'subcategorys' %} "
 fetch(url, {
 method: 'POST', // or 'PUT'
 headers: {
 'Content-Type': 'application/json',
 'X-CSRFToken': csrftoken
 },
 body: JSON.stringify(data),
 })
 .then(response => response.json())
 .then(data => {
 console.log('Success:', data);
 subcategory_field.innerHTML = '<option value = "" selected="">---------------</option>'
 for(let i = 0; i<data.length; i++){
 subcategory_field.innerHTML += '<option value ="'+data[i]["id"]+'">'+data[i].subcategory+'</option>'
 }
 })
 .catch((error) => {
 console.error('Error:', error);
 });
 let category_field = document.getElementById("id_category")
 let subcategory_field = document.getElementById("id_subcategory")
 let description_field = document.getElementById("id_description")
 subcategory_field.addEventListener("change", pickStates)
 function pickStates(e){
 subcategory_id = e.target.value
 const data = { id: subcategory_id}
 let url = " {% url 'descriptions' %} "
 fetch(url, {
 method: 'POST', // or 'PUT'
 headers: {
 'Content-Type': 'application/json',
 'X-CSRFToken': csrftoken
 },
 body: JSON.stringify(data),
 })
 .then(response => response.json())
 .then(data => {
 console.log('Success:', data);
 description_field.innerHTML = '<option value = "" selected="">---------------</option>'
 for(let i = 0; i<data.length; i++){
 description_field.innerHTML += '<option value ="'+data[i]["id"]+'">'+data[i].description+'</option>'
 }
 })
 .catch((error) => {
 console.error('Error:', error);
 });
 }
 }
 let input = document.getElementById("id_name")
 let select = document.getElementsByTagName("select")
 console.log(select)
 input.classList.add("form-control")
 for(let i = 0; i <select.length; i++){
 select[i].classList.add("form-select")
 }


</script>
