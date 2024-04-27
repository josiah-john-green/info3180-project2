<template></template>

<script setup>
  import { ref, onMounted } from "vue";
  import router from '../router/index.js'

  let csrf_token = ref("");

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}


function logout(){
    fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: {
        'X-CSRF-Token': csrf_token.value
    }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {              
        console.log(data);
    })
    .catch(function (error) {
        console.log(error);
    });
}

onMounted(() => {
    getCsrfToken();
    logout();
    sessionStorage.removeItem('jwt')
    return router.push({name: 'home'})
});

</script>

<style></style>