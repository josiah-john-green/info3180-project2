<template>    
  <div class="loginContainer">
    <form class="loginForm shadow p-4 mb-5 bg-white rounded" method="POST" enctype="multipart/form-data" @submit.prevent="loginUser" id="loginForm">
      <div class="form-group mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" id="username" name="username" class="form-control" v-model="formData.username" autofocus>
        <small v-if="formData.username === ''" class="text-danger">Username is required</small>
      </div>
      
      <div class="form-group mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" name="password" class="form-control" v-model="formData.password">
        <small v-if="formData.password === ''" class="text-danger">Password is required</small>
      </div>

      <button type="submit" class="btn">Login</button>

      <div v-if="loginError" class="text-danger">{{ loginError }}</div>
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
    username: '',
    password: ''
  });

  // Define loginError to hold error message
  const loginError = ref('');

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

  function loginUser(){

    let loginForm = document.getElementById('loginForm');
    let form_data = new FormData(loginForm);

    fetch("/api/v1/auth/login", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        if (data.message) {
            localStorage.setItem('jwt', data.token)
            router.push({name: 'explore'})
            console.log(data);
        }
        if (data.errors) {
            console.log(data.errors);
            clearForm();
        }
    })
    .catch(function (error) {
        console.log(error);
    });

  }

  //
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

.loginContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f4eee5;
}

.loginForm {
  height: 50%;
  width: 50%;
}

.form-group{
  padding-bottom: 15px;
}

.btn {
  display: inline-block;
  padding: 7px;
  min-width: 570px;
  max-width: auto;
  color: white;
  background-color: #7dd220;
  text-decoration: none;
  border-radius: 5px;
  /* transition: 0.3s ease-in-out; */
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
