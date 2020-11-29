<template>
  <div class="login">
    <b-alert
      variant="danger"
      dismissible
      :show="showDismissibleAlert"
      @dismissed="showDismissibleAlert=false"
    >{{registerError}}</b-alert>
    <img src="../../public/img/logo.png" class="login-logo" alt="Logo">
    <form class="form-signin" novalidate @submit.prevent="register">
      <img class="mb-4" src alt width="72" height="72">
      <label for="inputEmail" class="sr-only">Username</label>
      <div class="input-wrapper">
        <input
          type="text"
          name="username"
          class="login-input hc-input user-input"
          placeholder="Username"
          v-model="username"
          data-error="username"
          v-validate="'required|min:4'"
          data-vv-delay="5000"
          @input="validateBeforeSubmit()"
          autofocus
        >
        <i class="fas fa-user-circle login-icon"></i>
        <span
          v-show="errors.has('username')"
          class="help is-danger login-errors"
        >{{ errors.first('username') }}</span>
      </div>
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
      <div class="options">
        <span class="options-span"></span>
        <span class="text-uppercase more-options">more options</span>
        <span class="options-span"></span>
      </div>
      <p class="google-reg text-center" v-google-signin-button="clientId">
        <span class="register-google">Sign up with</span>
        <span class="google-icon">
          <i class="fab fa-google"></i>
        </span>
      </p>
      <div class="tos">
        <input
          type="checkbox"
          name="tos"
          v-validate="'required'"
          @change="validateBeforeSubmit()"
          class="tos-checkbox"
        >
        <label class="tos-label">
          By Signing-up you agree to our
          <a href>Terms of Service</a>
        </label>
        <span
          v-show="errors.has('tos')"
          class="help is-danger login-errors tos-errors"
          data-error="TOS"
        >{{ errors.first('tos') }}</span>
      </div>
      <button
        class="submit"
        :class="{submitDisabled: inputsInvalid}"
        type="submit"
        :disabled="inputsInvalid"
      >Signup Now</button>
      <p class="mont text-uppercase text-center already">Already Registered?</p>
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
import $ from "jquery";

import GoogleSignInButton from "../google-signin-directive";

export default {
  name: "Register",
  components: {},
  directives: {
    GoogleSignInButton
  },
  data() {
    return {
      username: "",
      email: "",
      password1: "",
      password2: "",
      inputType: "password",
      inputsInvalid: true,
      showDismissibleAlert: false,
      showLoading: false,
      clientId:
        "405077832351-lp98abenhf75jsj416g6126osglhhk2u.apps.googleusercontent.com"
    };
  },

  methods: {
    register() {
      const formData = {
        username: this.username,
        email: this.email,
        password1: this.password1,
        password2: this.password2
      };
      console.log(formData);
      this.inputType = "password";
      this.$store.dispatch("signup", {
        username: formData.username,
        email: formData.email,
        password1: formData.password1,
        password2: formData.password2
      });
    },

    OnGoogleAuthSuccess(token) {
      // Receive the idToken and make your magic with the backend
      this.$store.dispatch("googleAuth", token);
    },

    OnGoogleAuthFail(error) {
      console.log(error);
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
    /*function errorMessage(){
      let i = 0;
      for (i=0; i<5; i++){
        if($(".login-errors").eq(i).html().indexOf("required" !== -1)){
          let a = $("input").eq(i).attr("data-error");
          let b = $(".login-errors").eq(i).html("The "+a+" field is required");
        }
      }
    };

    $("input").keyup(function(){
      //errorMessage();
    })*/
  }
};
</script>

<style scoped>
</style>

