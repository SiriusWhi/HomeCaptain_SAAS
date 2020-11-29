import Vue from 'vue'
import Router from 'vue-router'
import store from './store/index';

import Login from './views/Auth/Login.vue';
import Register from './views/Auth/Register.vue';
import ForgotPassword from './views/Auth/Forgot-Password.vue';
import ResetPassword from './views/Auth/Reset-Password.vue';
import Dashboard from './views/Main/Activity/Dashboard.vue';
import HomeBuying from './views/Main/Activity/HomeBuying.vue';
import HomeSelling from './views/Main/Activity/HomeSelling.vue';

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    }, {
      path: '/register',
      name: 'register',
      component: Register
    }, {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword
    }, {
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPassword
    }, {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiredAuth: true }
    }, {
      path: '/home-buying',
      name: 'home-buying',
      component: HomeBuying,
      meta: { requiredAuth: true }
    }, {
      path: '/home-selling',
      name: 'home-selling',
      component: HomeSelling,
      meta: { requiredAuth: true }
    },

    // redirect
    {
      path: '*',
      redirect: '/login'
    }
  ]
});

router.beforeEach((to, from, next) => {
  let isAuthenticated = store.getters['auth/isAuthenticated'];
  if (to.name == 'login') {
    if(isAuthenticated) {
      return next({name: 'dashboard'});
    }
  } else {
    if (to.matched.some(m => m.meta.requiredAuth) && !isAuthenticated) {
      return next({name: 'login'});
    }
  }

  next();
});

export default router;

