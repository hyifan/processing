import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/processing'
  },
  {
    path: '/processing',
    component: () => import('../views/Processing'),
  },
  {
    path: '/knowledge',
    redirect: '/knowledge/gray',
    component: () => import('../views/Knowledge'),
    children: [{
      path: 'gray',
      component: () => import('../views/Knowledge/gray.vue')
    }, {
      path: 'histogram',
      component: () => import('../views/Knowledge/histogram.vue')
    }, {
      path: 'space',
      component: () => import('../views/Knowledge/space.vue')
    }]
  },
  {
    path: '/login',
    component: () => import('../views/SingleView/login.vue'),
  },
  {
    path: '*',
    component: () => import('../views/SingleView/404.vue'),
  }
]

/**
 * 重写路由的push方法
 */
const routerPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this, location).catch(error => error)
}

const router = new VueRouter({
  routes
})

export default router
