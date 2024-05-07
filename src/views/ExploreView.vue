<template>
    <div class="postContainer">
      <div class="post-view" id="post-view">
        <!-- Ensure posts are defined and not empty before rendering -->
        <div v-if="posts && posts.length" v-for="post in posts" :key="post.id" class="card shadow rounded">
          <h5 class="card-title">
            <img :src="post.profile_photo" class="post-profile_photo" />
            <RouterLink :to="{ name: 'profile', params: { user_id: post.user_id } }" class="post-user">
              {{ post.username }}
            </RouterLink>
          </h5>
          <img :src="post.photo" class="post-photo" />
          <div class="post-description">
            <p class="post-caption">{{ post.caption }}</p>
            <div class="post-details">
              <div class="like-details">
                <!-- Ensure like status and count are available before accessing -->
                <i @click="toggleLike(post.id)" :class="[isLiked[post.id] ? 'bi bi-heart-fill red' : 'bi bi-heart grey']"></i>
                <!-- Access the correct like count for each post -->
                <p class="post-likes">{{ likeCount[post.id] || 0 }} likes</p>
              </div>
              <p class="post-date">{{ post.created_on }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="button">
        <router-link to="/post/new" class="post btn">New Post</router-link>
      </div>
    </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import router from '../router/index.js';
  
  const csrf_token = ref('');
  const posts = ref([]);
  
  const isLiked = ref({});
  const likeCount = ref({}); // Initial state is an object
  
  async function getCsrfToken() {
    try {
      const response = await fetch('/api/v1/csrf-token');
      const data = await response.json();
      csrf_token.value = data.csrf_token;
    } catch (error) {
      console.error("Error fetching CSRF token:", error);
    }
  }
  
  async function getLikeStatus(post_id) {
    if (!post_id) {
      console.error("Post ID is undefined.");
      return;
    }
  
    const token = localStorage.getItem("jwt");
  
    try {
      const response = await fetch(`/api/v1/posts/${post_id}/like_status`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf_token.value,
        },
      });
      const data = await response.json();
      isLiked.value[post_id] = data.has_liked; // Store like status per post
      console.log('Liked?:', isLiked.value[post_id]);
    } catch (error) {
      console.error("Error fetching like status:", error);
    }
  }
  
  async function getLikeCount(post_id) {
    if (!post_id) {
      console.error("Post ID is undefined.");
      return;
    }
  
    const token = localStorage.getItem("jwt");
  
    try {
      const response = await fetch(`/api/v1/posts/${post_id}/like`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf_token.value,
        },
      });
      const data = await response.json();
      likeCount.value[post_id] = data.likes; // Store like count per post
      console.log('Like Count:', likeCount.value[post_id]);
    } catch (error) {
      console.error("Error fetching like count:", error);
    }
  }
  
  async function getPosts() {
    const token = localStorage.getItem("jwt");
  
    if (!token) {
      router.push({ name: "login" });
      return;
    }
  
    try {
      const response = await fetch("/api/v1/posts", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
          "X-CSRFToken": csrf_token.value,
        },
      });
  
      const data = await response.json();
  
      for (const post of data) {
        await getLikeCount(post.id);
        await getLikeStatus(post.id);
      }
  
      posts.value = data;
    } catch (error) {
      console.error("Error fetching posts:", error);
    }
  }
  
  async function toggleLike(post_id) {
    if (!post_id) {
      console.error("Post ID is undefined.");
      return;
    }
  
    const token = localStorage.getItem("jwt");
  
    try {
      const response = await fetch(`/api/v1/posts/${post_id}/like`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf_token.value,
        },
      });
      const data = await response.json();
      if (data.message) {
        isLiked.value[post_id] = !isLiked.value[post_id];
  
        if (isLiked.value[post_id]) {
          likeCount.value[post_id] += 1;
          console.log('Toggle Like (+):', likeCount.value[post_id]);
        } else {
          likeCount.value[post_id] -= 1;
          console.log('Toggle Like (-):', likeCount.value[post_id]);
        }
      }
    } catch (error) {
      console.error("Error toggling like status:", error);
    }
  }
  
  onMounted(async () => {
    await getCsrfToken();
    await getPosts();
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
  
  .post-description {
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
  
  .post-date {
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
  }
  
  .card-title {
      display: flex;
      flex-direction: row;
      font-size: 15px;
      padding: 20px;
  }
  
  i {
      padding: 0 13px 12.5px 0;
      cursor: pointer;
      font-size: 15px;
  }
  
  .red {
      color: #e74c3c;
  }
  
  .grey {
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
  
  .post:hover {
      background-color: #7dd220;
  }
</style>
  