<template>
  <b-modal v-model="contactModalShow" title="Contact" @hide="cancel()">
    <div class="row col-md-12">
      <div class="col-md-3">
        <p
          v-if="userInformation.user && this.$parent.userRole === ''"
          :data-avatar-medium-popup="userInformation.user.first_name[0]"
          class="buyer-avatar-medium float-left bg_3 ml-0"
        ></p>
        <!-- <p
          v-if="userInformation.user && this.$parent.userRole === 'officer'"
          :data-letters="userInformation.requirements[0].loan_officer.user.first_name[0]"
          class="buyer-avatar card-avatar float-left bg_3 ml-0"
        ></p>
        <p
          v-if="userInformation.user && this.$parent.userRole === 'concierge'"
          :data-letters="userInformation.requirements[0].concierge.user.first_name[0]"
          class="buyer-avatar card-avatar float-left bg_3 ml-0"
        ></p> -->
        <p
          v-if="userInformation.loan_officer && this.$parent.userRole === 'officer'"
          :data-avatar-medium-popup="userInformation.loan_officer.user.first_name[0]"
          class="buyer-avatar-medium float-left bg_3 ml-0"
        ></p>
        <p
          v-if="userInformation.concierge && this.$parent.userRole === 'concierge'"
          :data-avatar-medium-popup="userInformation.concierge.user.first_name[0]"
          class="buyer-avatar-medium float-left bg_3 ml-0"
        ></p>
      </div>
      <div class="col-md-9">
        <p
          class="change-status-avatar"
          v-if="userInformation.user && this.$parent.userRole === ''"
        >{{ userInformation.user.first_name }} {{userInformation.user.last_name }}</p>
        <!-- <p
          class="change-status-avatar"
          v-if="userInformation.user && this.$parent.userRole === 'officer'"
        >{{ userInformation.requirements[0].loan_officer.user.first_name }} {{userInformation.requirements[0].loan_officer.user.last_name }}</p>
        <p
          class="change-status-avatar"
          v-if="userInformation.user && this.$parent.userRole === 'concierge'"
        >{{ userInformation.requirements[0].concierge.user.first_name }} {{ userInformation.requirements[0].concierge.user.last_name }}</p> -->
        <p
          class="change-status-avatar"
          v-if="userInformation.loan_officer && this.$parent.userRole === 'officer'"
        >{{ userInformation.loan_officer.user.first_name }} {{userInformation.loan_officer.user.last_name }}</p>
        <p
          class="change-status-avatar"
          v-if="userInformation.concierge && this.$parent.userRole === 'concierge'"
        >{{ userInformation.concierge.user.first_name }} {{ userInformation.concierge.user.last_name }}</p>
        <p>
          <button class="btn mr-2 btn-primary btn-sm btn-call">
            <img width="16" src="../../public/img/icons/call.svg" class="mr-3">Call
          </button>
        </p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">
          Email
          <span
            v-if="userInformation.user && this.$parent.userRole === ''"
          >{{userInformation.user.first_name}}</span>
          <!-- <span
            v-if="userInformation.user && this.$parent.userRole === 'officer'"
          >{{ userInformation.requirements[0].loan_officer.user.first_name }}</span>
          <span
            v-if="userInformation.user && this.$parent.userRole === 'concierge'"
          >{{ userInformation.requirements[0].concierge.user.first_name }}</span> -->
          <span
            v-if="userInformation.loan_officer && this.$parent.userRole === 'officer'"
          >{{ userInformation.loan_officer.user.first_name }}</span>
          <span
            v-if="userInformation.concierge && this.$parent.userRole === 'concierge'"
          >{{ userInformation.concierge.user.first_name }}</span>
        </p>
        <p class="email-text" v-if="userInformation.user">
          <span v-if="this.$parent.userRole === '' && userInformation.user">{{userInformation.user.email}}</span>
          <!-- <span
            v-if="userInformation.user && this.$parent.userRole === 'officer'"
          >{{ userInformation.requirements[0].loan_officer.user.email}}</span>
          <span
            v-if=" userInformation.user && this.$parent.userRole === 'concierge'"
          >{{ userInformation.requirements[0].concierge.user.email}}</span> -->
          <span
            v-if="userInformation.loan_officer && this.$parent.userRole === 'officer'"
          >{{ userInformation.loan_officer.user.email}}</span>
          <span
            v-if="userInformation.concierge && this.$parent.userRole === 'concierge'"
          >{{ userInformation.concierge.user.email}}</span>
          <img src="../../public/img/icons/copy.svg" width="18" class="ml-2">
        </p>
        <p class="email-text" v-if="this.$parent.selectedUser">
          <span v-for="user in this.$parent.selectedUsers">{{ user.user.email}}
            <img src="../../public/img/icons/copy.svg" width="18" class="ml-2"><br/>
          </span>
        </p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Subject</p>
        <input
          type="text"
          placeholder="Subject Goes Here"
          v-model="email.subject"
          style="border:none; border-bottom: 2px solid #0000001A; width: 100%"
        >
        <p></p>
        <div class="email-send-icon">
          <img src="../../public/img/icons/send.svg">
        </div>
        <p>
          <textarea rows="4" class="email-textarea mt-4" v-model="email.body"></textarea>
        </p>
        <hr class="mont">
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">SEND A DIRECT MESSAGE</p>
        <p></p>
        <div class="email-send-icon mt-1">
          <img src="../../public/img/icons/send.svg">
        </div>
        <p>
          <textarea rows="2" class="email-textarea"></textarea>
        </p>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="sendEmail()">Send</b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Close <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
import axios from "../axios-auth";
import { mapState, mapActions } from "vuex";
import store from "../store";

export default {
  name: "contactModal",
  components: {},
  data() {
    return {};
  },
  methods: {
    sendEmail() {
      let url = "";
      // if (this.userInformation.user && this.$parent.userRole === "officer") {
      //   this.email.uid = this.userInformation.requirements[0].loan_officer.user.uid;
      //   url = `/api/realtor/email/loan-officer/`;
      // } else if (this.userInformation.user && this.$parent.userRole === "concierge") {
      //   this.email.uid = this.userInformation.requirements[0].concierge.user.uid;
      //   url = `/api/realtor/email/concierge/`;
      // } else
      if (this.userInformation.loan_officer && this.$parent.userRole === "officer") {
        this.email.uid = this.userInformation.loan_officer.user.uid;
        url = `/api/realtor/email/loan-officer/`;
      } else if (this.userInformation.concierge && this.$parent.userRole === "concierge") {
        this.email.uid = this.userInformation.concierge.user.uid;
        url = `/api/realtor/email/concierge/`;
      } else if(this.$parent.selectedUsers && this.$parent.selectedUsers.length > 0) {
        this.email.uid = this.$parent.checkedArray;
        url = `api/realtor/email/customer/`;
      } else {
        this.email.uid = this.userInformation.user.uid;
        url = `api/realtor/email/customer/`;
      }
      axios
        .post(url, this.email)
        .then(res => {
          this.$parent.contactModalShow = false;
          this.$router.go(this.$router.currentRoute);
          this.$toastr("success", "Email sent successfully", "Success!");
        })
        .catch(error => {
          this.$toastr("error", error, "Error");
        });
    },
    cancel() {
      this.$parent.contactModalShow = false;
      this.$parent.selectedUsers = [];
      // this.$parent.userInformation = {};
      // this.userInformation = {};
    }
  },
  props: {
    contactModalShow: Boolean,
    userInformation: Object,
    email: Object,
    userRole: String
  },
  computed: {
    ...mapState(["idToken", "loading"])
  },
  mounted() {}
};
</script>
<style scoped>
.btn-call {
  padding: 4px 15px;
  border-radius: 5px;
  background-color: #2c71c7;
  box-shadow: 0px 20px 30px -5px rgba(44,113,199,0.4);
}
hr {
  position: relative;
  display: flex;
  justify-content: center;
  margin: 22px 0 32px;
}
hr:before {
  content: 'MORE OPTIONS';
  position: absolute;
  top: -7px;
  line-height: 14px;
  padding: 0 19px;
  background: white;
  color: #808080;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
}
</style>
