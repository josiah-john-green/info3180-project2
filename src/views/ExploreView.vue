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
                <div class="like-details">
                    <i @click="toggleLike(post)" :class="[isLiked ? 'bi bi-heart-fill red' : 'bi bi-heart grey']"></i>
                    <p class="post-likes">{{ likeCount }} likes</p>
                </div>
                <p class="post-date">{{ post.created_on }}</p>
            </div>
          </div>
        </div>
      </div>
  
      <div class="button">
        <router-link to="/post/new" class="post btn"> New Post</router-link>
      </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import router from '../router/index.js';

let csrf_token = ref(''); // Reactive variable to store CSRF token
let posts = ref([]);

const isLiked = ref(false);
const likeCount = ref(0);

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        })
        .catch((error) => console.error("Error fetching CSRF token:", error));
}

function getLikeStatus(post) {
    const { id } = post; // Destructure to get post ID
    if (!id) {
        console.error("Post ID is undefined.");
        return;
    }

    const token = localStorage.getItem("jwt");

    fetch(`/api/v1/posts/${id}/like_status`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        isLiked.value = data.has_liked; // Ensure correct like status
        console.log("Liked?", isLiked.value);
    })
    .catch((error) => {
        console.error("Error fetching like status:", error);
    });
}

function getLikeCount(post) {
    const { id } = post; // Destructure to get post ID
    if (!id) {
        console.error("Post ID is undefined.");
        return;
    }

    const token = localStorage.getItem("jwt");

    fetch(`/api/v1/posts/${id}/like`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        likeCount.value = data.likes; // Set the like count
        isLiked.value = data.has_liked; // Set the liked status
        console.log("Like count:", likeCount.value);
    })
    .catch((error) => {
        console.error("Error getting like count:", error);
    });
}

function getPosts() {
    const token = localStorage.getItem("jwt");

    if (!token) {
        router.push({ name: "login" });
        return;
    }

    fetch("/api/v1/posts", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token.value,
      },
    })
    .then((response) => response.json())
    .then((data) => {
        posts.value = data.map((post) => {
            getLikeCount(post); // Pass the post to get the like count
            getLikeStatus(post); // Pass the post to get the like status
            return post;
        });
    })
    .catch((error) => {
        console.error("Error fetching posts:", error);
    });
}

function toggleLike(post) {
    if (!post || !post.id) {
        console.error("Post or Post ID is undefined.");
        return;
    }

    const token = localStorage.getItem("jwt");

    fetch(`/api/v1/posts/${post.id}/like`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.message){
            isLiked = !isLiked;

            if (isLiked) {
                likeCount.value += 1; 
            } else {
                likeCount.value -= 1; 
            }            
        }
    })
    .catch((error) => {
        console.error("Error toggling like status:", error);
    });
}

onMounted(() => {
    getCsrfToken(); 
    getPosts();
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
        padding: 30px 20px 20px 20px;
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
        text-decoration: none; 
        color: black; 
    }

    .post-date{
        color: grey;
        font-size: 15px;
        font-weight: 600;
        padding-top: 3px;
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
        padding: 30px 0 0 0;
    }

    .post-likes {
        font-size: 15px; 
        font-weight: 600;
        color: gray; 
    }

    .like-details {
        display: inline-flex; 
        flex-direction: row; 
        align-items: center; 
        justify-content: start;
        text-align: left;
    }

    .card-title {
        display: flex;
        flex-direction: row;
        font-size: 15px;
        padding: 20px;
    }

    i{
        padding: 0 13px 12.5px 0;
        cursor: pointer;
        font-size: 15px;
    }

    .red{
        color: #e74c3c;    
    }

    .grey{
        color: grey;    
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