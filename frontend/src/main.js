import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

const app = createApp(App)
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('./components/create.vue')
    },
    {
      path: '/:channel',
      component: () => import('./components/websocket.vue')
    }
  ]
})
app.use(router)

app.mount('#app')
