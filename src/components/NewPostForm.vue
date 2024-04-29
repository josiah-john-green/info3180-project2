<template>    
  <div class="postContainer">
    <form class="postForm shadow p-4 mb-5 bg-white rounded" method="POST" enctype="multipart/form-data" @submit.prevent="savePost" id="postForm">
      <div class="form-group mb-3">
        <label for="caption" class="form-label">Caption</label>
        <textarea id="caption" name="caption" class="form-control" v-model="formData.caption"></textarea>
        <small v-if="formData.caption === ''" class="text-danger">Caption is required</small>
      </div>
      
      <div class="form-group mb-3">
        <label for="photo" class="form-label">Photo</label>
        <input type="file" id="photo" name="photo" class="form-control" @change="handleFileChange">
        <small v-if="formData.photo === null" class="text-danger">Photo is required</small>
      </div>

      <!-- Submit button -->
      <button type="submit" class="btn">Submit</button>

      <div v-if="postError" class="text-danger">{{ postError }}</div>
    </form>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import router from '../router/index.js'


  // Define csrf_token as a reactive property
  let csrf_token = ref('');

  // Define formData as a reactive reference to an object
  const formData = ref({
    caption: '',
    photo: null
  });


  // Function to fetch CSRF token
  function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    })
    .catch(error => {
      console.error('Error fetching CSRF token:', error);
    });
  }

  function handleFileChange(event) {
    formData.value.photo = event.target.files[0];
  }


  // Define postError to hold error message
  const postError = ref('');

  function savePost() {

    // Retrieve the access token from local storage
    const token = localStorage.getItem('jwt')

    if (token == null){
        return router.push({ name: 'login'})
    }

    // Decode the access token to retrieve user ID
    const tokenParts = token.split('.')
    const payload = JSON.parse(atob(tokenParts[1]))
    const user_id = payload['subject']

    // Create a FormData object for the POST request
    let postForm = document.getElementById('postForm');
    let form_data = new FormData(postForm);

    // Send POST request to create a new post
    fetch(`/api/v1/users/${user_id}/posts`, {
      method: 'POST',
      body: form_data,
      headers: {
        'X-CSRFToken': csrf_token.value,
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) {
        console.log(data);
        throw new Error('Network response was not ok');

      }
      return response.json();
    })
    .then(data => {
        if (data.message) {
            router.push({name: 'explore'})
            console.log(data);
        }
        if (data.errors) {
            errors.value = data.errors;
            console.log(data.errors);
            clearForm();
        }
     })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }

  function clearForm(){
    var inputs = document.querySelectorAll('input');
    var textArea = document.querySelectorAll('textarea');
    inputs.forEach(input =>  input.value = '');
    textArea.forEach(input =>  input.value = '');
  }

  // Call getCsrfToken when the component is mounted
  onMounted(() => {
    clearForm();
    getCsrfToken();
  });

</script>

<style scoped>
  .postContainer {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .postForm {
    height: 50%;
    width: 50%;
  }
  
  .btn {
    display: inline-block;
    padding: 7px 300px;
    color: white;
    background-color: #7dd220;
    text-decoration: none;
    border-radius: 5px;
    transition: 0.3s ease-in-out;
    cursor: pointer;
  }

  .btn:hover {
      background-color: #4a90e1;
  }

  .text-danger {
    margin-top: 5px;
    font-size: 12px;
  }
</style>
