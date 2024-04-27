<template> 
    <div class="profileContainer">
        <div class="card shadow p-4 mb-5 bg-white rounded profileHeader">
            <img v-bind:src="user.profile_photo" class="user-profile_photo"> 

            <div class="user-details">
                <h3 class="user-name"> {{ user.firstname }} {{ user.lastname }} </h3>
                <p class="user-location"> {{ user.location }} </p>
                <p class="user-join"> Member since {{ user.joined_on }} </p>
                <p class="user-info"> {{ user.biography }}</p>
            </div>

            <div class="social-details">
                <div class="social">
                    <div class="post-count"> 
                        <p class="post-no"> {{ postCount }}</p>
                        <p class="post-title">Posts</p>
                    </div>
                    <div class="follower-count"> 
                        <p class="follower-no">{{ followerCount }}</p>
                        <p class="follower-title">Followers</p>
                    </div>
                </div>

                <button class="btn" @click="followUser(user.id)">
                    {{ followerCount > 0 ? 'Following' : 'Follow' }}
                </button>
            </div>       
        </div>

        <div class="profileBody">
            <div class="post-grid" v-for="post in user.posts" :key="post.id">                  
                <img v-bind:src="post.photo" class="card shadow post-photo"> 
            </div>
        </div>  
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import router from '../router/index.js';
    
    let user = ref({
        firstname: '',
        lastname: '',
        location: '',
        biography: '',
        joined_on: '',
        profile_photo: '',
        posts: []
    });
    
    let postCount = ref(0);
    let followerCount = ref(0); // Initialize follower count with 0
    
    // Function to handle follow action
    function followUser(userid) {
        const token = sessionStorage.getItem('jwt');

        if (!token) {
            return router.push({ name: 'AddLoginForm' });
        }

        fetch(`/api/users/${userid}/follow`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                // Increment follower count on successful follow
                followerCount.value++;
                return response.json();
            } else {
                throw new Error('Failed to follow user');
            }
        })
        .then(data => {
            console.log(data.message); // You can handle success message here if needed
        })
        .catch(error => {
            console.error('Error following user:', error);
        });
    }

    // Fetch user details including follower count from the API when the component is mounted
    function getUserDetails(){
        const token = sessionStorage.getItem('jwt')

        if (token == null){
            return router.push({ name: 'AddLoginForm'})
        }

        const tokenParts = token.split('.')
        const payload = JSON.parse(atob(tokenParts[1]))
        const userId = payload['subject']

        fetch(`/api/v1/users/${userId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            user.value = data;
            postCount.value = data.posts.length;
            followerCount.value = data.followers || 0; // Set to 0 if followers data is not available
        })
        .catch(error => {
            console.error('Error fetching user details:', error);
        });
    }

    onMounted(() => {
        getUserDetails();
    });
</script>

<style scoped>

.profileContainer{
    margin: 55px;
    background-color: #f4eee5;
}

.profileHeader{
    display: grid;
    grid-template-columns: 50px 800px 50px;
    gap: 100px;
}

.user-name{
    font-weight: 400;
}

.user-location{
    padding-top: 10px;
}

.user-join{
    padding-bottom: 10px;    
}

.profileBody{
    display: grid;
    grid-template-columns: repeat(3, 200px);
    gap: 250px;
}

.post-photo{
    width: 400px;
    height: 400px;
}

.user-details{
    padding: 0px 0px 0px 100px;
    
}

.user-profile_photo
{
    width: 200px;
    height: 200px;
    border-radius: 50%;
}

.social-details{
    text-align: center;
}

.social{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 50px;
    padding-bottom: 25px;
}

.follower-no, .post-no{
    font-size: 20px; 
}

.follower-title, .post-title{
    font-size: 15px;
    color: rgb(186, 186, 186);
}


.btn {
    padding: 7px 55px;
    color: white;
    background-color: #4a90e1;
    text-decoration: none;
    border-radius: 5px;
}


</style>