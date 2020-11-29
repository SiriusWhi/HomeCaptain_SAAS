<template>
  <div class="container recovery">
    <div class="row">
      <div class="col-12">
        <img class="auth-logo" src="./../../assets/images/logo.png" />
      </div>
    </div>

    <div class="row">
      <form class="col-md-12 pl-4 pr-4" novalidate @submit="sendRequest">
        <div class="form-group">
          <div class="custom-input-div">
            <font-awesome-icon icon="envelope" />
            <div class="custom-input-container" v-bind:class="{'input-has-value': email}">
              <label>Email Address</label>
              <input v-model="email" />
            </div>
          </div>
        </div>

        <div class="form-group text-center mt-5">
          <button type="submit" class="btn btn-recover">Send Request</button>
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
    name: "Forgot",
    data: function() {
      return {
        email: ''
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
      sendRequest: function(e) {
        e.preventDefault();
        return false;
      }
    }
  }
</script>
