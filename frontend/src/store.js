import Vue from "vue";
import Vuex from "vuex";
import VuexPersistence from "vuex-persist";
import axios from "./axios-auth";

import router from "./router";

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
  reducer: state => {
    return { idToken: state.idToken };
  }
});

export default new Vuex.Store({
  state: {
    idToken: null,
    userId: null,
    user: null,
    loginError: null,
    registerError: null,
    loading: false,
  },

  mutations: {
    authUser(state, userData) {
      state.idToken = userData.token;
      state.userId = userData.userId;
      state.loading = false;
    },

    clearAuthData(state) {
      state.idToken = null;
      state.loading = false;
    },

    loginError(state, errorData) {
      state.loginError = errorData.errorString;
      state.loading = false;
    },

    registerError(state, errorData) {
      state.registerError = errorData.errorString;
      state.loading = false;
    },

    loginRequest(state) {
      state.loading = true;
    },
  },

  actions: {
    signup({ commit }, authData) {
      commit("loginRequest");
      axios
        .post("/api/auth/registration/", {
          username: authData.username,
          email: authData.email,
          password1: authData.password1,
          password2: authData.password2,
        })
        .then((res) => {
          console.log(res);
          commit("authUser", {
            token: res.data.key,
          });
        })
        .catch((error) => {
          commit("registerError", {
            errorString: error.response.data.username[0],
          });
        });
    },

    googleAuth({ commit }, googleAuthToken) {
      console.log(typeof googleAuthToken);
      console.log(googleAuthToken);
      axios
        .post("/api/auth/google/", {
          access_token: googleAuthToken,
        })
        .then((res) => {
          console.log(res);
          commit("authUser", {
            token: res.data.key,
          });
        })
        .catch(error => console.log(error));
    },

    login({ commit }, authData) {
      commit("loginRequest");
      axios
        .post("/api/auth/login/", {
          username: authData.username,
          password: authData.password,
        })
        .then((res) => {
          commit("authUser", {
            token: res.data.key,
          });
        })
        .catch((error) => {
          commit("loginError", {
            errorString: "Incorrect credentials",
          });
        });
    },
    logout({ commit }, tokenString) {
      commit("loginRequest"); // loading
      axios
        .post("/api/auth/logout/", {
          key: tokenString,
        })
        .then((res) => {
          console.log(res);
          commit("clearAuthData");
          router.push({ name: "login" });
        })
        .catch(error => console.log(error));
    },
  },
  getters: {},
  plugins: [vuexLocal.plugin],
});
