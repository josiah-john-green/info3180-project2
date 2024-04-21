<template>    
    <div class="post-view" id="post-view">
      <div class="post-card" v-for="post in posts" :key="post.id">        

        <h4 class="post-user">{{ post.username }}</h4>
        <img :src="getPhotoUrl(post.photo)" class="post-photo">
        <p class="details-description">{{ post.caption }}</p>

      </div>
    </div>

    <div class="button">
        <RouterLink to="/post/new" class="btn">Create New Post</RouterLink>
    </div>
</template>
    
<script setup>
    import { ref, onMounted } from "vue";
    let posts = ref([]);
    
    // Fetch movies data from the API when the component is mounted
    onMounted(async () => {
      try {
        const response = await fetch("/api/v1/posts");
        if (!response.ok) {
          throw new Error("Failed to fetch posts");
        }
        const data = await response.json();
        posts.value = data.posts;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    });
  
    // Method to construct the poster URL
    function getPhotoUrl(filename) {
      return `/api/v1/photos/${filename}`;
    }
</script>
  
<style scoped>
.btn {
    display: inline-block;
    padding: 7px 10px;
    color: white;
    background-color: #17bd6d;
    text-decoration: none;
    border-radius: 5px;
}
</style>
  
  
  