<template> 
    <div class="profileContainer">
        <div class="card shadow p-4 mb-5 bg-white rounded profileHeader">
            <img :src="user.profile_photo" class="user-profile_photo"> 

            <div class="user-details">
                <h4 class="user-name">{{ user.firstname }} {{ user.lastname }}</h4>
                <div class="user-locale">
                    <p class="user-location">{{ user.location }}</p>
                    <p class="user-join">Member since {{ user.joined_on }}</p>
                </div>    
                <p class="user-info">{{ user.biography }}</p>
            </div>

            <div class="social-details">
                <div class="social">
                    <div class="post-count"> 
                        <p class="post-no">{{ postCount }}</p>
                        <p class="post-title">Posts</p>
                    </div>
                    <div class="follower-count"> 
                        <p class="follower-no">{{ followerCount || 0 }}</p>
                        <p class="follower-title">Followers</p>
                    </div>
                </div>
                
                <!-- Follow/Unfollow button with dynamic class and text -->
                <button
                    @click="toggleFollow"
                    :class="[user.followed ? 'following' : 'follow']"
                >
                    {{ user.followed ? 'Following' : 'Follow' }}
                </button>
            </div>       
        </div>

        <div class="profileBody">
            <div class="post-grid" v-for="post in user.posts" :key="post.id">                  
                <img :src="post.photo" class="post-photo"> 
            </div>
        </div>  
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from 'vue-router';
import router from '../router/index.js';

const route = useRoute();
const user_id = route.params.user_id;

const postCount = ref(0);
const isFollowing = ref(false);
const followerCount = ref(0);

const csrf_token = ref(""); // CSRF token

const user = ref({
  firstname: '',
  lastname: '',
  location: '',
  biography: '',
  joined_on: '',
  profile_photo: '',
  posts: [],
});

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    })
    .catch((error) => {
      console.error('Error fetching CSRF token:', error);
    });
}

function getFollowStatus() {
  const token = localStorage.getItem("jwt");

  if (!token) {
    router.push({ name: 'login' });
    return;
  }

  fetch(`/api/v1/users/${user_id}/follow_status`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
        if (data.hasOwnProperty("is_following")) {
            console.log("Follow status data:", data); // Log the response
            isFollowing.value = data.is_following; // Ensure correct follow status
        } else {
            console.warn("Follow status response doesn't contain 'is_following'");
        }
    })
    .catch((error) => {
      console.error("Error fetching follow status:", error);
    });
}

function getUserDetails() {
  const token = localStorage.getItem("jwt");

  if (!token) {
    router.push({ name: 'login' });
    return;
  }

  fetch(`/api/v1/users/${user_id}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      user.value = data;
      postCount.value = data.posts.length;
      getFollowerCount();
      getFollowStatus();
    })
    .catch((error) => {
      console.error("Error fetching user details:", error);
    });
}

function toggleFollow() {
  const token = localStorage.getItem("jwt");

  if (!token) {
    router.push({ name: 'login' });
    return;
  }

  fetch(`/api/v1/users/${user_id}/follow`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token.value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
        if (data.hasOwnProperty("message")) {
            isFollowing.value = !isFollowing.value; // Toggle follow status
        }
    })
    .catch((error) => {
      console.error("Error following/unfollowing:", error);
    });
}

function getFollowerCount() {
    const token = localStorage.getItem('jwt');

    fetch(`/api/v1/users/${user_id}/follow`, {
        method: 'GET',
        headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token.value, // Include CSRF token
        },
    })
    .then((response) => response.json())
    .then((data) => {
        followerCount.value = data.followers; // Set the like count
        isFollowing.value = data.followed; // Check if the current user liked the post
        console.log(`Follower count: ${followerCount.value}`); // Log the follower count
    })
    .catch((error) => {
        console.error('Error getting follower count:', error);
    });
}

onMounted(() => {
    if (!user_id) { // Check if `user_id` is undefined
        router.push({ name: 'login' }); // Redirect to login if undefined
        return; // Exit early to avoid further errors
    }
    getCsrfToken(); 
    getUserDetails(); // Fetch user details
});

</script>


<style scoped>
    .profileContainer {
        margin: 55px;
        background-color: #f4eee5;
    }

    .profileHeader {
        display: grid;
        grid-template-columns: 50px 750px 50px;
        gap: 100px;
    }

    .profileBody {
        display: grid;
        grid-template-columns: repeat(3, 200px);
        column-gap: 240px;
        row-gap: 25px;
    }

    .user-details {
        padding: 10px 10px 10px 100px;
    }

    .user-profile_photo {
        width: 200px;
        height: 200px;
        border-radius: 50%;
    }

    .user-name {
        font-weight: 650;
    }

    .user-locale{
        display: flex;
        flex-direction: column;
        padding: 20px 0 20px 0;
        line-height: 0.75;
        font-size: 14.5px;
    }

    .user-info{
        font-size: 14.5px;        
    }

    .post-photo {
        width: 400px;
        height: 400px;
    }

    .follower-no, .post-no {
        font-size: 20px;
    }

    .follower-title, .post-title {
        font-size: 15px;
        color: rgb(186, 186, 186);
        font-weight: 500;
    }

    .social-details {
        padding: 10px; /* Match button padding to ensure consistency */
        text-align: center;
        align-items: center;
    }

    .social {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 80px;
        padding-bottom: 25px;
    }

    button {
        display: flex; 
        justify-content: center; 
        align-items: center; 
        padding: 10px 95px; 
        color: white; 
        width: 100px;
        font-size: 16px; 
        font-weight: 500; 
        border: none; 
        border-radius: 5px; 
        white-space: nowrap; 
        overflow: hidden; 
        cursor: pointer; 
    }

    button.follow {
        background-color: #4a90e1; 
    }

    button.following {
    background-color: #7dd220; 
    }

</style>
