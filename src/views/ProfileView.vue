<template> 
    <div class="profileContainer">
        <div class="card shadow p-4 mb-5 bg-white rounded profileHeader">
            <img :src="user.profile_photo" class="user-profile_photo"> 

            <div class="user-details">
                <h3 class="user-name">{{ user.firstname }} {{ user.lastname }}</h3>
                <p class="user-location">{{ user.location }}</p>
                <p class="user-join">Member since {{ user.joined_on }}</p>
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
                   :class="['btn', isFollowing ? 'following' : 'follow']"
                    @click="toggleFollow"
                >
                    {{ isFollowing ? 'Following' : 'Follow' }}
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

    // State variables
    const user = ref({
    firstname: '',
    lastname: '',
    location: '',
    biography: '',
    joined_on: '',
    profile_photo: '',
    posts: [],
    });

    const postCount = ref(0);
    const isFollowing = ref(false); // Whether the current user is following
    const followerCount = ref(0); // Default to zero

    // Function to get user details and initialize follower count
    function getUserDetails() {
    const token = sessionStorage.getItem('jwt');

    if (!token) {
        router.push({ name: 'login' }); // Redirect if JWT is missing
        return;
    }

    fetch(`/api/v1/users/${user_id}`, {
        method: 'GET',
        headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('jwt')}`, // Ensure JWT
        },
    })
    .then((response) => response.json())
    .then((data) => {
        user.value = data;
        postCount.value = data.posts.length;
    })
    .catch((error) => {
        console.error('Error fetching user details:', error);
    });
    }

    const toggleFollow = () => {
    isFollowing.value = !isFollowing.value; // Toggle the state
    };

    onMounted(() => {
    getUserDetails(); // Fetch user details on component mount
    });
</script>



<style scoped>
.profileContainer {
    margin: 55px;
    background-color: #f4eee5;
}

.profileHeader {
    display: grid;
    grid-template-columns: 50px 800px 50px;
    gap: 100px;
}

.user-name {
    font-weight: 400;
}

.user-location {
    padding-top: 10px;
}

.user-join {
    padding-bottom: 10px;    
}

.profileBody {
    display: grid;
    grid-template-columns: repeat(3, 200px);
    column-gap: 240px;
    row-gap: 25px;
}

.post-photo {
    width: 400px;
    height: 400px;
}

.user-details {
    padding: 0px 0px 0px 100px;
}

.user-profile_photo {
    width: 200px;
    height: 200px;
    border-radius: 50%;
}

.social-details {
    text-align: center;
}

.social {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 50px;
    padding-bottom: 25px;
}

.follower-no, .post-no {
    font-size: 20px;
}

.follower-title, .post-title {
    font-size: 15px;
    color: rgb(186, 186, 186);
}

.follow {
  background-color: #e18e4a; 
  color: white;
}

.following {
  background-color: #7dd220; 
  color: white;
}

.btn {
    padding: 7px 55px;
    color: white;
    background-color: #4a90e1;
    text-decoration: none;
    border-radius: 5px;
    cursor: pointer;
    transition: 0.3s ease-in-out;
}

.btn:hover {
    background-color: #7dd220;
}
</style>
