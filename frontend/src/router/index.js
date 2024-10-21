import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/MainView.vue')
    },
    {
      path: '/register',
      name: 'register',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Auth/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/Auth/LoginView.vue')
    },

  ]
})

export default router






// import { createMemoryHistory, createRouter } from 'vue-router'

// import RegisterView from '.views/Auth/RegisterView.vue'
// import LoginView from './Auth/LoginView.vue'
// import MainView from './MainView.vue'

// const routes = [
//   { path: '/', component: MainView },
//   { path: '/register', component: RegisterView },
//   { path: '/login', component: LoginView },
// ]

// const router = createRouter({
//   history: createMemoryHistory(),
//   routes,
// })

// export default router