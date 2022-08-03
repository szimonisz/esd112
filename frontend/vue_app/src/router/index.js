import { createRouter, createWebHistory } from 'vue-router'
import UploadDirectory from '../components/UploadDirectory.vue'
import ViewDirectory from '../components/ViewDirectory.vue'

const routes = [
  { 
    path: '/', 
    redirect: 
      { 
        name: 'upload' 
      } 
  },
  {
    path: '/upload',
    name: 'upload',
    component: UploadDirectory 
  },
  {
    path: '/view',
    name: 'view',
    component: ViewDirectory 
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
