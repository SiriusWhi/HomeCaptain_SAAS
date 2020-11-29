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
          <div class="flex flex-wrap">
            <input
              class="hc-search buyers-filter ml-5 location-filter"
              v-model="location"
              placeholder="Type Location ..."
              @keydown.enter="getLists()"
            >
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
              <select class=" d-none hc-select buyers-filter ml-5" v-model="priceNum" v-on:change="getLists">
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
              <select class="d-none hc-select buyers-filter ml-5" v-model="bdrNum" v-on:change="getLists">
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
                  v-on:change="getLists"
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
                class="hc-select buyers-filter ml-5 styled-select sqft-styled-select pointer"
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
              <select class="d-none hc-select buyers-filter ml-5" v-model="sqft" v-on:change="getLists">
              <option value>
                SQFT:
                <span class="fa fa-plug"></span>
              </option>
              <option v-for="(sqft,f) in availableSqft" :key="f">{{sqft[0]}} - {{sqft[1]}}</option>
            </select>
            </div>
          </div>
          <div class="col-md-12 text-center pt-5">
            <p
              class="card-doc mt-3 recommended-tab pointer mr-3"
              v-bind:class="{'recommended-tab-active': isListView}"
              @click="isListView=true; isMapView=false"
            >
              <i class="fas fa-bars"></i>
              <span class="milestones-text">List View</span>
            </p>
            <p
              class="card-doc mt-3 recommended-tab pointer"
              v-bind:class="{'recommended-tab-active': isMapView}"
              @click="isListView=false; isMapView=true"
            >
              <i class="fas fa-map-marker-alt"></i>
              <span class="milestones-text">Map View</span>
            </p>
          </div>
        </div>
      </div>
      <div v-if="isListView">
        <section class="cards-row row">
          <article class="card-wrapper col-md-4" v-for="(item, i) in listingsSearch" :key="i">
            <CardSearch :item="item" :i="i">
            </CardSearch>
          </article>
        </section>
        <ListingDetailModal :listingDetailShow="detailModalShow" :item="detailItem" />
        <ScheduleModal :scheduleModalShow="scheduleModalShow" :scheduleList="scheduleList" />
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
import Sidebar from "@/components/Sidebar.vue";
import GoogleMap from "@/components/GoogleMap.vue";
import { mapState, mapActions } from "vuex";

import ListingDetailModal from "@/components/ListingInfoModal.vue";
import ScheduleModal from "@/components/ScheduleModal.vue";
import CardSearch from "@/components/CardSearch.vue";

import DateFilter from "@/filters/date";
import Commas from "@/filters/commas";

import store from "../store";

export default {
  name: "search",
  components: {
    HcHeader,
    Sidebar,
    GoogleMap,
    ListingDetailModal,
    ScheduleModal,
    CardSearch,
  },
  data() {
    return {
      showLoading: false,
      listingsSearch: [],
      availableLocations: [],
      availablePrices: [],
      availableBedrooms: [],
      availableBathrooms: [],
      availableSqft: [],
      showDismissibleAlert: false,
      location: "",
      price: "",
      bedroom: "",
      bathroom: "",
      sqft: "",
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
      scheduleModalShow: false,
      scheduleList: [],
      detailModalShow: false,
      detailItem: {
        address: {},
      },
      searchString: "",
    };
  },
  methods: {
    getLists() {
      this.showLoading = true;
      let url = "/api/realtor/listings/?limit=0";
      if (this.location !== "") {
        url += `&location=${this.location}`;
      }
      if (this.price !== "") {
        const priceGroup = this.price.split(" - ");
        url += `&min_price=${priceGroup[0]}&max_price=${priceGroup[1]}`;
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
      if (this.searchString !== "") {
        url += `&search=${this.searchString}`;
      }

      axios
        .get(url)
        .then((res) => {
          const listingsArr = [];
          const i = 0;
          const resData = res.data.results;
          this.listingsSearch = resData;
          console.log(res.data);
          this.showLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.showLoading = false;
          this.showDismissibleAlert = true;
        });
    },
    searchUser: _.debounce(function () {
      this.getLists();
    }, 1000),
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
          for (let i = res.data.min_bathrooms; i <= res.data.max_bathrooms; i++) {
            this.availableBathrooms.push(i);
          }
          this.availableSqft = res.data.area_range;
        })
        .catch((error) => {
          console.log(error);
          this.showDismissibleAlert = true;
        });
    },
    filterList() {
      this.getAvailebleFilters();
      this.getLists();
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
      this.getLists();
    },

    bdrNum: function(val) {
      this.bedroom = val;
      this.getLists();
    },

    priceNum: function(val) {
      this.price = val[0] + " - " + val[1];
      this.getLists();
    },

    sqftNum: function(val) {
      this.sqft = val[0] + " - " + val[1];
      this.getLists();
    }
  },

  mounted() {
    this.filterList();
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

  /* .list-label {
    font-size: 13px;
    color: #3c4d69;
    letter-spacing: normal;
  }

  .list-value {
    font-size: 14px;
  } */

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
</style>
