<template>
    <div class="postContainer">
      <div class="post-view" id="post-view">
        <div class="post-if" v-if="posts && posts.length > 0">
            <div class="card shadow rounded" v-for="post in posts" :key="post.id">                  
                <h5 v-if="post.id" class="card-title">
                    <img :src="post.profile_photo" class="post-profile_photo">
                    <RouterLink :to="{ name: 'profile', params: { user_id: post.user_id} }" class="post-user"> {{ post.username }} </RouterLink>
                </h5>
                <div class="user-else" v-else>
                    <p>Post ID is missing.</p>
                </div>
                
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
        <div class="post-else" v-else>
            <p class="post-unavailable">No posts available.</p>
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
    fetch('/api/v1/csrf-token') // Endpoint to fetch CSRF token
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token; // Store the CSRF token
        })
        .catch((error) => {
            console.error('Error fetching CSRF token:', error);
        });
}

function getLikeStatus(post) {

    if (!post || !post.id) {
        console.error("Post or Post ID is undefined.");
        return; // Avoid further execution if post is undefined
    }

    const token = localStorage.getItem("jwt");

    fetch(`/api/v1/posts/${post.id}/like_status`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value,
    },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.has_liked !== undefined) {
            console.log("Like status data:", data); // Log the response
            isLiked.value = data.has_liked; // Ensure correct follow status
        } else {
            console.warn("Like status response doesn't contain 'has_liked'");
        }
    })
    .catch((error) => {
        console.error("Error fetching like status:", error);
    });
}

function getLikeCount(post) {
    if (!post || !post.id) {
        console.log(post.id);
        console.error("Post or Post ID is undefined.");
        return; // Prevent further execution if post is undefined
    }

    const token = localStorage.getItem('jwt');

    fetch(`/api/v1/posts/${post.id}/like`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token.value,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        likeCount.value = data.likes; 
        console.log(`Like count: ${likeCount.value}`); // Log the follower count
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
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token.value,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch posts");
      }
      return response.json();
    })
    .then((data) => {
      posts.value = data;
      getLikeCount(post);
      getLikeStatus(post);
    })
    .catch((error) => {
      console.error("Error fetching posts:", error);
    });
}

function toggleLike(post) {
    
  if (!post || !post.id) {
    console.error("Post or Post ID is undefined.");
    return; // Avoid further execution if post is undefined
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
        if (data.message) {
            isLiked.value = !isLiked.value; // Toggle follow status

            if (isLiked.value) {
                likeCount.value += 1; // Increment follower count when following
            } else {
                likeCount.value -= 1; // Decrement follower count when unfollowing
            }
        }
    })
    .catch((error) => {
      console.error("Error toggling like status:", error);
    });
}

onMounted(() => {   
    getCsrfToken(); 
    getPosts(); // Fetch user details
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
  
  
  