<template>
  <div id="app" :class="{'main': $store.getters['auth/isAuthenticated'], 'auth': !$store.getters['auth/isAuthenticated']}">
    <Sidebar v-if="$store.getters['auth/isAuthenticated']" />

    <div class="right-container">
      <Topbar v-if="$store.getters['auth/isAuthenticated']" />
      <router-view/>
    </div>
  </div>
</template>

<script>
  import Sidebar from "./components/Sidebar.vue";
  import Topbar from "./components/Topbar.vue";

  export default {
    name: "App",
    components: {
      Sidebar,
      Topbar
    }
  }
</script>

<style lang="scss">
  @import "./assets/styles/index.scss";

  #app {
    position: absolute;
    background: rgba(250, 250, 250, 0.8);
    border-radius: 10px;

    &.auth {
      top: 50%;
      left: 50%;
      width: 450px;
      transform: translate(-50%, -50%);
      max-height: calc(100% - 40px);
      overflow-y: auto;
    }

    .right-container {
      width: 100%;
      height: 100%;
      position: relative;
    }

    &.main {
      top: 30px;
      right: 30px;
      bottom: 30px;
      left: 30px;

      .right-container {
        background: rgba(250, 250, 250, 0.9);
        border-radius: 0 10px 10px 0;
        margin-left: 300px;
        width: calc(100% - 300px);
      }
    }
  }
</style>
