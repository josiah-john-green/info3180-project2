<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";

</script>

<template>
  <AppHeader />

  <main>
    <RouterView />
  </main>

</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

body {
  padding-top: 75px;
  background-color: #f4eee5;
  font-family: 'Open Sans', sans-serif; /* Use Oleo Script font */ 
}
</style>