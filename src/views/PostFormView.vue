<template>
    <div class="post-container">
        <div class="card shadow rounded">
            <h5 class="user-details">
                <img :src="user.profile_photo" class="post-profile_photo"/>
                <p class="post-user"> {{ user.username }} </p>
            </h5>
            
            <img :src="post.photo" class="post-photo" />
            <div class="post-description">
            <p class="post-caption">{{ post.caption }}</p>
            <div class="post-details">
                <div class="like-details">
                <i @click="toggleLike" :class="[isLiked ? 'bi bi-heart-fill red' : 'bi bi-heart grey']"></i>
                <p class="post-likes">{{ likeCount }} likes</p>
                </div>
                <p class="post-date">{{ post.created_on }}</p>
            </div>
        </div>
      </div>
    </div>
  </template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import router from '../router/index.js';

const route = useRoute(); // Get the current route
const post_id = route.params.post_id; // Get the post_id parameter from the route

let csrf_token = ref('');

let post = ref({});
let user = ref({}); 

let isLiked = ref(false); // Initialize as ref to manage reactivity
let likeCount = ref(0); // Initialize as ref to manage reactivity

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => console.error("Error fetching CSRF token:", error));
}

function getLikeStatus(post_id) {
  if (!post_id) {
    console.error("Post ID is undefined.");
    return;
  }

  const token = localStorage.getItem("jwt");

  fetch(`/api/v1/posts/${post_id}/like_status`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      isLiked.value = data.has_liked; // Set the correct like status
    })
    .catch((error) => {
      console.error("Error fetching like status:", error);
    });
}

function getLikeCount(post_id) {
  if (!post_id) {
    console.error("Post ID is undefined.");
    return;
  }

  const token = localStorage.getItem("jwt");

  fetch(`/api/v1/posts/${post_id}/like`, {
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
    })
    .catch((error) => {
      console.error("Error getting like count:", error);
    });
}

function getPost() {
  const token = localStorage.getItem("jwt");

  fetch(`/api/v1/posts/${post_id}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      post.value = data; // Assign the post data
      user.value = data.user; // Assign user data
      getLikeCount(post_id); // Fetch the like count
      getLikeStatus(post_id); // Fetch the like status
    })
    .catch((error) => {
      console.error("Error fetching post:", error);
    });
}

function toggleLike() {
  const post_id = post.value.id; // Ensure post_id is obtained

  if (!post_id) {
    console.error("Post ID is undefined.");
    return;
  }

  const token = localStorage.getItem("jwt");

  fetch(`/api/v1/posts/${post_id}/like`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message) {
        isLiked.value = !isLiked.value; // Toggle like status

        if (isLiked.value) {
          likeCount.value += 1; // Increase like count
        } else {
          likeCount.value -= 1; // Decrease like count
        }
      }
    })
    .catch((error) => {
      console.error("Error toggling like status:", error);
    });
}

onMounted(() => {
  getCsrfToken(); 
  getPost(); // Fetch the post when the component is mounted
});
</script>

  
<style scoped>

    .post-container {

        padding: 50px 300px 300px 300px;
    }

    .post-description{
        padding: 30px 20px 20px 20px;
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

    .user-details {
        display: flex;
        flex-direction: row;
        font-size: 15px;
        padding: 20px 20px 2px 20px;
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