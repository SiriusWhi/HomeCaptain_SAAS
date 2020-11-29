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
      <input type="text" class="hiddenSearch"
             placeholder="Search buyers, sellers, or lenders"
             v-on:input="searchCustomers" v-model="searchString">
      <div class="d-inline-block">
        <span class="category">Customers</span>
        <section class="flex qty mt-1">
          <article class="flex flex-align-center clickable" @click="selected = 0" :class="{active: selected == 0}">
            <span class="mont statusbar__number">{{stats.counts? stats.counts.needs_update : 0}}</span>
            <span class="mont statusbar__desc">Needs Update</span>
          </article>
          <article class="flex flex-align-center clickable" @click="selected = 1" :class="{active: selected == 1}">
            <span class="mont statusbar__number">{{stats.counts? stats.counts.buyers : 0}}</span>
            <span class="mont statusbar__desc">Buyers</span>
          </article>
          <article class="flex flex-align-center clickable" @click="selected = 2" :class="{active: selected == 2}">
            <span class="mont statusbar__number">{{stats.counts? stats.counts.sellers : 0}}</span>
            <span class="mont statusbar__desc">Sellers</span>
          </article>
          <article class="flex flex-align-center clickable" @click="selected = 3" :class="{active: selected == 3}">
            <span class="mont statusbar__number">{{stats.counts? stats.counts.all : 0}}</span>
            <span class="mont statusbar__desc">All</span>
          </article>
        </section>
      </div>
      <div class="d-inline-block">
        <span class="category mb-1">Status</span>
        <CustomSelect
          :options="stats.filters"
          v-model="chosenMilestone"
          label-key="milestones_display"
          value-key="milestones"
          count-key="milestones__count"
          :on-change="onStatusChange"
          no-status-label="Select a Status Filter">
        </CustomSelect>
      </div>
      <StatusModal :modalShow="modalShow" :userInformation="selectedUser"
        :milestones="selectedUser.buyer_seller === 'Buyer' ? stats.BUYER_MILESTONES_CHOICES : stats.SELLER_MILESTONES_CHOICES"/>
      <EditModal :editModalShow="editModalShow" :userInformation="selectedUser"/>
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
      <BuyerFavoritesModal
        :buyerFavoritesModalShow="buyerFavoritesModalShow"
        :favoritesList="favoritesList"
      />
      <FavoritesModal
        :favoritesModalShow="favoritesModalShow"
        :userInformation="selectedUser"
        :role="userRole"
      />
      <ScheduleModal
        :scheduleModalShow="scheduleModalShow"
        :scheduleList="scheduleList"
      />
      <ListingDetailModal
        :listingDetailShow="detailModalShow"
        :item="detailItem"
      />
      <!-- <RecViewModal :recViewModalShow="recViewModalShow" :userInformation="selectedUser"/> -->

      <section class="card-container">
        <div class="card card-wrapper" v-for="(buyer, i) in dashboardBuyers" :key="i">
          <div class="header">
            <span>
              <i class="fas fa-globe-americas"></i> English
            </span>
            <button class="card-btn text-uppercase mont pull-right" @click="showEditModal(buyer.uid)">
              <i class="fas fa-pen"></i> Edit
            </button>
          </div>
          <div class="profile">
            <div class="avatar">
              <p :data-avatar-medium-popup="buyer.user.first_name[0]" :class="'bg_'+i" class="buyer-avatar-medium"></p>
              <!-- <img src="../../public/img/avatar2.png" class="card-avatar" alt> -->
            </div>
            <div class="name">
              <span class="card-name">{{buyer.fullName}}</span>
            </div>
            <div class="address">
              <span class="list-value">{{buyer.location}}</span>
            </div>
            <p class="card-doc flex">
              <span class="pulse-outside">
                <span class="pulse"></span>
              </span>
              <span class="milestone">{{buyer.milestones}}</span>
              <i class="fas fa-pen doc-pen pointer" @click="showStatusModal(buyer.uid)"></i>
            </p>
          </div>
          <div class="contact">
            <ul class="list-reset">
              <li class="card-list-item">
                <span class="list-bullet lb-lo pull-left"></span>
                <div class="hidden m-lr-35">
                  <span class="list-label text-uppercase mont">Loan Officer:</span>
                  <div>
                    <span class="card-contacts-span">{{buyer.loan_officer.user.first_name}} {{buyer.loan_officer.user.last_name}}</span>
                    <span class="list-value pull-right"><a href="#" class="card-contacts-a text-uppercase mont" @click="showOtherContactModal(buyer, 'officer')">Contact</a></span>
                  </div>
                </div>
              </li>
              <li class="card-list-item last-card-item">
                <span class="list-bullet lb-c pull-left"></span>
                <div class="hidden m-lr-35">
                  <span class="list-label text-uppercase mont">concierge:</span>
                  <div>
                    <span class="card-contacts-span">{{buyer.concierge.user.first_name}} {{buyer.concierge.user.last_name}}</span>
                    <span class="list-value pull-right"><a href="#" class="card-contacts-a text-uppercase mont" @click="showOtherContactModal(buyer, 'concierge')">Contact</a></span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <hr>
          <div class="row">
            <div class="card-col col-md-4" @click="showScheduleModal(buyer)">
              <div class="number">{{buyer.scheduled.length}}</div>
              <div class="description">Showings Scheduled</div>
            </div>
            <div class="card-col col-md-4 price-wrapper">
              <div class="number price-number">{{buyer.range}}</div>
              <div class="description">Desired Price Range</div>
            </div>
            <div class="card-col col-md-4" @click="showBuyerModal(buyer)">
              <div class="number">{{buyer.favorites.length}}</div>
              <div class="description">Number of Favorites</div>
            </div>
          </div>
          <div class="btn-container">
            <button class="submit card-contact" @click="showContactModal(buyer.uid)">Contact</button>
            <button class="card-btn text-uppercase mont" @click="showArchiveModal(buyer.uid)">
              Archive
              <i class="far fa-trash-alt"></i>
            </button>
          </div>
          <div v-if="buyer.requested" class="footer">
            <span class="circle"></span>
            Requested Valuation
          </div>
        </div>
      </section>
      <div class="pagination justify-content-center">
        <b-pagination size="md" :total-rows="totalCount" v-model="currentPage" :per-page="3">
        </b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import HcHeader from "@/components/HcHeader.vue";

import StatusModal from "@/components/DashboardStatusModal.vue";
import ContactModal from "@/components/ContactModal.vue";
import EditModal from "@/components/DashboardEditModal.vue";
import ArchiveModal from "@/components/ArchiveModal.vue";
import FavoritesModal from "@/components/FavoritesModal.vue";
import BuyerFavoritesModal from "@/components/Dashboard/BuyerFavoritesModal.vue";
import ScheduleModal from "@/components/ScheduleModal.vue";
import ListingDetailModal from "@/components/ListingInfoModal.vue";
import CustomSelect from "@/components/CustomSelect.vue";

import Sidebar from "@/components/Sidebar.vue";
import { mapState, mapActions } from "vuex";

import $ from "jquery";
import _ from "lodash";

export default {
  name: "dashboard",
  components: {
    HcHeader,
    Sidebar,
    StatusModal,
    ContactModal,
    EditModal,
    ArchiveModal,
    BuyerFavoritesModal,
    FavoritesModal,
    ScheduleModal,
    ListingDetailModal,
    CustomSelect,
  },
  data() {
    return {
      showLoading: false,
      dashboardBuyers: [],
      showDismissibleAlert: false,
      searchString: "",
      userRole: "",
      modalShow: false,
      contactModalShow: false,
      editModalShow: false,
      selectedUser: {},
      milestone: "",
      baseUrl: "/api/realtor/dashboard/customer/",
      stats: {},
      archiveModalShow: false,
      uid: "",
      url: "",
      totalCount: 0,
      currentPage: 1,
      buyerFavoritesModalShow: false,
      favoritesModalShow: false,
      favoritesList: [],
      scheduleModalShow: false,
      recViewModalShow: false,
      scheduleList: [],
      selected: 0,
      chosenMilestone: "",
      detailModalShow: false,
      detailItem: {
        address: {},
      },
    };
  },
  methods: {
    populateDashboard() {
      let pageLimit = 3;
      let apiUrl = `${this.baseUrl}?limit=${pageLimit+1}&offset=${pageLimit * (this.currentPage - 1)}`;
      if (this.milestone !== "") {
        apiUrl += `&milestones=${this.milestone}`;
      }

      if (this.searchString !== "") {
        apiUrl = apiUrl + "&search=" + this.searchString;
      }

      switch (this.selected) {
        case 0:
          apiUrl += "&needs_update=1";
        break;
        case 1:
          apiUrl += "&buyer=1";
        break;
        case 2:
          apiUrl += "&seller=1";
        break;
        case 3:
        break;
      }

      this.showLoading = true;
      axios
        .get(apiUrl)
        .then(res => {
          console.log(res);
          let buyerArr = [];
          let i = 0;
          this.totalCount = res.data.count;
          let resData = res.data.results;
          this.reqs = resData;
          for (i = 0; i < resData.length; i++) {
            let obj = {};
            obj.userId = resData[i].user.uid;
            obj.uid = resData[i].uid;
            obj.email = resData[i].user.email;
            obj.fullName =
              resData[i].user.first_name + " " + resData[i].user.last_name;

            if(resData[i].requirements.length !== 0) {
              let requirement = resData[i].requirements[0];
              let addr = resData[i].user.address;
              obj.location = addr? `${addr.city} ${addr.state}`: '';

              obj.range = `$${this.$options.filters.numberWithCommas(requirement.target_price_minimum)} - $${this.$options.filters.numberWithCommas(requirement.target_price_maximum)}`;
              obj.loan_officer = requirement.loan_officer;
              obj.concierge = requirement.concierge;
              obj.requirements = resData[i].requirements;
              obj.favorites = resData[i].favorite_properties;
              obj.scheduled = resData[i].scheduled_showings.showings;
            } else if(resData[i].properties.length !== 0) {
              let property = resData[i].properties[0];
              let addr = resData[i].properties[0].address;
              obj.location = addr? `${addr.city} ${addr.state}`: '';

              obj.range = `$${this.$options.filters.numberWithCommas(property.target_price_minimum)} - $${this.$options.filters.numberWithCommas(property.target_price_maximum)}`;
              obj.loan_officer = property.loan_officer;
              obj.concierge = property.concierge;
              obj.requirements = resData[i].properties;
              obj.favorites = resData[i].properties[0].favoriting_buyers;
              obj.scheduled = resData[i].properties[0].scheduled_showings.showings;
            }
            if(!obj.favorites) obj.favorites = [];
            if(!obj.scheduled) obj.favorites = [];
            obj.languages_spoken = resData[i].languages_spoken ? resData[i].languages_spoken : [];

            obj.locations = [
              this.toLocation(obj.requirements[0].desired_city_1, obj.requirements[0].desired_state_1),
              this.toLocation(obj.requirements[0].desired_city_2, obj.requirements[0].desired_state_2),
              this.toLocation(obj.requirements[0].desired_city_3, obj.requirements[0].desired_state_3),
            ];
            obj.locations = obj.locations.filter(function (el) {
              return el != null;
            });

            obj.buyer_seller = resData[i].buyer_seller;
            obj.properties = resData[i].properties;
            obj.milestones = resData[i].milestones;
            obj.user = resData[i].user;
            obj.requested = resData[i].requested_valuation;
            obj.customer_update_history = resData[i].customer_update_history;

            buyerArr.push(obj);
          }
          this.dashboardBuyers = buyerArr;
          this.showLoading = false;
        })
        .catch(error => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },
    toLocation(city, state) {
      if(city) {
        if(state)
          return city + ", " + state;
        else return city;
      }
      return null;
    },

    getStats() {
      axios
        .get("/api/realtor/dashboard/customer/stats/")
        .then(res => {
          this.stats = res.data;
          let noFilterAry = [{
            milestones: "",
            milestones_display: ""
          }]
          this.stats.filters = noFilterAry.concat(this.stats.filters);
          console.log(this.stats);
        })
        .catch(error => {
          console.log(error);
        });
    },

    onStatusChange(value) {
      this.milestone = this.chosenMilestone.milestones;
      this.populateDashboard();
    },

    randomColor() {
      const r = () => Math.floor(256 * Math.random());
      return `rgb(${r()}, ${r()}, ${r()})`;
    },

    showStatusModal(uid) {
      this.modalShow = true;
      this.contactModalShow = false;
      this.editModalShow = false;
      this.selectedUser = this.dashboardBuyers.find(obj => {
        return obj.uid === uid;
      });
    },

    showEditModal(uid) {
      this.editModalShow = true;
      this.contactModalShow = false;
      this.modalShow = false;
      this.selectedUser = this.dashboardBuyers.find(obj => {
        return obj.uid === uid;
      });
    },

    showContactModal(uid) {
      this.contactModalShow = true;
      this.modalShow = false;
      this.editModalShow = false;
      this.selectedUser = this.dashboardBuyers.find(obj => {
        return obj.uid === uid;
      });
    },

    showOtherContactModal(buyer, type) {
      this.contactModalShow = true;
      this.modalShow = false;
      this.editModalShow = false;
      this.selectedUser = buyer;
      this.userRole = type;
    },

    showArchiveModal(uid) {
      this.archiveModalShow = true;
      this.url = this.baseUrl + `${uid}/archive/`;
      this.uid = uid;
    },

    showBuyerModal(buyer) {
      if(buyer.buyer_seller === "Buyer") {
        this.buyerFavoritesModalShow = true;
        this.favoritesList = buyer.favorites;
      } else {
        this.favoritesModalShow = true;
        this.selectedUser = buyer.properties[0];
      }
    },

    showScheduleModal(buyer) {
      if (buyer.scheduled.length) {
        this.scheduleModalShow = true;
        this.scheduleList = buyer.scheduled;
      }
    },

    openListingDetailModal(item) {
      this.detailItem = item;
      this.detailModalShow = true;
    },

    searchCustomers: _.debounce(function() {
      this.populateDashboard();
    }, 1000)
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
    currentPage: function(pageNum) {
      this.populateDashboard();
    },
    selected: function(num) {
      this.chosenMilestone = {  // For custom select UI
        milestones: "",
        milestones_display: ""
      }
      this.milestone = "";  // For request parameter to api
      this.populateDashboard();
    },
  },

  filters: {
    numberWithCommas(x) {
      x = parseFloat(x)
        .toFixed(2)
        .replace(/\.00$/, "");
      var parts = x.toString().split(".");
      parts[0] = parts[0].replace(",", "");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      return parts.join(".");
    }
  },

  mounted() {
    this.populateDashboard();
    this.getStats();
  },

  created() {
    this.$root.$on("show-listing-detail-modal", this.openListingDetailModal);
  },
};
</script>

<style scoped>
.qty {
  margin-bottom: 15px;
}
.statusbar__number {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: #808080;
  background-size: cover;
  font-size: 14px;
  color: #ffffff;
  text-align: center;
  line-height: 25px;
  margin-right: 11px;
}
.active .statusbar__number {
  background-color: #2c71c7;
}
.statusbar__desc {
  font-size: 18px;
  color: #808080;
  font-weight: 700;
  margin: auto 42px auto auto;
}
.active .statusbar__desc {
  color: #2c71c7;
}
.clickable {
  cursor: pointer;
}
.category {
  font-size: 18px;
  color: #5f6273;
  font-weight: 700;
}
.card-doc {
  line-height: 1;
  margin-bottom: 5px;
}

.alert {
  width: 237px;
}

.status {
  width: 250px;
}

.card-wrapper {
  width: 500px;
}

.card-col {
  width: 234px;
}

.card-container {
  display: flex;
  margin: 0;
  overflow-x: auto;
}
.card-container .card-wrapper {
  width: 350px !important;
  min-width: 350px;
  height: 100%;
  margin-right: 25px;
  padding: 0;
  border-radius: 20px;
  background-color: #fff;
  background-size: cover;
  box-shadow: 0px 40px 50px -15px rgba(60,77,105,0.1);
}
.card-container .card-wrapper:nth-child(4):after{
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(240, 240, 240, 0.5);
}
.card-container .card-wrapper .header {
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 11px;
  color: #808080;
  text-decoration: none solid rgb(128, 128, 128);
}
.card-container .card-wrapper .profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-container .card-wrapper .profile .name {
  margin: 0;
}

.card-container .card-wrapper .profile .address {
  min-height: 25px;
  margin-bottom: 0px;
}

.card-list-item {
  height: 55px;
  margin-bottom: 12px;
}
.list-bullet {
  height: 55px;
  border-top-right-radius: 50px;
  border-bottom-right-radius: 50px;
  background-size: cover;
}
.pull-left {
  float: left;
}
.pull-right {
  float: right;
}
.hidden {
  overflow: hidden;
}
.m-lr-35 {
  margin: 0 35px;
}
hr {
  margin: 0 92px 5px 92px !important;
}
.number {
  color: #3c4d69;
  font-weight: 700;
  text-decoration: none solid rgb(60, 77, 105);
  text-align: center;
  margin-bottom: 12px;
}
.price-number {
  width: 200px;
}
.price-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.description {
  color: #808080;
  text-decoration: none solid rgb(128, 128, 128);
  text-align: center;
}
.btn-container {
  margin: 30px 25px 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-btn {
  font-size: 13px;
}

.btn-container .submit {
  margin: 0;
}
.card-container .card-wrapper .footer {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 58px;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  background-color: #ccc9d1;
  background-size: cover;

  font-size: 14px;
  color: #ffffff;
  font-weight: 500;
  text-decoration: none solid rgb(255, 255, 255);
  letter-spacing: 1px;
  text-transform: uppercase;
}
.circle {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background-color: #f26a52;
  background-size: cover;
  margin-right: 9px;
}
.buyer-avatar-medium {
  margin-right: 0;
}
</style>
