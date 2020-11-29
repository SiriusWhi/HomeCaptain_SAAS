<template>
  <b-modal v-model="recViewModalShow" hide-header class="favorites-view" size="lg" @hide="cancel()">
    <div class="flex align-items-center mb-4">
      <img
        src="../../public/img/house-bkg.png"
        v-if="userInformation.id && userInformation.parentPage === 'recommended'"
        class="rec-avatar"
        alt
      >
      <p
        v-if="userInformation.user && userInformation.parentPage === 'concierge'"
        :data-avatar-popup="userInformation.user.first_name[0]"
        class="rec-avatar text-center bg_8 ml-0"
      ></p>
      <div class="flex rec-title-wrapper">
        <h3
          class="rec-title"
          v-if="userInformation.id && userInformation.parentPage === 'recommended'"
        >Recommend Listing #{{userInformation.id}}</h3>
        <h3
          class="rec-title"
          v-if="userInformation.user && userInformation.parentPage === 'concierge'"
        >{{ userInformation.user.first_name }} {{ userInformation.user.last_name }}</h3>
        <div v-if="userInformation.user && userInformation.parentPage === 'concierge' && userInformation.thumbsDown === false">
          <article class="team-stars">
            <i class="fas fa-star"></i>
            <i class="fas fa-star"></i>
            <i class="fas fa-star"></i>
            <i class="fas fa-star"></i>
            <i class="fas fa-star-half-alt"></i>
          </article>
          <span class="based-on">
            Based on
            <strong>200</strong> reviews
          </span>
        </div>
        <div v-if="userInformation.user && userInformation.parentPage === 'concierge' && userInformation.thumbsDown === true">
          <article class="team-stars">
            <i class="far fa-star"></i>
            <i class="far fa-star"></i>
            <i class="far fa-star"></i>
            <i class="far fa-star"></i>
            <i class="far fa-star"></i>
          </article>
          <span class="based-on">
            Based on
            <strong>1</strong> reviews
          </span>
        </div>
        <p
          class="rec-title-info"
          v-if="userInformation.address"
        >{{userInformation.address.city}} | {{userInformation.bathrooms}} Bathrooms | {{userInformation.bedrooms}} Bedrooms</p>
      </div>
      <span
        class="rec-range"
        v-if="userInformation.target_price_maximum"
      >{{userInformation.target_price_maximum | numberWithCommas}}</span>
    </div>
    <div class="pad-rec">
      <span v-if="userInformation.thumbsDown === false">
        <p class="recommend-to mont text-uppercase">recommend to:</p>
      <ul class="list-reset recommend-to-list">
        <li class="mb-3">
          <input
            type="text"
            v-model="addedUser"
            class="add-user-input mr-3"
            placeholder="Enter username"
          >
          <span class="hc-blue pointer" @click="addUsers(addedUser)">Add</span>
        </li>
        <li class="rec-list" v-for="(user,k) in myUsers" :key="k">
          <span class="list-bullet lb-c"></span>
          <span>@{{user}}</span>
          <i class="rec-trash fas fa-trash-alt float-right pointer" @click="myUsers.splice(k,1)"></i>
        </li>
      </ul>
      <p class="mb-5">
        Add a new customer or click
        <button
          class="pointer hc-blue"
          @click="loadUsers()"
          :disabled="allUsersAdded"
        >Add All</button> to
        <br>add all on your customer list
      </p>
      </span>
      <p class="rec-message mont text-uppercase">Message</p>
      <p class="rec-text position-relative">
        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis
        <span
          class="rec-text-counter mont"
        >250/1000</span>
      </p>
      <p
        v-if="userInformation.id && userInformation.parentPage === 'recommended'"
        class="d-flex align-items-center"
      >
        <i class="add-showing-info mr-2 fas fa-info-circle"></i>
        <span class="add-showing-text">You can add showing directly in the
          <br>message attachments by clicking on
        </span>
        <i class="add-showing-plus text-center ml-1 pointer">+</i>
      </p>
      <div class="d-flex justify-content-between align-items-center">
        <p
          v-if="userInformation.user && userInformation.parentPage === 'concierge'"
          class="d-flex align-items-center"
        >
          <i class="add-showing-info mr-2 fas fa-info-circle"></i>
          <span class="add-showing-text">
            Your message will be posted to {{privacy ? "private" : "public"}} on
            <br>
            {{ userInformation.user.first_name }}'s profile.
          </span>
        </p>
        <div>
          <input type="checkbox" v-model="privacy" id="switch-privacy" class="toggle-input d-none">
          <label
            for="switch-privacy"
            class="toggle-label text-uppercase mont text-center pointer flex"
          >{{privacy ? "Private" : "Public"}}</label>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn
        size="sm"
        class="float-left mr-2"
        variant="primary"
        @click="send()"
        v-if="userInformation.thumbsDown === false"
      >
        Send
      </b-btn>
      <b-btn
        size="sm"
        class="float-left mr-2"
        variant="primary"
        @click="send()"
        v-if="userInformation.thumbsDown === true"
      >
      Save Changes
      </b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">Cancel x</b-btn>
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
      currentRoute: "",
      myUsers: [],
      addedUser: "",
      allUsersAdded: false,
      privacy: false
    };
  },
  methods: {
    loadUsers() {
      this.$parent.showLoading = true;
      let url = "";
      if (this.userInformation.parentPage === "recommended") {
        axios
          .get("api/realtor/dashboard/customer/?buyer=1")
          .then(res => {
            console.log(res);
            let i = 0;
            for (i = 0; i < res.data.results.length; i++) {
              this.myUsers.push(res.data.results[i].user.username);
            }
            //this.$toastr("success", "Status update successfully", "Success!");
            //this.$parent.viewModalShow = false;
            this.$parent.showLoading = false;
            this.allUsersAdded = true;
          })
          .catch(error => {
            this.$toastr("error", error, "Error");
            this.$parent.showLoading = false;
            this.allUsersAdded = false;
          });
      } else if (this.userInformation.parentPage === "concierge") {
        let i = 0;
        //alert(this.userInformation.realtor_users[0].customer__user__first_name);

        for (i = 0; i < this.userInformation.realtor_users.length; i++) {
          this.myUsers.push(
            this.userInformation.realtor_users[i].customer__user__first_name
          );
        }

        this.$parent.showLoading = false;
      }
    },

    addUsers(a) {
      this.myUsers.push(a);
    },

    send() {
      this.$parent.showLoading = true;
      let url = "";

      if (this.userInformation.parentPage === "recommended") {
        url = `/api/realtor/listings/${
          this.userInformation.uid
        }/add_recommend/`;
      } else if (this.userInformation.parentPage === "concierge") {
        url = `api/realtor/team/concierge/${this.userInformation.uid}/recommend/`;
      }

      axios
        .post(url, { usernames: this.myUsers })
        .then(res => {
          this.$toastr("success", "Recommendation Sent!", "Success!");
          this.$parent.recViewModalShow = false;
          this.$parent.showLoading = false;
        })
        .catch(error => {
          this.$toastr("error", error, "Error");
          this.$parent.showLoading = false;
        });
    },

    cancel() {
      this.$parent.recViewModalShow = false;
    },

    openContactModal(role) {
      this.$parent.userRole = role;
      this.$parent.viewModalShow = false;
      this.$parent.contactModalShow = true;
    }
  },
  props: {
    recViewModalShow: Boolean,
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
  mounted() {}
};
</script>

<style scoped>
.pad-rec {
  padding-left: 110px;
}
</style>

