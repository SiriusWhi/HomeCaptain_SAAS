import Vue from "vue";
import ToggleButton from "vue-js-toggle-button";
import vSelect from "vue-select";
import VueToastr from "@deveodk/vue-toastr";
import "@deveodk/vue-toastr/dist/@deveodk/vue-toastr.css";

import "./registerServiceWorker";

import axios from "axios";
import _ from "lodash";
import VeeValidate from "vee-validate";

import BootstrapVue from "bootstrap-vue";
import simplebar from "simplebar";
import "simplebar/dist/simplebar.min.css";

import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

import App from "./App.vue";
import router from "./router";
import store from "./store";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import VueCookies from "vue-cookies";
import * as VueGoogleMaps from "vue2-google-maps";
import instance from "./axios-auth";

Vue.use(VueGoogleMaps, {
  load: {
    key: "AIzaSyBE2Jue91YZwSGmBDA9UMeqc5sa_57HTSI",
    libraries: "places",
  },
});

axios.defaults.headers.get["Content-Type"] = "application/json";
axios.defaults.headers.get.Accept = "application/json";

instance.interceptors.request.use((config) => {
  if (store.state.idToken) {
    config.headers.Authorization = `Token ${store.state.idToken}`;
  }
  return config;
});

Vue.use(VeeValidate);
Vue.use(BootstrapVue);
Vue.use(ToggleButton);
Vue.component("v-select", vSelect);
Vue.use(VueCookies);
Vue.use(VueToastr, {
  defaultPosition: "toast-top-center",
  defaultType: "info",
  defaultTimeout: 3000,
});
Vue.use(_);
Vue.component("vue-bootstrap-typeahead", VueBootstrapTypeahead);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount("#app");
