<template>
  <div class="sidebar">
    <div class="row">
      <div class="col-12">
        <img class="sidebar-logo" src="./../assets/images/logo.png" />
      </div>

      <div class="col-12">
        <div class="menu-wrapper">
          <ul class="menu-item menu-submenu menu-open">
            <li class="menu-item">
              <a class="menu-toggle">
                <font-awesome-icon icon="folder" />
                <span>Activity</span>
                <font-awesome-icon icon="caret-down" />
              </a>

              <div class="sub-menu-wrapper">
                <ul class="menu-submenu">
                  <router-link :to="{name: 'dashboard'}" class="menu-item" v-bind:class="{'active': $route.name == 'dashboard'}">
                    <li>Dashboard</li>
                  </router-link>
                  <router-link :to="{name: 'home-buying'}" class="menu-item" v-bind:class="{'active': $route.name == 'home-buying'}">
                    <li>Home <u>B</u>uying</li>
                  </router-link>
                  <router-link :to="{name: 'home-selling'}" class="menu-item" v-bind:class="{'active': $route.name == 'home-selling'}">
                    <li>Home <u>S</u>elling</li>
                  </router-link>
                </ul>
              </div>
            </li>
          </ul>

          <ul class="menu-item menu-submenu menu-open">
            <li class="menu-item">
              <a class="menu-toggle">
                <font-awesome-icon icon="user" />
                <span>My Team</span>
                <font-awesome-icon icon="caret-down" />
              </a>

              <div class="sub-menu-wrapper">
                <ul class="menu-submenu">
                  <li class="menu-item">Realtors</li>
                  <li class="menu-item">My Concierge</li>
                </ul>
              </div>
            </li>
          </ul>

          <ul class="menu-item menu-submenu disabled">
            <li class="menu-item">
              <a class="menu-toggle">
                <font-awesome-icon icon="handshake" />
                <span>Services</span>
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="col-12 mt-5 text-center">
        <button class="btn btn-agenda">Agenda</button>
      </div>
    </div>
  </div>
</template>

<script>
  import $ from 'jQuery';

  export default {
    name: "Sidebar",
    mounted() {
      $('.menu-wrapper .menu-toggle').click((e) => {
        $(e.target).parent().parent().toggleClass('menu-open');
      });
    }
  }
</script>

<style lang="scss">
  @import "./../assets/styles/sidebar.scss";
</style>
