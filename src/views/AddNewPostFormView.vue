<script setup>
    import NewPostForm from '@/components/NewPostForm.vue'; 
</script>

<template>
    <div>
      <h4 id="post-title">New Post</h4>
      <NewPostForm />
    </div>
</template>

<style>
#post-title {
  margin-top: 55px;
  margin-bottom: 55px;
  margin-left: 385px; /* Lefts the title */
  margin-right: auto; /* Left the title */
  text-align: left; /* Left the text */
}

@media (max-width: 1200px) {
  #post-title {
    margin-left: 295px; /* Lefts the title */
  }
}

@media (min-width: 1200px) {
  #post-title {
    margin-left: 360px; /* Lefts the title */
  }
}
</style>
