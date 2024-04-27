<template>
  <div class="startup-view">
    <!-- Dynamically generate the poster URL using the photogram's poster filename -->
    <div class="startup-image shadow bg-white rounded">
      <img src="start-up-photo.jpeg" class="startup-photo rounded" alt="Startup Photo">
    </div>

    <div class="startup-details shadow p-3 mb-5 bg-white rounded">
      <h4 class="startup-title"><i class=""></i>Photogram</h4>
      <hr>
      <p class="startup-description">Share photos of your favorite moments with friends, family, and the world.</p>

      <div class="button">
        <router-link to="/register" class="btn blue">Register</router-link>
        <router-link to="/login" class="btn green">Login</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Oleo+Script:wght@400;700&display=swap');

/* Add styling for the button */
.startup-view {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin: 150px 55px 55px 55px;

}

.startup-image, .startup-details{
  width: 100%;
  height: 40%;    
}

.startup-title{
  font-family: 'Oleo Script', cursive; /* Use Oleo Script font */ 
  text-align: center;
  font-size: 30px;
  padding: 10px;
}

.startup-photo{
  width: 100%; /* Ensure the image fills the container */
  height: 100%; /* Maintain aspect ratio */
  object-fit: cover; /* Scale the image to cover the entire container */
}

/* Base button style */
.button {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  padding: 30px 0 0 0;
  cursor: pointer;
}

/* Button color variants */
.blue {
  background-color: #4a90e1;
  color: white;
}

.green {
  background-color: #7dd220;
  color: white;
}
</style>
