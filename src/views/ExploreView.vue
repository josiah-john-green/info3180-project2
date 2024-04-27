<template> 

    <div class="postContainer">
        <div class="post-view" id="post-view">
            <div class="card shadow rounded" v-for="post in posts" :key="post.id">                  
                <h5 class="card-title">
                    <img :src="post.profile_photo" class="post-profile_photo"> 
                    <router-link :to="'/users/' + post.user_id" class="post-user">{{ post.username }}</router-link>
                </h5>
                
                <!-- Render post details -->
                <img v-bind:src="post.photo" class="post-photo">
                <div class="post-description">
                    <p class="post-caption">{{ post.caption }}</p>
                    <div class="post-details">
                        <p class="post-likes"><small class="text-muted">{{ post.likes }} likes</small></p>
                        <p class="post-date"><small class="text-muted">{{ post.created_on }}</small></p>
                    </div>
                </div>
            </div>
        </div>

        <div class="button">
            <router-link to="/post/new" class="btn"> New Post</router-link>
        </div>
    </div>
</template>
    
<script setup>
    import { ref, onMounted } from "vue";
    import router from '../router/index.js';
    
    let posts = ref([]);
    var errors = ref([]);
    
    // Fetch posts data from the API when the component is mounted
    function getPosts(){
        const token = sessionStorage.getItem('jwt')

        if (token == null){
            return router.push({ name: 'AddLoginForm'})
        }

        fetch("/api/v1/posts", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // Iterate over each post in the data array
            data.forEach(post => {
                // Push post object into posts array
                posts.value.push({
                    id: post.id,
                    user_id: post.user_id,
                    profile_photo: post.profile_photo,
                    username: post.username,
                    photo: post.photo,
                    caption: post.caption,
                    created_on: post.created_on,
                    likes: post.likes
                });
            });
        })
        .catch(function (error) {
            // Log any errors
            console.log(error);
            errors.value.push(error);
        });
    }

    onMounted(() => {
        // Call the function to fetch posts when the component is mounted
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

    padding: 10px;

}

.post-user{
    padding: 2px;
}

.post-view{
    width: 700px;
}

.post-view {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 50px;
}

.post-photo {
    width: 100%;
    height: 500px;
    object-fit: fill;
}

.post-user {
    padding-left: 10px;
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
}

.card-title {
    display: flex;
    flex-direction: row;
    font-size: 15px;
    padding: 20px;
}

.btn {
    padding: 7px 70px;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    background-color: #4a90e1;
}

</style>
  
  
  