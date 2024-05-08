<script setup>
    import RegistrationForm from '@/components/RegistrationForm.vue'; 
</script>

<template>
    <div>
      <h4 id="register-title">Register</h4>
      <RegistrationForm />
    </div>
</template>

<style>
#register-title {
  margin-top: 55px;
  margin-bottom: 55px;
  margin-left: 385px; /* Lefts the title */
  margin-right: auto; /* Left the title */
  text-align: left; /* Left the text */
}

@media (max-width: 1200px) {
  #register-title {
    margin-left: 295px; /* Lefts the title */
  }
}

@media (min-width: 1200px) {
  #register-title {
    margin-left: 360px; /* Lefts the title */
  }
}

</style>
