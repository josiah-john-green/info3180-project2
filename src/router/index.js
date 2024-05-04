import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AddRegistrationFormView from '../views/AddRegistrationFormView.vue';
import AddLoginFormView from '../views/AddLoginFormView.vue';
import AddLogoutView from '../views/AddLogoutView.vue';
import ExploreView from '../views/ExploreView.vue';
import AddNewPostFormView from '../views/AddNewPostFormView.vue';
import ProfileView from '../views/ProfileView.vue';
import PostFormView from '../views/PostFormView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Ensure this is set up correctly
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    { 
      path: '/register',
      name: 'register',
      component: AddRegistrationFormView,
    },
    {
      path: '/login',
      name: 'login',
      component: AddLoginFormView,
    },
    {
      path: '/logout',
      name: 'logout',
      component: AddLogoutView,
    },
    {
      path: '/explore',
      name: 'explore',
      component: ExploreView,
    },
    {
      path: '/post/new',
      name: 'post',
      component: AddNewPostFormView,
    },
    {
      path: '/post/:post_id',
      name: 'profilepost',
      component: PostFormView,
    },
    {
      path: '/users/:user_id', // Ensure this path matches with your intention
      name: 'profile',
      component: ProfileView,
      props: true, // Pass route params as component props
    },
  ],
});

export default router;
