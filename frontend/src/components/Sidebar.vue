<template>
  <aside class="left-sidebar">
    <router-link :to="{name: 'dashboard'}">
      <img src="../../public/img/logo.png" class="logo" alt="Logo">
    </router-link>
    <ul class="sidebar-menu">
      <li class="menu-list">
        <img src="../../public/img/folder.svg" class="menu-icon" alt>
        <span class="menu-list-item toggle-menu">Activity</span>
        <i class="fas fa-info-circle menu-fa pointer"></i>
        <img src="../../public/img/sort-down.svg" class="menu-show pointer" alt>
        <ul class="submenu">
          <li><router-link :to="{name: 'dashboard'}">Dashboard</router-link></li>
          <li><router-link :to="{name: 'homeBuying'}">Home Buying</router-link></li>
          <li><router-link :to="{name: 'homeSelling'}">Home Selling</router-link></li>
          <li><router-link :to="{name: 'archive'}">Archive</router-link></li>
        </ul>
      </li>
      <li class="menu-list">
        <img src="../../public/img/house.svg" class="menu-icon" alt>
        <span class="menu-list-item toggle-menu">Listings</span>
        <img src="../../public/img/sort-down.svg" class="menu-show pointer" alt>
        <ul class="submenu">
          <li><router-link :to="{name: 'search'}">Search</router-link></li>
          <li><router-link :to="{name: 'favorites'}">Favorites</router-link></li>
          <li><router-link :to="{name: 'recommend'}">Recommend</router-link></li>
        </ul>
      </li>
      <li class="menu-list">
        <img src="../../public/img/person.svg" class="menu-icon" alt>
        <span class="menu-list-item toggle-menu">My Team</span>
        <img src="../../public/img/sort-down.svg" class="menu-show pointer" alt>
        <ul class="submenu">
          <li><router-link :to="{name: 'loanOfficers'}">Loan Officers</router-link></li>
          <li><router-link :to="{name: 'concierge'}">My Concierge</router-link></li>
          <li class="d-none">Archive</li>
        </ul>
      </li>
      <li class="menu-list">
        <i class="far fa-handshake menu-icon menu-icon-fa menu-inactive"></i>
        <span class="menu-list-item menu-inactive">Services</span>
      </li>
    </ul>
    <button class="submit agenda" @click="openAgendaModal({item: null, cid: ''})">Agenda</button>
    <AgendaModal :modalShow="showAgendaModal" :item="agendaItem" :uid="agendaUID" />
    <p class="text-center recommend">
      <span @click="openRecommendModal()"><i class="fas fa-thumbs-up"></i> Recommend Us</span>
    </p>
    <RecommendModal :modalShow="showRecommendModal" />
  </aside>
</template>

<script>
import axios from "../axios-auth";
import AgendaModal from "@/components/AgendaModal.vue";
import RecommendModal from "@/components/RecommendUsModal.vue";

import $ from "jquery";

export default {
  name: "sidebar",
  components: {
    AgendaModal,
    RecommendModal,
  },
  created() {
    this.$root.$on("show-agenda-modal", this.openAgendaModal);
  },
  methods: {
    openAgendaModal(data) {
      this.agendaItem = data.item;
      this.agendaUID = data.cid;
      this.showAgendaModal = true;
    },
    openRecommendModal() {
      this.showRecommendModal = true;
    },
  },
  data() {
    return {
      showAgendaModal: false,
      agendaItem: null,
      showRecommendModal: false,
      agendaUID: '',
    };
  },

  mounted() {
    /*$(".toggle-menu").click(function(){
      let a =  $(".toggle-menu").index(this);
      let smallMenus = $(".sidebar-menu").find(".submenu");
      let menuShow = $(".sidebar-menu").find(".menu-show");
      let i;

      for(i=0; i<smallMenus.length; i++){
        if(i !== a) {
          //smallMenus.eq(i).hide();
          //menuShow.eq(i).removeClass('flipArrow');
        }
      }

      $(this).find(".menu-show").toggleClass('flipArrow');
      $(this).find("ul").slideToggle(280);
    }) */


  }
};
</script>

<style scoped>

.flipArrow {
  transform: rotateZ(0deg);
  transition: all 0.2s;
}
</style>

