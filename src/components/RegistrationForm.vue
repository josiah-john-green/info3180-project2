<template>    
    <div class="registrationContainer">
        <form  method="POST" enctype="multipart/form-data" @submit.prevent="saveRegistration" id="registrationForm">
        
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" id="username" name="username" class="form-control" v-model="formData.username">
            </div>
        
            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <textarea id="password" name="password" class="form-control" v-model="formData.password"></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="firstname" class="form-label">Firstname</label>
                <textarea id="firstname" name="firstname" class="form-control" v-model="formData.firstname"></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="lastname" class="form-label">Lastname</label>
                <textarea id="lastname" name="lastname" class="form-control" v-model="formData.lastname"></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="email" class="form-label">Email</label>
                <textarea id="email" name="email" class="form-control" v-model="formData.email"></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="location" class="form-label">Location</label>
                <textarea id="location" name="location" class="form-control" v-model="formData.location"></textarea>
            </div>

            <div class="form-group mb-3">
                <label for="biography" class="form-label">Biography</label>
                <textarea id="biography" name="biography" class="form-control" v-model="formData.biography"></textarea>
            </div>
                
            <div class="form-group mb-3">
                <label for="profile_photo" class="form-label">Photo</label>
                <input type="file" id="profile_photo" name="profile_photo" class="form-control" @change="handleFileChange">
            </div>

            <button type="submit" class="btn">Register</button>
        </form>
    </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';

  // Define csrf_token as a reactive property
  let csrf_token = ref('');

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

  // Call getCsrfToken when the component is mounted
  onMounted(() => {
    getCsrfToken();
  });

  // Function to handle file change
  function handleFileChange(event) {
    formData.profile_photo = event.target.files[0];
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
          console.log(data);

          // Clear the form data after successful submission
          formData.value = {
              username: '',
              password: '',
              firstname: '',
              lastname: '',
              email: '',
              location: '',
              biography: ''
          };
          
          // Clear the form data after successful submission, primarly uploads
          registrationForm.reset(); // Reset the form

      })
      .catch(function (error) {
          console.error('There was a problem with the fetch operation:', error);
          
      });
    
  }

</script>

<style scoped>
.registrationContainer{
    display: flex;
    justify-content: center;
    align-items: center;
}

.registrationForm{
    height: 50%;
    width: 50%;
}

.btn {
    display: inline-block;
    padding: 7px 302px;
    color: white;
    background-color: #17bd6d;
    text-decoration: none;
    border-radius: 5px;
}

</style>