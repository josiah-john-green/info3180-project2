<script setup>
    import LoginForm from '@/components/LoginForm.vue'; 
</script>

<template>
    <div>
      <h4 id="login-title">Login</h4>
      <LoginForm />
    </div>
</template>

<style>
#login-title {
  margin-top: 55px;
  margin-bottom: 55px;
  margin-left: 385px; /* Lefts the title */
  margin-right: auto; /* Left the title */
  text-align: left; /* Left the text */
}

@media (max-width: 1200px) {
  #login-title {
    margin-left: 295px; /* Lefts the title */
  }
}

@media (min-width: 1200px) {
  #login-title {
    margin-left: 360px; /* Lefts the title */
  }
}

</style>
