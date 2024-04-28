<template>
    <div class="postContainer">
      <div class="post-view" id="post-view">
        <div class="card shadow rounded" v-for="post in posts" :key="post.id">                  
          <h5 class="card-title">
            <img :src="post.profile_photo" class="post-profile_photo">
            <RouterLink :to="{ name: 'profile', params: { user_id: post.user_id } }" class="post-user"> {{ post.username }} </RouterLink>
          </h5>
          
          <!-- Render post details -->
          <img v-bind:src="post.photo" class="post-photo">
          <div class="post-description">
            <p class="post-caption">{{ post.caption }}</p>
            <div class="post-details">  
                <p class="post-likes"><i class="bi bi-heart"></i>{{ post.likes }} likes</p>
                <p class="post-date"><small class="text-muted">{{ post.created_on }}</small></p>
            </div>
          </div>
        </div>
      </div>
  
      <div class="post-btn">
        <router-link to="/post/new" class="post btn"> New Post</router-link>
      </div>
    </div>
</template>
  
    
<script setup>
    import { ref, onMounted } from 'vue';
    import router from '../router/index.js';

    const posts = ref([]);

    function getPosts() {
        const token = sessionStorage.getItem('jwt');

        if (!token) {
            router.push({ name: 'login' });
            return;
        }

        fetch('/api/v1/posts', {
            method: 'GET',
            headers: {
            'Authorization': `Bearer ${token}`,
            },
        })
        .then((response) => response.json())
        .then((data) => {
            posts.value = data;
        })
        .catch((error) => {
            console.error(error);
        });
    }

    onMounted(() => {
        getPosts(); // Fetch user details on component mount
    });
</script>


  
<style scoped>
    .postContainer {
        display: grid;
        grid-template-columns: 700px auto;
        gap: 50px;
        margin: 50px 100px 100px 200px;
        background-color: #f4eee5;
    }

    .post-description{
        padding: 15px;
    }

    .post-view {
        display: grid;
        grid-template-columns: repeat(1, 1fr);
        gap: 50px;
        width: 700px;
    }

    .post-photo {
        width: 100%;
        height: 500px;
        object-fit: fill;
    }

    .post-user {
        padding: 2px 2px 2px 10px;
        text-decoration: none; /* Remove underline */
        color: black; /* Set the color to black */
    }

    .post-profile_photo {
        width: 20px;
        height: 20px;
        border-radius: 50%;
    }

    .post-details {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        font-size: 15px;
        padding-top: 10px;
    }

    .like-btn{
        background-color: transparent;
        border: none;
    }


    .card-title {
        display: flex;
        flex-direction: row;
        font-size: 15px;
        padding: 20px;
    }

    i{
        padding-right: 10px;
        cursor: pointer;
        font-size: 15px;
    }

    .btn {
        padding: 7px 70px;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        background-color: #4a90e1;
        transition: 0.3s ease-in-out;
    }

    .post:hover{
        background-color: #7dd220; 
    }
</style>
  
  
  