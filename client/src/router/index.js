import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/table',
    name: 'table',
    component: () => import('../views/TableView.vue')
  },
  {
    path: '/add',
    name: 'create',
    component: () => import('../views/CreateView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
