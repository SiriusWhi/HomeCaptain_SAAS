<template>
  <div class="login">
    <b-alert
      variant="danger"
      dismissible
      :show="showDismissibleAlert"
      @dismissed="showDismissibleAlert=false"
    >{{registerError}}</b-alert>
    <img src="../../public/img/logo.png" class="login-logo" alt="Logo">
    <form class="form-signin" novalidate @submit.prevent="reset">
      <img class="mb-4" src alt width="72" height="72">
      <label for="inputPassword" class="sr-only">Password</label>
      <div class="input-wrapper">
        <input
          :type="inputType"
          name="password1"
          class="login-input hc-input password-input"
          placeholder="Password"
          autocomplete="new-password"
          v-model="password1"
          data-error="password"
          v-validate="'required|min:8'"
          @input="validateBeforeSubmit()"
          data-vv-delay="5000"
          ref="password"
        >
        <i class="fas fa-lock login-icon"></i>
        <img
          src="../../public/img/reveal.png"
          class="password-peek"
          @click="inputType == 'password' ? inputType = 'text' : inputType = 'password'"
          alt="Show Password"
        >
        <span
          v-show="errors.has('password1')"
          class="help is-danger login-errors"
        >{{ errors.first('password1') }}</span>
      </div>
      <label for="inputPassword" class="sr-only">Confirm Password</label>
      <div class="input-wrapper">
        <input
          :type="inputType"
          name="password2"
          class="login-input hc-input password-input"
          placeholder="Confirm Password"
          autocomplete="new-password"
          v-model="password2"
          data-error="confirm password"
          v-validate="'required|confirmed:password'"
          @input="validateBeforeSubmit()"
          data-vv-delay="5000"
        >
        <i class="fas fa-lock login-icon"></i>
        <img
          src="../../public/img/reveal.png"
          class="password-peek"
          @click="inputType == 'password' ? inputType = 'text' : inputType = 'password'"
          alt="Show Password"
        >
        <span
          v-show="errors.has('password2')"
          class="help is-danger login-errors"
        >{{ errors.first('password2') }}</span>
      </div>
      <button
        class="submit"
        :class="{submitDisabled: inputsInvalid}"
        type="submit"
        :disabled="inputsInvalid"
      >Reset Password</button>
      <router-link :to="{name:'login'}" class="to-login text-center pointer text-uppercase">
        Login
        <i class="fas fa-arrow-right"></i>
      </router-link>
    </form>
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
  name: "Reset",
  components: {},
  data() {
    return {
      password1: "",
      password2: "",
      inputType: "password",
      inputsInvalid: true,
      showDismissibleAlert: false,
      showLoading: false,
    };
  },

  methods: {
    reset() {
      const formData = {
        password1: this.password1,
        password2: this.password2
      };
      console.log(formData);
      this.inputType = "password";
      axios
        .post("/api/auth/password/reset/confirm/", formData)
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
</style>

