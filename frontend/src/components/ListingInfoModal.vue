<template>
  <b-modal class="listing-item-detail" v-model="listingDetailShow" size="lg" hide-header @hide="cancel()">
    <div class="row">
      <div class="col-md-12 house-background">
        <img src="/img/home-info-background.jpeg" />
        <div class="house-detail">
          <div class="house-detail-container">
            <img src="/img/home-avatar.jpeg" />
            <p class="location">
              <span>{{item.address.street}}</span> <br/>
              <span>{{item.address.city}}</span>
            </p>
            <span class="rooms">
              {{item.bedrooms}} Bedrooms | {{item.bathrooms}} Baths | {{item.square_feet}} sqft
            </span>
            <span class="price">
              ${{item.target_price_maximum | Commas}}
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-7 owner-detail">
        <img src="/img/avatar4.png" />
        <div class="detail-container">
          <div class="detail-item">
            <label>Listing Broker</label>
            <p v-if="item.realtor">
              {{item.realtor.user.first_name}} {{item.realtor.user.last_name}}
              <span class="float-right contact-icon">
                <img width="16" src="/img/contact.b1b299dc.svg"> Contact
              </span>
            </p>
          </div>
          <div class="detail-item">
            <label>BATHROOMS</label>
            <p>{{item.bathrooms}}</p>
          </div>
          <div class="detail-item">
            <label>BEDROOMS</label>
            <p>{{item.bedrooms}}</p>
          </div>
          <div class="detail-item">
            <label>SQFT</label>
            <p>{{item.square_feet}} sqft</p>
          </div>
        </div>
      </div>
      <div class="col-md-5" style="margin: 10px 0;">
        <gmap-map
          :center="{ lat: 39.77768, lng: -104.826 }"
          :zoom="15"
          ref="gmap"
          v-bind:options="{mapTypeId: 'terrain'}"
          style="width:100%;  height: 300px;" />
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="showAgendaModal()">Request Showing</b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Hide <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
import { mapState, mapActions } from "vuex";
import store from "../store";

import Commas from "@/filters/commas";

export default {
  name: "ListingInfoModal",
  components: {},
  data() {
    return {};
  },
  filters: {
    Commas,
  },
  methods: {
    showAgendaModal() {
      this.$root.$emit("show-agenda-modal", { item: this.item, cid: "" });
    },
    cancel() {
      this.$parent.detailModalShow = false;
    },
  },
  props: {
    listingDetailShow: Boolean,
    item: Object,
  },
  mounted() {

  },
};
</script>
