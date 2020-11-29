<template>
  <div class="dashboard">
    <b-alert
      variant="danger"
      dismissible
      :show="showDismissibleAlert"
      @dismissed="showDismissibleAlert=false"
    >Error loading content</b-alert>
    <div class="loading-wrapper" v-show="showLoading">
      <img src="../../public/img/loading.svg" alt>
    </div>
    <Sidebar/>
    <div class="page-content" data-simplebar data-simplebar-auto-hide="false">
      <HcHeader/>
      <input type="text"
             class="hiddenSearch"
             placeholder="Search buyers, sellers, or lenders"
             v-on:input="searchUser" v-model="searchString">
      <section class="row qty">
        <article class="col-md-2 status">
          <div
            class="status-wrap d-flex justify-content-center align-items-center pointer"
            @click="priorFilter = false, populateDashboard()"
          >
            <span class="mont qty-number">{{stats.current}}</span>
            <span class="mont qty-desc">Active
              <br>Concierges
            </span>
          </div>
        </article>
        <article class="col-md-2 status">
          <div
            class="status-wrap d-flex justify-content-center align-items-center pointer"
            @click="priorFilter = true, populateDashboard()"
          >
            <span class="mont qty-number">{{stats.prior_count}}</span>
            <span class="mont qty-desc">Prior
              <br>Concierges
            </span>
          </div>
        </article>
      </section>
      <ContactModal
        :contactModalShow="contactModalShow"
        :userInformation="selectedUser"
        :role="userRole"
        :email="{}"
      />
      <FavoritesModal
        :favoritesModalShow="favoritesModalShow"
        :userInformation="selectedUser"
        :role="userRole"
      />
      <RecViewModal :recViewModalShow="recViewModalShow" :userInformation="selectedUser"/>
      <section class="cards-row row">
        <article class="card-wrapper col-md-4" v-for="(concierge, i) in concierges" :key="i">
          <CardConcierge :concierge="concierge" :i="i">
          </CardConcierge>
        </article>
      </section>

      <div class="pagination justify-content-center">
        <b-pagination size="md" :total-rows="totalCount" v-model="currentPage" :per-page="9">
        </b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import HcHeader from "@/components/HcHeader.vue";
import Sidebar from "@/components/Sidebar.vue";

import { mapState, mapActions } from "vuex";
import store from "../store";

import ContactModal from "@/components/ContactModal.vue";
import FavoritesModal from "@/components/FavoritesModal.vue";
import RecViewModal from "@/components/RecommendView.vue";
import CardConcierge from "@/components/CardConcierge.vue";

export default {
  name: "concierge",
  components: {
    HcHeader,
    Sidebar,
    ContactModal,
    FavoritesModal,
    RecViewModal,
    CardConcierge
  },
  data() {
    return {
      showLoading: false,
      concierges: [],
      showDismissibleAlert: false,
      contactModalShow: false,
      favoritesModalShow: false,
      selectedUser: {},
      userRole: "",
      totalCount: 11,
      currentPage: 1,
      recViewModalShow: false,
      stats: {},
      priorFilter: false,
      searchString: "",
    };
  },
  methods: {
    populateDashboard() {
      this.showLoading = true;
      let url = "/api/realtor/team/concierge/?limit=9&offset=" + (this.currentPage - 1) * 9;
      if (this.priorFilter) {
        url += "&prior=1";
      }
      if (this.searchString !== "") {
        url += `&search=${this.searchString}`;
      }

      axios
        .get(url)
        .then(res => {
          this.totalCount = res.data.count;
          this.concierges = res.data.results;
          this.getStats();
          this.showLoading = false;
        })
        .catch(error => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    searchUser: _.debounce(function () {
      this.populateDashboard();
    }, 1000),

    getStats() {
      axios
        .get("/api/realtor/team/concierge/stats/")
        .then(res => {
          console.log(res);
          this.stats = res.data;
        })
        .catch(error => {
          console.log(error);
          this.showDismissibleAlert = true;
        });
    },
  },

  computed: {
    ...mapState(["idToken", "loading"])
  },

  watch: {
    loading: function(load) {
      if (load === true) {
        this.showLoading = true;
      } else {
        this.showLoading = false;
      }
    },
    currentPage: function() {
      this.populateDashboard();
    }
  },

  mounted() {
    this.populateDashboard();
  }
};
</script>
