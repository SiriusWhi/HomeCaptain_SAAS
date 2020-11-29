import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index'
import './registerServiceWorker'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue);

import VeeValidate from 'vee-validate'
Vue.use(VeeValidate);

VeeValidate.Validator.extend('verify_password', {
  getMessage: field => `The password must contain at least: 1 uppercase letter, 1 lowercase letter, 1 number, and one special character (E.g. , . _ & ? etc)`,
  validate: value => {
    var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    return strongRegex.test(value);
  }
});

import VueToastr from '@deveodk/vue-toastr'
import '@deveodk/vue-toastr/dist/@deveodk/vue-toastr.css'
Vue.use(VueToastr, {
  defaultPosition: 'toast-top-right',
  defaultType: 'info',
  defaultTimeout: 3000
});

import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserCircle, faLock, faEye, faEyeSlash, faFolder, faUser, faHandshake,
          faCaretRight, faCaretDown, faQuestionCircle, faSearch, faCommentAlt, faBell,
          faPowerOff, faArrowRight, faEnvelope, faPlusCircle, faPen, faUpload,
          faCaretUp, faPaperPlane } from '@fortawesome/free-solid-svg-icons'
import { faGoogle } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(faUserCircle, faLock, faEye, faEyeSlash, faFolder, faUser, faHandshake,
            faCaretRight, faCaretDown, faQuestionCircle, faSearch, faCommentAlt, faBell,
            faPowerOff, faArrowRight, faEnvelope, faGoogle, faPlusCircle, faPen, faUpload,
            faCaretUp, faPaperPlane);
Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
