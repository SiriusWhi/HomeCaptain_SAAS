<template>
  <b-modal v-model="viewModalShow" hide-header  class="favorites-view" size="lg" @hide="cancel()" >
    <div class="row">
      <div class="col-md-2">
        <p
          v-if="userInformation.bathrooms"
          class="buyer-avatar user-avatar-popup card-avatar float-left bg_8 ml-0"
        ></p>
      </div>
      <div class="col-md-4">
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">{{userInformation.parentPage === "recommended" ? "Listing Broker" : "Property Owner"}}</p>
        <p class="bordered-input pointer bordered-text" v-if="userInformation.bathrooms">
          N/A
          <span class="float-right contact-icon" @click="openContactModal('officer')">
            <img width="16" src="../../public/img/icons/contact.svg"> Contact
          </span>
        </p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">ASSIGNED LOAN OFFICER</p>
        <p class="bordered-input pointer bordered-text" v-if="userInformation.bathrooms">
          {{ userInformation.loan_officer.user.first_name }}
          {{ userInformation.loan_officer.user.last_name }}
          <span
            class="float-right contact-icon"
            @click="openContactModal('officer')"
          >
            <img width="16" src="../../public/img/icons/contact.svg"> Contact
          </span>
        </p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">ASSIGNED CONCIERGE</p>
        <p class="bordered-input pointer bordered-text" v-if="userInformation.bathrooms">
          {{
          userInformation.concierge.user.first_name }}
          {{ userInformation.concierge.user.last_name }}
          <span
            class="float-right contact-icon"
            @click="openContactModal('concierge')"
          >
            <img width="16" src="../../public/img/icons/contact.svg"> Contact
          </span>
        </p>
      </div>
      <div class="col-md-1"></div>
      <div class="col-md-5">
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">BATHROOMS</p>
        <input
          type="text"
          readonly
          placeholder="Enter a number"
          v-if="userInformation.bathrooms"
          class="bordered-input"
          v-model="userInformation.bathrooms"
        >
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">BEDROOMS</p>
        <input
          type="text"
          readonly
          placeholder="Enter a number"
          v-if="userInformation.bathrooms"
          class="bordered-input"
          v-model="userInformation.bedrooms"
        >
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">SQFT</p>
        <input
          type="text"
          readonly
          placeholder="Enter a number"
          class="bordered-input"
          v-if="userInformation.bathrooms"
          v-model="userInformation.square_feet"
        >
      </div>
    </div>
    <div class="row">
      <div class="col-md-2"></div>
      <div class="col-md-10"></div>
    </div>
    <div class="row">
      <div class="col-md-2"></div>
      <div class="col-md-10">
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Price Range</p>
        <p class="d-flex fav-price-range">
          <span>${{userInformation.target_price_minimum | numberWithCommas}} - ${{userInformation.target_price_maximum | numberWithCommas}}</span>
        </p>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn v-if="userInformation.parentPage === 'favorites'" size="sm" class="float-left mr-2" variant="primary" @click="save()">Add Showing</b-btn>
      <b-btn v-if="userInformation.parentPage === 'recommended'" size="sm" class="float-left mr-2" variant="primary" @click="recommend()">Recommended</b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Cancel <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
import axios from "../axios-auth";
import { mapState, mapActions } from "vuex";
import store from "../store";

export default {
  name: "viewModal",
  components: {},
  data() {
    return {
      currentRoute: ""
    };
  },
  methods: {
    save() {
      axios
        .put(url, this.userInformation)
        .then(res => {
          this.$toastr("success", "Status update successfully", "Success!");
          this.$parent.viewModalShow = false;
        })
        .catch(error => {
          this.$toastr("error", error, "Error");
        });
    },
    cancel() {
      this.$parent.viewModalShow = false;
    },
    openContactModal(role) {
      this.$parent.userRole = role;
      this.$parent.viewModalShow = false;
      this.$parent.contactModalShow = true;
    },

    recommend(){
      this.$parent.viewModalShow = false;
      this.$parent.recViewModalShow = true;
    }
  },
  props: {
    viewModalShow: Boolean,
    userInformation: Object,
    userRole: String
  },
  computed: {
    ...mapState(["idToken", "loading"])
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
    //this.currentRoute = this.$route.name;
  }
};
</script>
