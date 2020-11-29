<template>
  <div class="container register">
    <div class="row">
      <div class="col-12">
        <img class="auth-logo" src="./../../assets/images/logo.png" />
      </div>
    </div>

    <div class="row">
      <form class="col-md-12 pl-4 pr-4" novalidate @submit.prevent="onRegister">
        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="user-circle" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': username}">
              <label>Your Username</label>
              <input name="username" v-model="username" v-validate="'required|min:4'"/>
            </div>
          </div>
          <p class="form-error text-center" v-show="errors.has('username')">
            {{errors.first('username')}}
          </p>
        </div>

        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="envelope" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': email}">
              <label>Email Address</label>
              <input name="email" v-model="email" v-validate="'required|email'" />
            </div>
          </div>
          <p class="form-error text-center" v-show="errors.has('email')">
            {{errors.first('email')}}
          </p>
        </div>

        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="lock" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': password}">
              <label>Type your password</label>
              <input name="password" v-model="password" :type="showPassword ? 'text' : 'password'" v-validate="'required|min:8|verify_password'" ref="password" />
            </div>
            <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" @click="showPassword = !showPassword" />
          </div>
          <p class="form-error text-center" v-show="errors.has('password')">
            {{errors.first('password')}}
          </p>
        </div>

        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="lock" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': repeatPassword}">
              <label>Repeat your password for security</label>
              <input name="repeatPassword" v-model="repeatPassword" :type="showRepeatPassword ? 'text' : 'password'" data-vv-as="Password" v-validate="'required|confirmed:password'" />
            </div>
            <font-awesome-icon :icon="showRepeatPassword ? 'eye-slash' : 'eye'" @click="showRepeatPassword = !showRepeatPassword" />
          </div>
          <p class="form-error text-center" v-show="errors.has('repeatPassword')">
            {{errors.first('repeatPassword')}}
          </p>
        </div>

        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="envelope" />
            <div class="custom-dropdown-container">
              <label>User Type</label>
              <b-dropdown>
                <template slot="button-content">
                  {{userType.text}}
                </template>
                <b-dropdown-item v-for="type in userTypes" :key="type.key" @click="setUserType(type)">{{type.text}}</b-dropdown-item>
              </b-dropdown>
            </div>
            <font-awesome-icon icon="caret-down" />
          </div>
        </div>

        <div class="more-options">
          <span>MORE OPTIONS</span>
        </div>

        <div class="form-group text-center">
          <p v-google-signin-button="clientId" class="google-signin-button mt-3">
            Sign up with
            <span>
              <font-awesome-icon :icon="['fab', 'google']" />
            </span>
          </p>
        </div>

        <div class="form-group agree-tos">
          <b-form-checkbox name="tosAgree" v-model="agree" value="1" unchecked-value="0" v-validate="'required'" v-bind:class="{'form-error': agreeError}">
            By Signing-up you agree to our <a href="/">Terms of Service</a>
          </b-form-checkbox>
        </div>

        <div class="form-group text-center mt-4">
          <button type="submit" class="btn btn-register" :disabled="registering">
            <span v-if="!registering">Signup Now</span>
            <span v-else>Registering...</span>
          </button>
        </div>
      </form>

      <div class="col-md-12 mt-3 mb-5 text-center">
        <span class="already-registered">ALREADY REGISTERED?</span>
        <router-link to="/login" class="login-link">
          LOGIN &nbsp;<font-awesome-icon icon="arrow-right"/>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jQuery';
  import GoogleSignInButton from 'vue-google-signin-button-directive'

  export default {
    name: "Register",
    data: function() {
      return {
        username: '',
        email: '',
        password: '',
        userType: {
          key: 'home-buyer',
          text: 'Home Buyer'
        },
        userTypes: [
          {
            key: 'home-buyer',
            text: 'Home Buyer'
          }, {
            key:'home-seller',
            text: 'Home Seller'
          }, {
            key: 'realtor',
            text: 'Realtor'
          }, {
            key:'loan-officer',
            text:'Loan Officer'
          }
        ],
        showPassword: false,
        repeatPassword: '',
        showRepeatPassword: false,
        agree: '0',
        agreeError: false,
        clientId: '405077832351-lp98abenhf75jsj416g6126osglhhk2u.apps.googleusercontent.com',
        registering: false
      }
    },
    directives: {
      GoogleSignInButton
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
      onRegister: function() {
        if(this.agree == '1')
          this.agreeError = false;
        else
          this.agreeError = true;

        this.$validator.validateAll().then(result => {
          if (result && !this.agreeError) {
            this.registering = false;

            this.$store.dispatch('auth/register', {
              username: this.username,
              email: this.email,
              password1: this.password,
              password2: this.repeatPassword,
              user_type: this.userType.key
            }).then(response => {
              if(response.status == 'success') {
                this.$router.push('dashboard');
              }
            }).catch(error => {
              this.registering = false;

              this.$toastr('error', 'Unable to sign up with provided information.', 'Error!')
            })
          }
        })
      },
      setUserType: function(type) {
        this.userType = type;
      },
      OnGoogleAuthSuccess (idToken) {
        // Receive the idToken and make your magic with the backend
      },
      OnGoogleAuthFail (error) {
        // Receive the error when the google auth failed
      }
    },
    watch: {
      agree: function(val) {
        if(val == '1')
          this.agreeError = false;
        else
          this.agreeError = true;
      }
    }
  }
</script>
