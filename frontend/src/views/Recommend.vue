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
      <div class="row">
        <div class="col-md-12">
          <div class="flex mb-5 flex-wrap">
            <input class="hc-search buyers-filter ml-5" v-model="location" placeholder="Type Location ..." @keydown.enter="populateDashboard()"/>
            <div class="position-relative styled-select-wrap sqft-wrap">
              <div
                class="hc-select buyers-filter ml-4 styled-select sqft-styled-select pointer"
                @click="showFilterOptions.showPrices = !showFilterOptions.showPrices"
                :class="{dropSelect: showFilterOptions.showPrices}"
              >
                <span>
                  <i class="styled-select-plus fas fa-plus"></i>
                  <span class="styled-select-label">
                    <em>Price:</em>
                    <b v-show="priceNum !== ''"> {{priceNum[0] | Commas}} - {{priceNum[1] | Commas}}</b>
                  </span>
                </span>
                <p class="styled-select-options sqft-options">
                  <span @click="priceNum = ''">Any</span>
                  <span
                    v-for="(price,b) in availablePrices"
                    :key="b"
                    @click="priceNum = price"

                  >{{price[0] | Commas}} - {{price[1] | Commas}}</span>
                </p>
              </div>
                <select class=" d-none hc-select buyers-filter ml-5" v-model="priceNum" v-on:change="populateDashboard()">
              <option value>
                Price
                <span class="fa fa-plug"></span>
              </option>
              <option
                v-for="(price,b) in availablePrices"
                :key="b"
              >{{price[0] | Commas}} - {{price[1] | Commas}}</option>
            </select>
            </div>
            <div class="position-relative styled-select-wrap">
              <div
                class="hc-select buyers-filter ml-5 styled-select pointer"
                @click="showFilterOptions.showBedrooms = !showFilterOptions.showBedrooms"
                :class="{dropSelect: showFilterOptions.showBedrooms}"
              >
                <span>
                  <i class="styled-select-plus fas fa-plus"></i>
                  <span class="styled-select-label">
                    <em>Bedrooms:</em>
                    {{bdrNum}}
                  </span>
                </span>
                <p class="styled-select-options" style="overflow-y: scroll;">
                  <span @click="bdrNum = ''">Any</span>
                  <span
                     v-for="(bedroom,c) in availableBedrooms" :key="c"
                    @click="bdrNum = bedroom"
                  >{{bedroom}}</span>
                </p>
              </div>
              <select class="d-none hc-select buyers-filter ml-5" v-model="bdrNum" v-on:change="populateDashboard()">
              <option value>
                Bedrooms
                <span class="fa fa-plug"></span>
              </option>
              <option v-for="(bedroom,c) in availableBedrooms" :key="c">{{bedroom}}</option>
            </select>
            </div>
            <div class="position-relative styled-select-wrap">
              <div
                class="hc-select buyers-filter ml-5 styled-select pointer"
                @click="showFilterOptions.showBathrooms = !showFilterOptions.showBathrooms"
                :class="{dropSelect: showFilterOptions.showBathrooms}"
              >
                <span>
                  <i class="styled-select-plus fas fa-plus"></i>
                  <span class="styled-select-label">
                    <em>Bathrooms:</em>
                    {{bthNum}}
                  </span>
                </span>
                <p class="styled-select-options">
                  <span @click="bthNum = ''">Any</span>
                  <span
                    v-for="(bathroom,k) in availableBathrooms"
                    @click="bthNum = bathroom"
                    :key="k"
                  >{{bathroom}}</span>
                </p>
                <select
                  class="d-none hc-select buyers-filter ml-5"
                  v-model="bthNum"
                  v-on:change="populateDashboard()"
                >
                  <option value>
                    Bathrooms
                    <span class="fa fa-plug"></span>
                  </option>
                  <option v-for="(bathroom,d) in availableBathrooms" :key="d">{{bathroom}}</option>
                </select>
              </div>
            </div>
            <div class="position-relative styled-select-wrap sqft-wrap">
              <div
                class="hc-select buyers-filter ml-4 styled-select sqft-styled-select pointer"
                @click="showFilterOptions.showSqft = !showFilterOptions.showSqft"
                :class="{dropSelect: showFilterOptions.showSqft}"
              >
                <span>
                  <i class="styled-select-plus fas fa-plus"></i>
                  <span class="styled-select-label">
                    <em>Square Feet:</em>
                    {{sqft}}
                  </span>
                </span>
                <p class="styled-select-options sqft-options">
                  <span @click="sqftNum = ''">Any</span>
                  <span
                    v-for="(sqft,f) in availableSqft" :key="f"
                    @click="sqftNum = sqft"
                  >{{sqft[0]}} - {{sqft[1]}}</span>
                </p>
              </div>
              <select class="d-none hc-select buyers-filter ml-4" v-model="sqft" v-on:change="populateDashboard()">
              <option value>
                SQFT:
                <span class="fa fa-plug"></span>
              </option>
              <option v-for="(sqft,f) in availableSqft" :key="f">{{sqft[0]}} - {{sqft[1]}}</option>
            </select>
            </div>
            <input class="hc-search buyers-filter ml-5" v-model="keyword"
                   placeholder="Type Keyword ..." @keydown.enter="populateDashboard()"/>
          </div>
        </div>
        <div class="col-md-12 text-center">
          <p class="card-doc mt-3 recommended-tab pointer mr-3" v-bind:class="{'recommended-tab-active': isListView}" @click="isListView=true; isMapView=false">
            <i class="fas fa-bars"></i><span class="milestones-text">List View</span></p>
          <p class="card-doc mt-3 recommended-tab pointer" v-bind:class="{'recommended-tab-active': isMapView}" @click="isListView=false; isMapView=true">
            <i class="fas fa-map-marker-alt"></i><span class="milestones-text">Map View</span></p>
        </div>
      </div>
      <ViewModal :viewModalShow="viewModalShow" :userInformation="selectedUser"/>
      <RecViewModal :recViewModalShow="recViewModalShow" :userInformation="selectedUser"/>
      <ContactModal
        :contactModalShow="contactModalShow"
        :userInformation="selectedUser"
        :role="userRole"
        :email="{}"/>
      <ListingDetailModal :listingDetailShow="detailModalShow" :item="detailItem" />
      <div v-if="isListView">
        <section class="cards-row row">
          <article class="card-wrapper col-md-4" v-for="(listing,i) in listingsRecommended" :key="i">
            <div class="card">
              <div class="row">
                <div class="search-bkg"></div>
                <div class="card-av card-av-search flex mont ml-2">
                  <span class="card-name text-left">
                  {{listing.address.street}}
                  <br>
                  {{listing.address.city}} {{listing.address.state}} {{listing.address.postalcode}}
                  </span>
                </div>
                <span class="rec-date mont text-center">30 Dec 2018</span>
                <span class="card-range search-range pull-right">${{listing.target_price_maximum | Commas}}</span>
                <div class="actions">
                  <button class="small" @click="onFavorite(listing)">
                    <i class="fas fa-star"></i>
                  </button>
                  <button class="large" @click="onShowInfo(listing)">
                    <i class="fas fa-info-circle"></i>
                  </button>
                  <button class="small" @click="onRecommend(listing)">
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
                          <span class="list-value pull-right">{{listing.square_feet}} sq/ft</span>
                        </li>
                        <li class="card-list-item">
                          <span class="list-bullet lb-g"></span>
                          <span class="list-label text-uppercase mont">Bathrooms:</span>
                          <span class="list-value pull-right">{{listing.bathrooms}}</span>
                        </li>
                      </ul>
                    </div>
                    <div class="col-md-6">
                      <ul class="list-reset search-list">
                        <li class="card-list-item">
                          <span class="list-bullet lb-c"></span>
                          <span class="list-label text-uppercase mont">Bedrooms:</span>
                          <span class="list-value pull-right">{{listing.bedrooms}}</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-6">
                      <button class="submit card-contact" @click="showRecommendModal(listing)">
                        Recommend
                      </button>
                    </div>
                    <div class="flex card-btn-wrap col-md-6">
                      <button class="card-btn text-uppercase mont" @click="archiveFavorite(listing)">
                        Archive
                        <i class="far fa-trash-alt"></i>
                      </button>
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </article>
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
      <div v-else>
        <GoogleMap/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import HcHeader from "@/components/HcHeader.vue";
import store from "../store";

import Sidebar from "@/components/Sidebar.vue";
import { mapState, mapActions } from "vuex";

import DateFilter from "@/filters/date";
import Commas from "@/filters/commas";

import RecViewModal from "@/components/RecommendView.vue";
import ContactModal from "@/components/ContactModal.vue";

import ListingDetailModal from "@/components/ListingInfoModal.vue";
import ViewModal from "@/components/FavoritesViewModal.vue";
import GoogleMap from "@/components/GoogleMap.vue";

export default {
  name: "recommend",
  components: {
    HcHeader,
    Sidebar,
    ViewModal,
    ContactModal,
    RecViewModal,
    GoogleMap,
    ListingDetailModal,
  },
  data() {
    return {
      showLoading: false,
      listingsRecommended: [],
      showDismissibleAlert: false,
      modalShow: false,
      contactModalShow: false,
      viewModalShow: false,
      recViewModalShow: false,
      selectedUser: {},
      userRole: "",
      count: 11,
      currentPage: 1,
      favoritesModalShow: false,
      location: "",
      price: "",
      bedroom: "",
      bathroom: "",
      sqft: "",
      keyword: "",
      availableLocations: [],
      availablePrices: [],
      availableBedrooms: [],
      availableBathrooms: [],
      availableSqft: [],
      isListView: true,
      isMapView: false,
      showFilterOptions: {
        showBedrooms: false,
        showBathrooms: false,
        showPrices: false,
        showSqft: false,
      },
      bthNum: "",
      bdrNum: "",
      sqftNum: "",
      priceNum: "",
      detailModalShow: false,
      detailItem: {
        address: {},
      },
      searchString: "",
    };
  },
  methods: {
    populateDashboard() {
      this.showLoading = true;
      this.getAvailebleFilters();
      let offSet;
      this.currentPage > 1
        ? (offSet = this.currentPage * 10 - 10)
        : (offSet = 0);
      let url = `/api/realtor/listings/?recommended=true&limit=10&offset=${offSet}`;

      if (this.location !== "") {
        url += `&location=${this.location}`;
      }
      if (this.price !== "") {
        const priceGroup = this.price.split(" - ");
        url += `&min_price=${priceGroup[0].replace(
          ",",
          "",
        )}&max_price=${priceGroup[1].replace(",", "")}`;
      }
      if (this.bedroom !== "") {
        url += `&bedrooms=${this.bedroom}`;
      }
      if (this.bathroom !== "") {
        url += `&bathrooms=${this.bathroom}`;
      }
      if (this.sqft !== "") {
        const sqftGroup = this.sqft.split(" - ");
        url += `&min_sqft=${sqftGroup[0]}&max_sqft=${sqftGroup[1]}`;
      }

      if (this.keyword !== "") {
        url += `&keyword=${this.keyword}`;
      }

      if (this.searchString !== "") {
        url += `&search=${this.searchString}`;
      }

      axios
        .get(url)
        .then((res) => {
          console.log(res);
          this.listingsRecommended = res.data.results;
          this.count = res.data.count;
          this.showLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },

    searchUser: _.debounce(function () {
      this.populateDashboard();
    }, 1000),

    archiveFavorite(listing) {
      this.showLoading = true;
      const url = `/api/realtor/listings/${listing.uid}/archive/`;
      axios
        .post(url)
        .then((res) => {
          this.listingsRecommended = res.data.results;
          this.populateDashboard();
          this.showLoading = false;
          this.$toastr("success", "Listing Archived", "Success!");
        })
        .catch((error) => {
          this.showLoading = false;
          this.showDismissibleAlert = true;
          this.$toastr("error", error, "Error");
        });
    },

    getAvailebleFilters() {
      const url = "/api/realtor/listings/filters/";

      axios
        .get(url)
        .then((res) => {
          this.availableLocations = res.data.cities;
          this.availablePrices = res.data.price_range;
          this.availableBedrooms = [];
          for (let i = res.data.min_bedrooms; i <= res.data.max_bedrooms; i++) {
            this.availableBedrooms.push(i);
          }
          this.availableBathrooms = [];
          for (
            let i = res.data.min_bathrooms;
            i <= res.data.max_bathrooms;
            i++
          ) {
            this.availableBathrooms.push(i);
          }
          this.availableSqft = res.data.area_range;
        })
        .catch((error) => {
          console.log(error);
          this.showDismissibleAlert = true;
        });
    },

    showRecommendModal(item) {
      this.recViewModalShow = true;
      this.modalShow = false;
      this.selectedUser = item;
      this.selectedUser.parentPage = "recommended";
    },

    showViewModal(item) {
      this.viewModalShow = true;
      this.modalShow = false;
      this.selectedUser = item;
      this.selectedUser.parentPage = "recommended";
    },

    onFavorite(item) {

    },
    onRecommend(item) {

    },
    onShowInfo(item) {
      this.detailModalShow = true;
      this.detailItem = item;
    },
  },

  computed: {
    ...mapState(["idToken", "loading"]),
  },

  filters: {
    DateFilter,
    Commas,
  },

  watch: {
    loading(load) {
      if (load === true) {
        this.showLoading = true;
      } else {
        this.showLoading = false;
      }
    },

    bthNum: function(val) {
      this.bathroom = val;
      this.populateDashboard();
    },

    bdrNum: function(val) {
      this.bedroom = val;
      this.populateDashboard();
    },

    priceNum: function(val) {
      this.price = val[0] + " - " + val[1];
      this.populateDashboard();
    },

    sqftNum: function(val) {
      this.sqft = val[0] + " - " + val[1];
      this.populateDashboard();
    }
  },

  mounted() {
    this.populateDashboard();
  },
};
</script>

<style scoped>
.card-doc {
  line-height: 1;
  padding: 10px;
}

.alert {
  width: 237px;
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

.card-btn-wrap {
  justify-content: flex-end;
}

.search-list {
  margin-bottom: 30px;
  padding-top: 17px;
}

.recommend-list {
  padding-top: 93px;
}

.search-range {
  top: 36px;
}

.styled-select-label b {
  font-weight: normal;
}

.dropSelect {
  background: #c4d7ed;
  height: auto;
  border-radius: 12px;
  padding: 8px 0 0 8px;
  overflow: auto;
}

.sqft-wrap {
  width: 239px;
}

.sqft-options {
  width: 226px;
}

.sqft-styled-select {
  width: 243px;
}

  .actions button {
    cursor: pointer;
  }

  .card-doc {
    line-height: 1;
    padding: 10px;
  }

  .alert {
    width: 237px;
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

  .card-btn-wrap {
    justify-content: flex-end;
  }

  .card-btn {
    font-size: 13px;
  }

  .search-list {
    margin-bottom: 30px;

  }

  .recommend-list {
    padding-top: 93px;
  }

  .rec-date {
    left: initial;
    top: 0;
    right: 15px;
  }
</style>
