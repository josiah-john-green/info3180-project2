<template>    
    <div class="registrationContainer">
        <form class="registrationForm shadow p-3 mb-5 bg-white rounded" method="POST" enctype="multipart/form-data" @submit.prevent="saveRegistration" id="registrationForm">
        
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" id="username" name="username" class="form-control" v-model="formData.username">
                <small v-if="formData.username === ''" class="text-danger">Username is required</small>
            </div>
        
            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" name="password" class="form-control" v-model="formData.password">
                <small v-if="formData.password === ''" class="text-danger">Password is required</small>
            </div>

            <div class="form-group mb-3">
                <label for="firstname" class="form-label">Firstname</label>
                <input type="text" id="firstname" name="firstname" class="form-control" v-model="formData.firstname">
                <small v-if="formData.firstname === ''" class="text-danger">Firstname is required</small>
            </div>

            <div class="form-group mb-3">
                <label for="lastname" class="form-label">Lastname</label>
                <input type="text" id="lastname" name="lastname" class="form-control" v-model="formData.lastname">
                <small v-if="formData.lastname === ''" class="text-danger">Lastname is required</small>
            </div>

            <div class="form-group mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" id="email" name="email" class="form-control" v-model="formData.email">
                <small v-if="formData.email === ''" class="text-danger">Email is required</small>
            </div>

            <div class="form-group mb-3">
                <label for="location" class="form-label">Location</label>
                <input type="text" id="location" name="location" class="form-control" v-model="formData.location">
                <small v-if="formData.location === ''" class="text-danger">Location is required</small>
            </div>

            <div class="form-group mb-3">
                <label for="biography" class="form-label">Biography</label>
                <textarea id="biography" name="biography" class="form-control" v-model="formData.biography"></textarea>
                <small v-if="formData.biography === ''" class="text-danger">Biography is required</small>
            </div>
                
            <div class="form-group mb-3">
                <label for="profile_photo" class="form-label">Photo</label>
                <input type="file" id="profile_photo" name="profile_photo" class="form-control" @change="handleFileChange">
                <small v-if="formData.profile_photo === null" class="text-danger"> Photo is required</small>
            </div>

            <div class="form-group mb-3">
                <button type="submit" class="btn">Register</button>
            </div>


            <div v-if="registrationError" class="text-danger">{{ registrationError }}</div>
        </form>
    </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import router from '../router/index.js'

  // Define csrf_token as a reactive property
  let csrf_token = ref('');
  

  // Define loginError to hold error message
  const registrationError = ref('');
  var errors = ref([]);

  // Define formData as a reactive reference to an object
  const formData = ref({
    username: '',
    password: '',
    firstname: '',
    lastname: '',
    email: '',
    location: '',
    biography: '',
    profile_photo: null  // Assuming you're handling file uploads
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
  
  // Function to handle form submission
  function saveRegistration() 
  {

      let registrationForm = document.getElementById('registrationForm');
      let form_data = new FormData(registrationForm);
      
      form_data.append('username', formData.username);
      form_data.append('password', formData.password);
      form_data.append('firstname', formData.firstname);
      form_data.append('lastname', formData.lastname);
      form_data.append('email', formData.email);
      form_data.append('location', formData.location);
      form_data.append('biography', formData.biography);
      form_data.append('profile_photo', formData.profile_photo);

      fetch("/api/v1/register", {
          method: 'POST',
          body: form_data,
          headers: {
          'X-CSRFToken': csrf_token.value
          }
      })
      .then(function (response) {
          if (!response.ok) {            
            throw new Error('Network response was not ok'); 
          }
          return response.json();
      })
      .then(function (data) {
        if (data.message) {
            router.push({name: 'login'})
            console.log(data);
        }
        if (data.errors) {
            errors.value = data.errors;
            console.log(data.errors);
            clearForm();
        }
      })
      .catch(function (error) {
          console.error('There was a problem with the fetch operation:', error);
      });
    
  }

  // Function to handle file change
  function handleFileChange(event) {
    formData.value.profile_photo = event.target.files[0];
  }

  
  // Clears the form
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
    .registrationContainer{
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f4eee5;
    }

    .registrationForm{
        height: 50%;
        width: 50%;
    }

    .form-group{
        padding-bottom: 15px;
    }

    .btn {
        width: 100%;
        padding: 10px;
        display: inline-block;
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