<template>
  <div class="container login">
    <div class="row">
      <div class="col-12">
        <img class="auth-logo" src="./../../assets/images/logo.png" />
      </div>
    </div>

    <div class="row">
      <form class="col-md-12 pl-4 pr-4" novalidate @submit.prevent="onLogin">
        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="user-circle" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': username}">
              <label>Username</label>
              <input name="username" v-model="username" v-validate="'required'"/>
            </div>
          </div>
          <p class="form-error text-center" v-show="errors.has('username')">
            {{errors.first('username')}}
          </p>
        </div>

        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="lock" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': password}">
              <label>Password</label>
              <input name="password" v-model="password" :type="showPassword ? 'text' : 'password'" v-validate="'required'"/>
            </div>
            <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" @click="showPassword = !showPassword" />
          </div>
          <p class="form-error text-center" v-show="errors.has('password')">
            {{errors.first('password')}}
          </p>
        </div>

        <div class="form-group text-center mt-5">
          <button type="submit" class="btn btn-login" :disabled="signing">
            <span v-if="!signing">Login</span>
            <span v-else>Logging in...</span>
          </button>
        </div>
      </form>

      <div class="col-md-12 mt-3 mb-5 text-center">
        <router-link to="/forgot-password" class="recovery-link">Account Recovery</router-link>
        <br/>
        <router-link to="/register" class="register-link mt-3">
          SIGNUP &nbsp;<font-awesome-icon icon="arrow-right" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jQuery';

  export default {
    name: "Login",
    data: function() {
      return {
        username: '',
        password: '',
        showPassword: false,
        signing: false
      }
    },
    mounted() {
      $(".auth .custom-input-container input").focusin((e) => {
        $(e.target).parent().addClass("input-focused");
      });

      $(".auth .custom-input-container input").focusout((e) => {
        $(e.target).parent().removeClass("input-focused");
      });
    },
    methods: {
      onLogin: function() {
        this.$validator.validateAll().then(result => {
          if (result) {
            this.signing = true;

            this.$store.dispatch('auth/login', {
              username: this.username,
              password: this.password
            }).then(response => {
              if(response.status == 'success') {
                this.$router.push('dashboard');
              }
            }).catch(error => {
              this.signing = false;

              this.$toastr('error', 'Unable to log in with provided credentials.', 'Error!')
            })
          }
        })
      }
    }
  }
</script>
