import { createMemoryHistory, createRouter, createWebHistory } from 'vue-router'
import Home from '../src/components/Home.vue'
import Navbar from '../src/components/navbar.vue'
import Login from '../src/components/Login.vue'
import Register from '@/components/Register.vue'
import Upload from '@/components/Upload.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login/',
        name: 'Login',
        component: Login
    },
    {
        path: '/upload/',
        name: 'Upload',
        component: Upload,
        props: true
    }
]

function waitForEl(selector, timeout = 1500) {
  return new Promise((resolve) => {
    const start = performance.now()

    const check = () => {
      const el = document.querySelector(selector)
      if (el) return resolve(el)
      if (performance.now() - start > timeout) return resolve(null)
      requestAnimationFrame(check)
    }

    check()
  })
}

const router = createRouter({
  history: createWebHistory(),
  routes,
  async scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition

    if (to.hash) {
      const el = await waitForEl(to.hash)
      if (el) {
        return {
          el: to.hash,
          behavior: 'smooth',
          // opsional kalau navbar kamu fixed dan nutupin section
          top: 90,
        }
      }
    }

    return { top: 0 }
  },
})

export default router