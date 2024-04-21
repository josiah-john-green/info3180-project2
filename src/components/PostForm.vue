<template>
    <div class="postContainer">
      <form method="POST" enctype="multipart/form-data" @submit.prevent="savePost" id="postForm">
        
        <div class="form-group mb-3">
          <label for="caption" class="form-label">Caption</label>
          <textarea id="caption" name="caption" class="form-control" v-model="formData.caption"></textarea>
        </div>
        
        <div class="form-group mb-3">
          <label for="photo" class="form-label">Photo</label>
          <input type="file" id="photo" name="photo" class="form-control" @change="handleFileChange">
        </div>
  
        <button type="submit" class="btn">Submit</button>
      </form>
    </div>
  </template>
  
  <script setup>
    import { ref, onMounted } from 'vue';
  
    let csrf_token = ref('');
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
  
    // Function to fetch user_id based on username
    async function fetchUserId(username) {
      try {
        const response = await fetch(`/api/v1/users/${username}/id`);
        const data = await response.json();
        if (response.ok) {
          return data.user_id;
        } else {
          console.error('Error fetching user_id:', data.error);
          return null;
        }
      } catch (error) {
        console.error('Error fetching user_id:', error);
        return null;
      }
    }
  
    // Call getCsrfToken and fetchUserId when the component is mounted
    onMounted(async () => {
      await getCsrfToken();
      const username = 'username'; // Replace 'username' with the actual username
      const user_id = await fetchUserId(username);
      if (user_id !== null) {
        // If user_id is successfully fetched, store it in a variable accessible to other functions
        // You can pass it as an argument to the savePost function if needed
        // For now, let's just log it
        console.log('User ID:', user_id);
      } else {
        console.error('Failed to fetch user_id');
      }
    });
  
    // Function to handle file change
    function handleFileChange(event) {
      formData.photo = event.target.files[0];
    }
  
    function savePost() {
      // Your savePost function code here
      // You can access user_id variable here if needed
    }
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
    padding: 7px 302px;
    color: white;
    background-color: #17bd6d;
    text-decoration: none;
    border-radius: 5px;
  }
  </style>
  