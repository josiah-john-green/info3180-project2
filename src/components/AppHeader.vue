<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"><i class="bi bi-camera"></i>Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item" @click="goToProfile">
              <a class="nav-link">My Profile</a>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from "vue"; // Use ref for reactive variables
import { useRouter } from "vue-router"; // Ensure router is used

// Initialize the router for navigation
const router = useRouter(); 

// Retrieve JWT from local storage
const token = localStorage.getItem("jwt");

// Check if token exists
console.log(token);

function goToProfile() {

  if (token) {

    // Decode the JWT and extract the user ID
    const tokenParts = token.split(".");
    const payload = JSON.parse(atob(tokenParts[1])); // Decode Base64 to JSON

    // Get the user ID from the JWT
    const user_id = payload["subject"]; 

    // Navigate to the profile page with the correct user_id
    router.push({ name: "profile", params: { user_id: user_id}});

    console.log(user_id);
    
  } else {
    // Redirect to the login page if JWT is missing
    router.push({ name: "login" });
  }
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Oleo+Script:wght@400;700&display=swap');

  .navbar {
    background-color: #4a90e1;
  }

  .navbar-brand{
    font-family: 'Oleo Script', cursive; /* Use Oleo Script font */
  }

  .navbar-nav{
    padding-right: 10px;
  }

  i{
      padding-right: 5px;
  }

</style>
