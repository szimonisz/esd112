import { createRouter, createWebHistory } from 'vue-router'
import MyHelen from '../components/MyHelen.vue'
import UploadDirectory from '../components/UploadDirectory.vue'

const routes = [
  {
    path: '/helen',
    name: 'helen',
    component: MyHelen
  },
  {
    path: '/upload',
    name: 'upload',
    component: UploadDirectory 
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
