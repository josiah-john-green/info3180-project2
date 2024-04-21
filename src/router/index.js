import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddRegistrationFormView from '../views/AddRegistrationFormView.vue'
import AddLoginFormView from '../views/AddLoginFormView.vue'
import ExploreView from '../views/ExploreView.vue'
import AddPostFormView from '../views/AddPostFormView.vue'

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
      path: '/explore',
      name: 'ExploreView',
      component: ExploreView
    },
    {
      path: '/post/new',
      name: 'AddPostForm',
      component: AddPostFormView
    }
  ]
})

export default router
