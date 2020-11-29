<template>
  <div class="login login-actual">
    <b-alert variant="danger"
             dismissible
             :show="showDismissibleAlert"
             @dismissed="showDismissibleAlert=false">
      {{loginError}}
    </b-alert>
    <img
      src="../../public/img/logo.png"
      class="login-logo"
      alt="Logo"
    >
    <form class="form-signin" novalidate @submit.prevent="onSubmit">
      <img class="mb-4" src alt width="72" height="72">
      <label class="sr-only">Username</label>
      <div class="input-wrapper">
        <input
          type="text"
          class="login-input hc-input user-input"
          placeholder="Username"
          autocomplete="username"
          v-model="username"
          name="username"
          v-validate="'required|min:4'"
          data-vv-delay="2000"
          @input="validateBeforeSubmit()"
          autofocus
        >
        <i class="fas fa-user-circle login-icon"></i>
        <span
          v-show="errors.has('username')"
          class="help is-danger login-errors"
        >{{ errors.first('username') }}</span>
      </div>
      <label for="inputPassword" class="sr-only">Password</label>
      <div class="input-wrapper login-password">
        <input
          :type="inputType"
          id="inputPassword"
          name="password"
          class="login-input hc-input password-input"
          placeholder="Password"
          autocomplete="current-password"
          v-model="password"
          v-validate="'required|min:8'"
          data-vv-delay="2000"
          @input="validateBeforeSubmit();"
        >
        <i class="fas fa-lock login-icon"></i>
        <img
          src="../../public/img/reveal.png"
          class="password-peek"
          @click="inputType == 'password' ? inputType = 'text' : inputType = 'password'"
          alt="Show Password"
        >
        <span
          v-show="errors.has('password')"
          class="help is-danger login-errors"
        >{{ errors.first('password') }}</span>
      </div>
      <button
        class="submit login-btn"
        :class="{submitDisabled: inputsInvalid}"
        type="submit"
        :disabled="inputsInvalid"
      >Login</button>
      <p class="mont text-uppercase text-center already account-recover pointer"><router-link :to="{name: 'recover'}">Account Recovery</router-link></p>
      <router-link
        :to="{name:'register'}"
        class="to-login text-center pointer text-uppercase to-register"
      >Register
        <i class="fas fa-arrow-right"></i>
      </router-link>
      <router-link :to="{name:'reset'}" class="to-login text-center pointer text-uppercase d-none">
        <i class="fas fa-arrow-left"></i>
        Reset
      </router-link>
      <div class="loading-wrapper" v-show="showLoading">
        <img src="../../public/img/loading.svg" alt="">
      </div>
    </form>
  </div>
</template>

<script>
// @ is an alias to /src

import axios from "../axios-auth";
import { mapState, mapActions } from "vuex";

export default {
  name: "Login",
  components: {},
  data() {
    return {
      username: "",
      password: "",
      inputType: "password",
      inputsInvalid: true,
      showLoading: false,
      showDismissibleAlert: false,
    };
  },
  methods: {
    onSubmit() {
      let self = this;
      this.showLoading = true;
      const formData = {
        username: this.username,
        password: this.password
      };
      console.log(formData);
      this.inputType = "password";
      this.$store.dispatch("login", {
        username: formData.username,
        password: formData.password
      }).then(function() {})
        .catch(function() {});
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
        this.$router.push({ name: "dashboard" });
      }
    },
    loginError: function(error) {
      if (error !== null) {
        this.showDismissibleAlert = true;
        this.showLoading = false;
      }
    },
    loading: function(load) {
      if (load === true) {
        this.showDismissibleAlert = false;
        this.showLoading = true;
      } else {
        this.showLoading = false;
        this.showDismissibleAlert = true;
      }
    }
  },

  computed: {
    ...mapState(["idToken", "loginError", "loading"])
  }
};
</script>

<style scoped>
</style>

