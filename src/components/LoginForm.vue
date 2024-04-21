<template>    
    <div class="loginContainer">
        <form  method="POST" enctype="multipart/form-data" @submit.prevent="loginUser" id="loginForm">
        
            <div class="form-group mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" id="username" name="username" class="form-control" v-model="formData.username">
            </div>
        
            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <textarea id="password" name="password" class="form-control" v-model="formData.password"></textarea>
            </div>

            <button type="submit" class="btn">Login</button>
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
    password: ''
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

  // Function to handle form submission for login
  function loginUser() {
      let loginForm = document.getElementById('loginForm');
      let form_data = new FormData(loginForm);

      form_data.append('username', formData.username);
      form_data.append('password', formData.password);

      fetch("/api/v1/auth/login", {
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
          // Redirect to explore page or handle login success
          window.location.href = '/explore';
      })
      .catch(function (error) {
          console.error('There was a problem with the fetch operation:', error);
      });
  }

</script>

<style scoped>
.loginContainer{
    display: flex;
    justify-content: center;
    align-items: center;
}

.loginForm{
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
