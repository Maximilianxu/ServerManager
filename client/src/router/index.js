import Vue from 'vue';
import VueRouter from 'vue-router';
import store from "../store";
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import menu from './menu';
import NProgress from 'nprogress';
import _default from 'vuex';

Vue.use(VueRouter);

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/");
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/login");
};

const routes = [
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/register",
    name: "register",
    component: Register,
  },
  ...menu,
];

// 白名单，不会重定向
const whiteList = ['/login', '/register'];

console.log("routers:", routes);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  NProgress.start();
  document.title = to.meta.title;
  console.log("current auth or not:", store.getters.isAuthenticated);
  // 如果存在 token
  if (store.getters.isAuthenticated) {
    if (to.path === '/login') {
      // 跳过登录
      router.push({ path: '/' });
      NProgress.done();
    } else {
      next();
    }
  } else {
    if (whiteList.indexOf(to.path) > -1) {
      next();
    } else {
      // 直接跳转到登录，也可以给出提示
      router.push({ path: '/login' });
      NProgress.done();
    }
  }
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
