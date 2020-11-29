import Vue from "vue";
import Router from "vue-router";
import store from "./store";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Dashboard from "./views/Dashboard.vue";
import Archive from "./views/Archive.vue";
import HomeBuying from "./views/HomeBuying.vue";
import HomeSelling from "./views/HomeSelling.vue";
import Search from "./views/Search.vue";
import Favorites from "./views/Favorites.vue";
import Recommend from "./views/Recommend.vue";
import LoanOfficers from "./views/LoanOfficers.vue";
import Concierge from "./views/Concierge.vue";
import Recover from "./views/AccountRecovery.vue";
import Reset from "./views/Reset.vue";

Vue.use(Router);

const router = new Router({
  routes: [
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
    {
      path: "/dashboard",
      name: "dashboard",
      component: Dashboard,
    },
    {
      path: "/archive",
      name: "archive",
      component: Archive,
    },
    {
      path: "/selling",
      name: "homeSelling",
      component: HomeSelling,
    },
    {
      path: "/buying",
      name: "homeBuying",
      component: HomeBuying,
    },
    {
      path: "/search",
      name: "search",
      component: Search,
    },
    {
      path: "/favorites",
      name: "favorites",
      component: Favorites,
    },
    {
      path: "/recommend",
      name: "recommend",
      component: Recommend,
    },
    {
      path: "/loan-officers",
      name: "loanOfficers",
      component: LoanOfficers,
    },
    {
      path: "/concierge",
      name: "concierge",
      component: Concierge,
    },
    {
      path: "/recover",
      name: "recover",
      component: Recover,
    },
    {
      path: "/reset",
      name: "reset",
      component: Reset,
    },
    {
      path: "/",
      redirect: { name: "dashboard" },
    },
  ],
});

router.beforeEach((to, from, next) => {

  if (store.state.idToken === null) {
    if (to.name === "dashboard") {
      return next({ name: "login" });
    }
  }

  if (store.state.idToken !== null) {
    if (to.name === "login" || to.name === "register") {
      return next({ name: "dashboard" });
    }
  }

  next();
});

export default router;
