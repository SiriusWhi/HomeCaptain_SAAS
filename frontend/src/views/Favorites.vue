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
    <div class="page-content" data-simplebar data-simplebar-auto-hide="true">
      <HcHeader/>
      <input type="text"
             class="hiddenSearch"
             placeholder="Search buyers, sellers, or lenders"
             v-on:input="searchUser" v-model="searchString">
      <section class="row qty">
        <article class="col-md-2 status">
          <input type="text" class="filter-input" v-model="clientFilter" v-on:input="filterByClient" placeholder="Filter by Client">
        </article>
        <article class="col-md-2 status filter-button" @click="showByFilter('top10')">
          <span class="mont qty-number">10</span>
                   <span class="mont qty-desc">Most<br/> Favorited</span>
        </article>
        <article class="col-md-2 status filter-button" @click="showByFilter('showing')">
                   <span class="mont qty-number light-blue">{{hasShowings}}</span>
                    <span class="mont qty-desc">Added to<br/> Showing</span>
        </article>
        <article class="col-md-2 status filter-button" @click="showByFilter('all')">
                   <span class="mont qty-number deep-blue">{{totalCount}}</span>
                   <span class="mont qty-desc">Total<br/> Favorites</span>
        </article>
      </section>
      <ViewModal :viewModalShow="viewModalShow" :userInformation="selectedUser"/>
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
      <ListingDetailModal :listingDetailShow="detailModalShow" :item="detailItem" />
      <section class="cards-row row">
        <article class="card-wrapper col-4" v-for="(favorite, i) in listingsFavorites" :key="i">
          <div class="card">
            <div class="row">
              <div class="search-bkg"></div>
              <span class="faves-imgs pointer">
                <i class="fas fa-camera"></i>
              </span>
              <div class="card-av card-av-search flex mont ml-2">
                  <span class="card-name text-left">
                    {{favorite.address.street}}, {{favorite.address.city}} {{favorite.address.state}} {{favorite.address.postalcode}}
                  </span>
              </div>
              <span class="card-range search-range pull-right">${{favorite.target_price_maximum | Commas}}</span>
              <div class="actions">
                <button class="small" @click="onFavorite(favorite)">
                  <i class="fas fa-star"></i>
                </button>
                <button class="large" @click="onShowInfo(favorite)">
                  <i class="fas fa-info-circle"></i>
                </button>
                <button class="small" @click="onRecommend(favorite)">
                  <i class="fas fa-share-alt"></i>
                </button>
              </div>
              <article class="card-container">
                <div class="row">
                  <div class="col-md-6">
                    <ul class="list-reset search-list">
                      <li class="card-list-item">
                        <span class="list-bullet lb-lo"></span>
                        <span class="list-label text-uppercase mont">SQFT:</span>
                        <span class="list-value pull-right">{{favorite.square_feet}} sq/ft</span>
                      </li>
                      <li class="card-list-item">
                        <span class="list-bullet lb-c"></span>
                        <span class="list-label text-uppercase mont">Bedrooms:</span>
                        <span class="list-value pull-right">{{favorite.bedrooms}}</span>
                      </li>
                      <li class="card-list-item">
                        <span class="list-bullet lb-g"></span>
                        <span class="list-label text-uppercase mont">Bathrooms:</span>
                        <span class="list-value pull-right">{{favorite.bathrooms}}</span>
                      </li>
                    </ul>
                  </div>
                  <div class="col-md-6">
                    <p class="faves-p" @click="showSchedules(favorite)">
                      <span class="faves-qty">{{favorite.scheduled_showings.count}}</span>
                      <span class="faves-label"># of Schedules</span>
                    </p>

                    <p class="faves-p" @click="showFavorites(favorite)">
                      <span class="faves-qty">{{favorite.favorite_count}}</span>
                      <span class="faves-label"># of Favorites</span>
                    </p>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <button class="submit card-contact" @click="showAgendaModal(favorite)">
                      <i class="fas fa-play"></i> &nbsp;
                      Add Showing
                    </button>
                  </div>
                  <div class="flex card-btn-wrap col-md-4 offset-2">
                    <button class="card-btn text-uppercase mont" @click="archiveFavorite(favorite)">
                      Archive
                      <i class="far fa-trash-alt"></i>
                    </button>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </article>
        <ScheduleModal :scheduleModalShow="scheduleModalShow" :scheduleList="scheduleList" />
      </section>
      <div class="row" v-if="count>10">
        <div class="col-md-8">
          <b-pagination
            class="float-right"
            size="md"
            :total-rows="count"
            v-model="currentPage"
            :per-page="10"
            @input="populateDashboard()"
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
import store from "../store";

import ViewModal from "@/components/FavoritesViewModal.vue";
import ContactModal from "@/components/ContactModal.vue";
import FavoritesModal from "@/components/FavoritesModal.vue";
import ScheduleModal from "@/components/ScheduleModal.vue";
import ListingDetailModal from "@/components/ListingInfoModal.vue";

import Commas from "@/filters/commas";

import _ from "lodash";

export default {
  name: "favorites",
  components: {
    HcHeader,
    Sidebar,
    ViewModal,
    ContactModal,
    FavoritesModal,
    ScheduleModal,
    ListingDetailModal,
  },
  data() {
    return {
      showLoading: false,
      listingsFavorites: [],
      showDismissibleAlert: false,
      modalShow: false,
      contactModalShow: false,
      viewModalShow: false,
      selectedUser: {},
      userRole: "",
      currentPage: 1,
      favoritesModalShow: false,
      clientFilter: "",
      count: 10,
      hasShowings: 0,
      totalCount: 0,
      scheduleModalShow: false,
      scheduleList: [],
      searchString: "",
      detailModalShow: false,
      detailItem: {
        address: {},
      },
    };
  },
  methods: {
    populateDashboard() {
      this.showLoading = true;
      let url = "/api/realtor/listings/?favorite=true";
      this.clientFilter === "" ? url = url : url += "&search_client=" + this.clientFilter

      let offSet;
      this.currentPage > 1 ? offSet = this.currentPage * 10 - 10 : offSet = 0;
      url += "&limit=10&offset=" + offSet;

      if (this.searchString !== "") {
        url += `&search=${this.searchString}`;
      }

      axios
        .get(url)
        .then(res => {
          console.log(res);
          this.listingsFavorites = res.data.results;
          this.count = res.data.count;
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

    showByFilter(type) {
      this.showLoading = true;
      let url = "/api/realtor/listings/?favorites=1";

      switch(type) {
        case "top10":
          url += "&top=1";
          break;
        case "showing":
          url += "&has_showings=1";
          break;
        case "all":
          break;
      }

      this.clientFilter ? url += "&search_client=" + this.clientFilter : null;

      axios.get(url)
        .then(res => {
          this.listingsFavorites = res.data.results;
          this.count = res.data.count;
          this.showLoading = false;
        })
        .catch(error => {
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    archiveFavorite(favorite) {
      this.showLoading = true;

      let url = `/api/realtor/listings/${favorite.uid}/archive/`;
      axios
        .post(url)
        .then(res => {
          this.populateDashboard();
          this.showLoading = false;
        })
        .catch(error => {
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    showViewModal(item) {
      this.viewModalShow = true;
      this.modalShow = false;
      this.selectedUser = item;
      this.selectedUser.parentPage = "favorites";
    },

    showFavorites(item) {
      this.favoritesModalShow = true;
      this.modalShow = false;
      this.viewModalShow = false;
      this.selectedUser = item;
      this.selectedUser.parentPage = "favorites";
    },

    showSchedules(item) {
      if (item.scheduled_showings.count) {
        this.scheduleModalShow = true;
        this.scheduleList = item.scheduled_showings.showings;
      }
    },

    showAgendaModal(favorite) {
      this.$root.$emit("show-agenda-modal", { item: favorite, cid: "" });
    },

    filterByClient: _.debounce(function() {
      this.populateDashboard();
    }, 1000),

    getFilterValues() {
      axios.get("/api/realtor/listings/favorite-filters/")
        .then(res => {
          this.totalCount = res.data.total_favorites;
          this.hasShowings = res.data.has_showings;
        })
        .catch(error => {
          this.showDismissibleAlert = true;
        })
    },

    onShowInfo(item) {
      this.detailModalShow = true;
      this.detailItem = item;
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
    },
    Commas,
  },

  mounted() {
    this.getFilterValues();
    this.populateDashboard();
  }
};
</script>

<style scoped>
  .search-bkg {
    height: 70px;
  }

  .search-range {
    top: 7px;
  }

  .faves-p:first-of-type {
    width: 100px;
  }

  .faves-p:last-of-type {
    width: 81px;
    margin-right: 10px;
  }

.card-doc {
  line-height: 1;
  padding: 10px;
}

.alert {
  width: 237px;
}

.card-btn {
  font-size: 13px;
}

.list-label {
  font-size: 13px;
  color: #3c4d69;
  letter-spacing: normal;
}

.list-value {
  font-size: 14px;
}

.search-list {
  margin-bottom: 30px;
}

.favorites-range {
  top: 0;
}

  .filter-button {
    cursor: pointer;
  }

  .card-wrapper {
    width: 484px !important;
    flex: none !important;
    max-width: none !important;
}
</style>
