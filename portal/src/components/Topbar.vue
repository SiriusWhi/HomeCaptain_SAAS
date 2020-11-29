<template>
  <div class="topbar">
    <span class="info" v-b-tooltip.hover.bottom.html="'Can\'t find out how it works? Worries free. See the Help Center or Contact Us directly.'">
      <font-awesome-icon icon="question-circle" />
    </span>

    <div class="custom-input-div search">
      <font-awesome-icon icon="search" />
      <div class="custom-input-container" v-bind:class="{'input-has-value': search}">
        <label>Search for listings, realtors, or services</label>
        <input v-model="search" />
      </div>
    </div>

    <div class="actions">
      <span class="message">
        <font-awesome-icon icon="comment-alt" />
      </span>
      <span class="notification">
        <font-awesome-icon icon="bell" />
      </span>
      <div class="user-info">
        <span class="user-name">{{username}}</span>
        <img class="user-avatar" src="./../assets/images/user-avatar_1.jpg" v-b-tooltip.hover.bottom="'Edit your profile'" />
        <span class="log-out" v-b-tooltip.hover.bottom="'Log out'" @click="logout">
          <font-awesome-icon icon="power-off" />
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jQuery';

  export default {
    name: "Topbar",
    data: function() {
      return {
        search: '',
        username: ''
      }
    },
    mounted() {
      $(".topbar .custom-input-container input").focusin((e) => {
        $(e.target).parent().addClass("input-focused");
      });

      $(".topbar .custom-input-container input").focusout((e) => {
        $(e.target).parent().removeClass("input-focused");
      });

      let user = JSON.parse(localStorage.getItem('user'));
      this.username = user.username;
    },
    methods: {
      logout: function() {
        this.$store.dispatch('auth/logout').then(response => {
          if(response.status == 'success')
            this.$router.push('login');
        })
      }
    }
  }
</script>

<style lang="scss">
  @import "./../assets/styles/topbar.scss";
</style>
