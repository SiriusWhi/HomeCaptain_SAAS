<template>
  <div class="login">
    <b-alert
      variant="danger"
      dismissible
      :show="showDismissibleAlert"
      @dismissed="showDismissibleAlert=false"
    >{{registerError}}</b-alert>
    <img src="../../public/img/logo.png" class="login-logo" alt="Logo">
    <form class="form-signin" novalidate @submit.prevent="recover">
      <img class="mb-4" src alt width="72" height="72">
      <label for="inputEmail" class="sr-only">Username</label>
      <label for="inputEmail" class="sr-only">Email address</label>
      <div class="input-wrapper">
        <input
          type="email"
          name="email"
          id="inputEmail"
          class="login-input hc-input email-input"
          placeholder="Email address"
          autocomplete="email"
          v-model="email"
          data-error="email"
          v-validate="'required|email'"
          data-vv-delay="5000"
          @input="validateBeforeSubmit()"
          autofocus
        >
        <i class="fas fa-envelope login-icon"></i>
        <span
          v-show="errors.has('email')"
          class="help is-danger login-errors"
        >{{ errors.first('email') }}</span>
      </div>

      <button
        class="submit"
        :class="{submitDisabled: inputsInvalid}"
        type="submit"
        :disabled="inputsInvalid"
      >Submit</button>
    </form>
    <router-link :to="{name:'login'}" class="to-login text-center pointer text-uppercase">
        <i class="fas fa-arrow-left"></i>
        Back
      </router-link>
    <div class="loading-wrapper" v-show="showLoading">
        <img src="../../public/img/loading.svg" alt="">
      </div>
  </div>
</template>

<script>
// @ is an alias to /src

import axios from "../axios-auth";
import { mapState, mapActions } from "vuex";

export default {
  name: "Recover",
  components: {},
  data() {
    return {
      email: "",
      inputsInvalid: true,
      showDismissibleAlert: false,
      showLoading: false,
    };
  },

  methods: {
    recover() {
      const formData = {
        email: this.email,
      };
      console.log(formData);
      axios
        .post("/api/auth/password/reset/", formData)
        .then(res => {
          console.log(res);
          this.showLoading = false;
        })
        .catch(error => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    validateBeforeSubmit() {
      this.$validator.validateAll().then(result => {
        if (result) {
          this.inputsInvalid = false;
          return;
        }
        this.inputsInvalid = true;
      });
    }
  },

  watch: {
    idToken: function(token) {
      if (token !== null) {
        this.$router.push({ name: "login" });
      }
    },
    registerError: function(error) {
      if (error !== null) {
        this.showDismissibleAlert = true;
      }
    },
    loading: function(load) {
      if (load === true) {
        //alert(1);
        this.showDismissibleAlert = false;
        this.showLoading = true;
      } else {
        this.showLoading = false;
        this.showDismissibleAlert = true;
      }
    }
  },

  computed: {
    ...mapState(["idToken", "registerError", "loading"])
  },

  mounted() {
  }
};
</script>

<style scoped>

.login {
    height: 388px;
}

</style>

