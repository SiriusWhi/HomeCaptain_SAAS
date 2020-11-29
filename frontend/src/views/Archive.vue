<template>
  <div class="dashboard">
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
        <article class="col-md-2">
          <select class="hc-select" v-model="listingType" v-on:change="populateDashboard()">
            <option default value="buyer">Buyers</option>
            <option value="seller">Sellers</option>
            <option value="listing">Listings</option>
            <option value="loan_officer">Loan Officers</option>
            <option value="concierge">Concierges</option>
          </select>
        </article>
      </section>
      <ContactModal
        :contactModalShow="contactModalShow"
        :userInformation="selectedUser"
        :role="userRole"
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
      <RecViewModal :recViewModalShow="recViewModalShow" :userInformation="selectedUser"/>
      <ListingDetailModal :listingDetailShow="detailModalShow" :item="detailItem" />
      <ScheduleModal :scheduleModalShow="scheduleModalShow" :scheduleList="scheduleList" />

      <section class="cards-row row">
        <article
          class="card-wrapper col-md-4"
          v-for="(archive, i) in archives"
          :key="i"
          :class="(i>1 && i<5) ? 'order-' + (2+ (i-1)%3) : 'order-' + i"
        >
          <div class="card" v-if="listingType === 'buyer' || listingType === 'seller'">
            <div class="row">
              <article class="card-col col-md-6">
                <div class="card-av flex">
                  <p
                    :data-letters="archive.user.first_name[0]"
                    :class="'bg_'+i"
                    class="buyer-avatar ml-6"
                  ></p>
                  <p class="flex card-info">
                    <span class="card-name">{{archive.user.first_name}} {{archive.user.last_name}}</span>
                    <span
                      class="card-range"
                      v-if="archive.target_price_minimum && archive.target_price_minimum !== '0'"
                    >${{archive.target_price_minimum | Commas}} - ${{archive.target_price_maximum | Commas}}</span>
                  </p>
                </div>
                <p class="card-doc flex">
                  <span class="pulse-outside">
                    <span class="pulse"></span>
                  </span>
                  <span v-if="archive.milestones" class>{{archive.milestones}}</span>
                </p>
              </article>
              <article class="card-col col-md-6">
                <!-- <div class="faves flex">
                  <p class="faves-p faves-first">
                    <span class="faves-qty">17</span>
                    <span class="faves-label"># of Favorites</span>
                  </p>
                  <p class="faves-p">
                    <span class="faves-qty">2</span>
                    <span class="faves-label">Appointments Pending</span>
                  </p>
                </div> -->
              </article>
              <article class="col-md-12">
                <ul class="list-reset">
                  <li class="card-list-item">
                    <span class="list-bullet lb-l"></span>
                    <span class="list-label bs-list-label text-uppercase mont">location:</span>
                    <span class="list-value">{{archive.user.address? archive.user.address.city + ' ' + archive.user.address.state : ''}}</span>
                  </li>
                  <li class="card-list-item">
                    <span class="list-bullet lb-lo"></span>
                    <span class="list-label bs-list-label text-uppercase mont">Loan Officer:</span>
                    <span class="list-value pull-right"></span>
                    <span class="float-right">
                      <span
                        class="card-contacts-span mr-2"
                        v-if="archive.requirements && archive.requirements.length > 0"
                      >{{archive.requirements[0].loan_officer.user.first_name}} {{archive.requirements[0].loan_officer.user.last_name}}</span>
                      <span
                        class="card-contacts-a text-uppercase mont"
                        @click="openContactModal('officer',i)"
                      >Contact</span>
                    </span>
                  </li>
                  <li class="card-list-item last-card-item">
                    <span class="list-bullet lb-c"></span>
                    <span class="list-label bs-list-label text-uppercase mont">Concierge:</span>
                    <span class="float-right">
                      <span
                        class="card-contacts-span mr-2"
                        v-if="archive.requirements && archive.requirements.length > 0"
                      >{{archive.requirements[0].concierge.user.first_name}} {{archive.requirements[0].concierge.user.last_name}}</span>
                      <span
                        class="card-contacts-a text-uppercase mont"
                        @click="openContactModal('concierge',i)"
                      >Contact</span>
                    </span>
                  </li>
                </ul>
              </article>
            </div>
            <div class="row">
                <div class="col-md-6">
                  <button class="submit card-contact" @click="openContactModal('',i)">Contact</button>
                </div>
                <div class="col-md-6">
                  <div class="flex card-btn-wrap">
                  <button class="card-btn text-uppercase mont" @click="restore(archive.uid)">
                    Restore
                    <i class="far fa-trash-alt"></i>
                  </button>
                </div>
                </div>
              </div>
          </div>

          <CardLoanOfficer :officer="archive" :i="i" v-if="listingType === 'loan_officer'"
            :onRestore="restore"
          >
          </CardLoanOfficer>

          <CardConcierge :concierge="archive" :i="i" v-if="listingType === 'concierge'"
            :onRestore="restore"
          >
          </CardConcierge>

          <CardSearch :item="archive" :i="i" v-if="listingType === 'listing'"
            :onRestore="restore"
          >
          </CardSearch>
        </article>
      </section>
      <div class="row" >
        <div class="col-md-8">
          <b-pagination
            class="float-right"
            size="md"
            :total-rows="totalCount"
            v-model="currentPage"
            :per-page="4"
          ></b-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import HcHeader from "@/components/HcHeader.vue";

import Sidebar from "@/components/Sidebar.vue";
import { mapState, mapActions } from "vuex";

import ContactModal from "@/components/ContactModal.vue";
import ArchiveModal from "@/components/ArchiveModal.vue";
import FavoritesModal from "@/components/FavoritesModal.vue";
import ViewModal from "@/components/LoanOfficer/ViewModal.vue";
import RecommendModal from "@/components/LoanOfficer/RecommendModal.vue"; // Loan Officer Recommend Modal
import DiscourageModal from "@/components/LoanOfficer/DiscourageModal.vue";
import RecViewModal from "@/components/RecommendView.vue";  // Concierge Recommend Modal
import ListingDetailModal from "@/components/ListingInfoModal.vue";
import ScheduleModal from "@/components/ScheduleModal.vue";

import CardLoanOfficer from "@/components/CardLoanOfficer.vue";
import CardConcierge from "@/components/CardConcierge.vue";
import CardSearch from "@/components/CardSearch.vue";

import store from "../store";

import Commas from "@/filters/commas";

export default {
  name: "archive",
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
    CardConcierge,
    CardSearch,
    RecViewModal,
    ListingDetailModal,
    ScheduleModal,
  },
  data() {
    return {
      showLoading: false,
      archives: [],
      modalShow: false,
      totalCount: 0,
      contactModalShow: false,
      archiveModalShow: false,
      favoritesModalShow: false,
      viewModalShow: false,
      recommendModalShow: false,
      discourageModalShow: false,
      recViewModalShow: false,
      scheduleModalShow: false,
      detailModalShow: false,
      selectedUser: {},
      userRole: "",
      currentPage: 1,
      listingType: "buyer",
      searchString: "",
      uid: "",
      url: "",
      detailItem: {
        address: {},
      },
      scheduleList: [],
    };
  },
  methods: {
    populateDashboard() {
      this.showLoading = true;
      let pageLimit = 4;

      let url;

      switch (this.listingType) {
        case "buyer":
          url = "/api/realtor/dashboard/customer/?limit=0&milestones=Archived&buyer=1";
          break;
        case "seller":
          url = "/api/realtor/dashboard/customer/?limit=0&milestones=Archived&seller=1";
          break;
        case "listing":
          url = "/api/realtor/listings/archived/?limit=0";
          break;
        case "loan_officer":
          url = "/api/realtor/team/loan-officer/archived/?limit=0";
          break;
        case "concierge":
          url = "/api/realtor/team/concierge/archived/?limit=0";
          break;
      }
      if (this.searchString !== "") {
        url += `&search=${this.searchString}`;
      }
      url += `&offset=${pageLimit * (this.currentPage - 1)}`;

      axios
        .get(url)
        .then(res => {
          this.totalCount = res.data.count;
          let results = res.data.results;
          for (let i = 0; i < results.length; i++) {
            if (results[i].properties && results[i].properties.length !== 0) {
              results[i].requirements = results[i].properties;
            }
            if(this.listingType === 'buyer' || this.listingType === 'seller') {
              results[i].target_price_minimum = results[i].requirements[0].target_price_minimum;
              results[i].target_price_maximum = results[i].requirements[0].target_price_maximum;
            }
            if(this.listingType === 'listing') {
              results[i].user = results[i].realtor.user;
              results[i].target_price_minimum = results[i].target_price_minimum;
              results[i].target_price_maximum = results[i].target_price_maximum;
            }
          }
          console.log(results);

          this.archives = [];
          this.archives = results;
          this.showLoading = false;
        })
        .catch(error => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    openContactModal(role, i) {
      this.userRole = role;
      if (
        this.archives[i].properties &&
        this.archives[i].properties.length !== 0
      ) {
        this.archives[i].requirements = this.archives[i].properties;
      }
      this.selectedUser = this.archives[i];
      this.selectedUser.concierge = this.archives[i].requirements[0].concierge;
      this.selectedUser.loan_officer = this.archives[
        i
      ].requirements[0].loan_officer;
      this.contactModalShow = true;
    },

    restore(uid) {
      this.showLoading = true;
      let url;

      switch (this.listingType) {
        case "buyer":
          url = `/api/realtor/dashboard/customer/${uid}/restore/?milestones=Archived&buyer=1`;
          break;
        case "seller":
          url = `/api/realtor/dashboard/customer/${uid}/restore/?milestones=Archived&seller=1`;
          break;
        case "listing":
          url = `/api/realtor/listings/${uid}/restore/`;
          break;
        case "loan_officer":
          url = `/api/realtor/team/loan-officer/${uid}/restore/`;
          break;
        case "concierge":
          url = `/api/realtor/team/concierge/${uid}/restore/`;
          break;
      }

      axios
        .post(url)
        .then(res => {
          // this.archives = res.data;
          this.populateDashboard();
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

  },

  computed: {
    ...mapState(["idToken", "loading"])
  },

  filters: {
    Commas
  },

  watch: {
    loading: function(load) {
      if (load === true) {
        this.showLoading = true;
      } else {
        this.showLoading = false;
      }
    },
    currentPage: function(pageNum) {
      this.populateDashboard();
    },
  },

  mounted() {
    this.populateDashboard();
  }
};
</script>

<style scoped>
.card-wrapper {
  max-width: 33.33333% !important;
}
.card-wrapper:nth-child(5):after, .card-wrapper:nth-child(6):after{
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(240, 240, 240, 0.5);
}

.faves {
  visibility: hidden;
}

.pulse {
  background-color: #29d9c2;
}

.pulse-outside {
  background: rgba(41, 217, 194, 0.5);
}

.card-btn-wrap {
  justify-content: flex-end;
}

.bs-list-label {
  font-size: 13px;
  color: #3c4d69;
  letter-spacing: normal;
  margin-right: 20px;
}

.faves {
  margin-bottom: 0;
}

.card-range {
  font-size: 13px;
}

.buyer-avatar {
  margin-left: 0;
  margin-right: 16px;
}

.list-value {
  float: none;
}
</style>
