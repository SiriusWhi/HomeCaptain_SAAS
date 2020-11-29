<template>
  <b-modal
    v-model="favoritesModalShow"
    class="favorites-view"
    title="Contact"
    size="md"
    @hide="cancel()"
  >
    <div class="row">
      <div class="col-md-12">
        <div class="search-wrapper">
          <input
            type="text"
            class="search-input hc-input"
            placeholder="Search buyers, sellers, or lenders"
          >
          <img src="../../public/img/search.png" class="search-icon" alt="search icon">
        </div>
        <p class="text-center mb-5">
          <span class="fvm-btns fvmActive mr-4">Buyers</span>
          <span>Sellers</span>
        </p>
        <div v-if="userInformation.favoriting_buyers">
          <p
            class="bordered-input pointer bordered-text"
            v-for="(buyers,k) in userInformation.favoriting_buyers"
            :key="k">
            {{ buyers.first_name }} {{ buyers.last_name }}
            <span
              class="float-right contact-icon"
              @click="openContactModal('',k)"
            >
              <img width="16" src="../../public/img/icons/contact.svg"> Contact
            </span>
          </p>
        </div>
        <div v-if="userInformation.realtor_users">
          <p
            class="bordered-input pointer bordered-text"
            v-for="(buyers,k) in userInformation.realtor_users"
            :key="k"
          >
            {{
            buyers.customer__user__first_name }}
            <span
              class="float-right contact-icon"
              @click="openContactModal('',k)"
            >
              <img width="16" src="../../public/img/icons/contact.svg"> Contact
            </span>
          </p>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        <img src="../../public/img/icons/close-icon.svg" width="18"/> Hide</b-btn>
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
    cancel() {
      this.$parent.favoritesModalShow = false;
    },
    openContactModal(role, i) {
      //console.log(JSON.stringify(this.userInformation));
      this.userInformation.user = {};

      if (this.userInformation.parentPage === "favorites") {

        this.userInformation.user.first_name = this.userInformation.favoriting_buyers[i].first_name;
        this.userInformation.user.uid = this.userInformation.favoriting_buyers[i].uid;

      } else if (this.userInformation.parentPage === "concierge") {

        this.userInformation.user.first_name = this.userInformation.realtor_users[i].customer__user__first_name;
        this.userInformation.user.uid = this.userInformation.realtor_users[i].customer__user__uid;
      }

      this.userInformation.user.last_name = "";
      this.$parent.userRole = role;
      this.$parent.favoritesModalShow = false;
      this.$parent.contactModalShow = true;
    }
  },
  props: {
    favoritesModalShow: Boolean,
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
