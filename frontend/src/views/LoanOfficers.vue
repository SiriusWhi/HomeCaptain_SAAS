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
        <article class="col-md-2 status clickable" @click="getActiveList()">
          <span class="mont qty-number">{{stats.current_count}}</span>
          <span class="mont qty-desc">Active Loan Officers</span>
        </article>
        <article class="col-md-2 status clickable" @click="getPriorList()">
          <span class="mont qty-number">{{stats.prior_count}}</span>
          <span class="mont qty-desc">Prior Loan Officers</span>
        </article>
      </section>
      <ContactModal
        :contactModalShow="contactModalShow"
        :userInformation="selectedUser"
        :email="{}"
      />
      <ArchiveModal
        :archiveModalShow="archiveModalShow"
        :uid="uid"
        :url="url"
      />
      <FavoritesModal
        :favoritesModalShow="favoritesModalShow"
        :userInformation="selectedUser"
        :role="userRole"
      />
      <ViewModal
        :viewModalShow="viewModalShow"
        :userInformation="selectedUser"
      />
      <RecommendModal
        :recommendModalShow="recommendModalShow"
        :userInformation="selectedUser"
      />
      <DiscourageModal
        :discourageModalShow="discourageModalShow"
        :userInformation="selectedUser"
      />

      <!-- <section class="cards-row row">
        <article class="card-wrapper col-md-4" v-for="(officer, i) in loanOfficers" :key="i">
          <CardLoanOfficer :officer="officer" :i="i">
          </CardLoanOfficer>
        </article>
      </section> -->

      <section class="cards-row">
        <div style="display: flex;">
          <article class="card-wrapper" v-for="(officer, i) in loanOfficers1" :key="i">
            <CardLoanOfficer :officer="officer" :i="i">
            </CardLoanOfficer>
          </article>
        </div>
        <div style="display: flex;">
          <article class="card-wrapper" v-for="(officer, i) in loanOfficers2" :key="i">
            <CardLoanOfficer :officer="officer" :i="i+3">
            </CardLoanOfficer>
          </article>
        </div>
      </section>

      <div class="pagination justify-content-center">
        <b-pagination size="md" :total-rows="totalCount" v-model="currentPage" :per-page="6">
        </b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import HcHeader from "@/components/HcHeader.vue";

import ContactModal from "@/components/ContactModal.vue";
import ArchiveModal from "@/components/ArchiveModal.vue";
import FavoritesModal from "@/components/FavoritesModal.vue";
import ViewModal from "@/components/LoanOfficer/ViewModal.vue";
import RecommendModal from "@/components/LoanOfficer/RecommendModal.vue";
import DiscourageModal from "@/components/LoanOfficer/DiscourageModal.vue";
import CardLoanOfficer from "@/components/CardLoanOfficer.vue";

import Sidebar from "@/components/Sidebar.vue";
import { mapState, mapActions } from "vuex";

export default {
  name: "loanOfficers",
  components: {
    HcHeader,
    Sidebar,
    ContactModal,
    ArchiveModal,
    FavoritesModal,
    ViewModal,
    RecommendModal,
    DiscourageModal,
    CardLoanOfficer,
  },
  data() {
    return {
      showLoading: false,
      stats: {},
      loanOfficers: [],
      showDismissibleAlert: false,
      contactModalShow: false,
      selectedUser: {},
      userRole: "",
      archiveModalShow: false,
      uid: "",
      favoritesModalShow: false,
      viewModalShow: false,
      recommendModalShow: false,
      discourageModalShow: false,
      type: 0,
      url: "",
      searchString: "",
      currentPage: 1,
      totalCount: 0,
    };
  },
  methods: {
    getLoanOfficers() {
      this.showLoading = true;
      let apiUrl = "/api/realtor/team/loan-officer/?limit=6&offset=" + (this.currentPage - 1) * 6;
      if (this.type === 1) {
        apiUrl += "&prior=1";
        if (this.searchString !== "") {
          apiUrl += `&search=${this.searchString}`;
        }
      } else {
        if (this.searchString !== "") {
          apiUrl += `&search=${this.searchString}`;
        }
      }

      axios
        .get(apiUrl)
        .then(res => {
          this.totalCount = res.count;
          this.loanOfficers = res.data.results;
          this.showLoading = false;
        })
        .catch(error => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    searchUser: _.debounce(function () {
      this.getLoanOfficers();
    }, 1000),

    getActiveList() {
      this.type = 0;
      this.getLoanOfficers();
    },
    getPriorList() {
      this.type = 1;
      this.getLoanOfficers();
    },
    getStats() {
      this.showLoading = true;
      axios
        .get("/api/realtor/team/loan-officer/stats/")
        .then(res => {
          this.stats = res.data;
          this.showLoading = false;
        })
        .catch(error => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },
  },

  computed: {
    ...mapState(["idToken", "loading"]),
    loanOfficers1: function() {
      return this.loanOfficers.slice(0, 3);
  },
    loanOfficers2: function() {
      return this.loanOfficers.slice(3, 6);
    }
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
      this.getLoanOfficers();
    }
  },

  mounted() {
    this.getStats();
    this.getLoanOfficers();
  }
};
</script>
<style scoped>
.cards-row {
  display: flex;
  flex-direction: column;
  margin: 0;
  overflow-x: auto;
  /* flex-wrap: wrap; */
}
.cards-row .card-wrapper {
  width: 400px !important;
  min-width: 400px;
  /* height: 100%; */
  margin-right: 25px;
  /* padding: 0; */
}
</style>
