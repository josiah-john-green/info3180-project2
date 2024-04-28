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
            <li class="nav-item">
              <RouterLink class="nav-link" to="/user/:user_id">My Profile</RouterLink>
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
