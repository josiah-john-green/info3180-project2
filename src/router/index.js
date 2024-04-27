import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddRegistrationFormView from '../views/AddRegistrationFormView.vue'
import AddLoginFormView from '../views/AddLoginFormView.vue'
import AddLogoutView from '../views/AddLogoutView.vue'
import ExploreView from '../views/ExploreView.vue'
import AddNewPostFormView from '../views/AddNewPostFormView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    { 
      path: '/register',
      name: 'AddRegistrationForm',
      component: AddRegistrationFormView
    },
    {
      path: '/login',
      name: 'AddLoginForm',
      component: AddLoginFormView
    },
    {
      path: '/logout',
      name: 'AddLogoutView',
      component: AddLogoutView
    },
    {
      path: '/explore',
      name: 'ExploreView',
      component: ExploreView
    },
    {
      path: '/post/new',
      name: 'AddNewPostForm',
      component: AddNewPostFormView
    },
    {
      path: '/users/:userid',
      name: 'ProfileView',
      component: ProfileView
    }
  ]
})

export default router
