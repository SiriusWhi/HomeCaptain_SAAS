<template>
  <div class="row">
    <div class="loading-wrapper" v-show="showLoading">
      <img src="../../public/img/loading.svg" alt="">
    </div>
    <div class="col-7">
      <div class="row">
        <div class="col-1">
          <i class="fas fa-question-circle qtn"></i>
        </div>
        <div class="col-11">
          <div class="search-wrapper">
            <input
              type="text"
              class="search-input hc-input">
            <img src="../../public/img/search.png" class="search-icon" alt="search icon">
          </div>
        </div>
      </div>
    </div>
    <div class="col-5">
      <div class="header-right float-right">
        <i class="fas fa-comment-alt header-icons pointer"></i>
        <i class="fas fa-bell header-icons pointer"></i>
        <span class="header-user">Marshall Douglas</span>
        <p data-avatar="A" class="header-avatar bg_10 user-avatar ml-0" style="display: inline-block"></p>
        <i class="fas fa-power-off header-icons pointer" @click="handleLogout(idToken)"></i>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import { mapState, mapActions } from "vuex";

export default {
  name: "HcHeader",
  components: {
  },
  data() {
    return {
      showLoading: false,
    };
  },
  methods: {
    ...mapActions(["logout"]),
    ...mapActions({
      handleLogout: "logout"
    }),
  },

  computed: {
    ...mapState(["idToken","loading"])
  },

  watch: {
    loading: function(load) {
      if (load === true) {
        this.showLoading = true;
      } else {
        this.showLoading = false;
      }
    }
  },
}
</script>
