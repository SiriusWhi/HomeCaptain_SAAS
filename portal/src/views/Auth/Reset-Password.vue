<template>
  <div class="container recovery">
    <div class="row">
      <div class="col-12">
        <img class="auth-logo" src="./../../assets/images/logo.png" />
      </div>
    </div>

    <div class="row">
      <form class="col-md-12 pl-4 pr-4" novalidate @submit="resetPassword">
        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="lock" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': password}">
              <label>Your new password</label>
              <input v-model="password" :type="showPassword ? 'text' : 'password'" />
            </div>
            <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" @click="showPassword = !showPassword" />
          </div>
        </div>

        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="lock" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': repeatPassword}">
              <label>Repeat your new password</label>
              <input v-model="repeatPassword" :type="showRepeatPassword ? 'text' : 'password'" />
            </div>
            <font-awesome-icon :icon="showRepeatPassword ? 'eye-slash' : 'eye'" @click="showRepeatPassword = !showRepeatPassword" />
          </div>
        </div>

        <div class="form-group text-center mt-5">
          <button type="submit" class="btn btn-recover">Save</button>
        </div>
      </form>

      <div class="col-md-12 mt-3 mb-5 text-center">
        <router-link to="/login" class="login-link">
          LOGIN &nbsp;<font-awesome-icon icon="arrow-right" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jQuery';

  export default {
    name: "Reset",
    data: function() {
      return {
        password: '',
        repeatPassword: '',
        showPassword: false,
        showRepeatPassword: false
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
      resetPassword: function(e) {
        e.preventDefault();
        return false;
      }
    }
  }
</script>
