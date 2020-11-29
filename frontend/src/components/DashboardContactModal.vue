<template>
  <b-modal v-model="contactModalShow" title="Edit Status" @hide="cancel()">
    <div class="row col-md-12">
      <div class="col-md-2">
        <p v-if="userInformation.buyerName" :data-letters="userInformation.buyerName[0]"
           class="buyer-avatar card-avatar float-left bg_3 ml-0"></p>
      </div>
      <div class="col-md-10">
        <p class="change-status-avatar" v-if="userInformation.buyerName">
          {{ userInformation.buyerName }}</p>
        <p>
          <button class="btn mr-2 btn-primary btn-sm" style="padding: 4px 15px;">
            <img width="16"
                 src="../../public/img/icons/call.svg"
                 class="mr-3"/>Call
          </button>
        </p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Email
          <span v-if="userInformation.buyerName">{{userInformation.buyerName}}</span></p>
        <p class="email-text" v-if="userInformation.email">{{userInformation.email}}
          <img src="../../public/img/icons/copy.svg" width="18" class="ml-2"></p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Subject</p>
        <input type="text" placeholder="Subject Goes Here" v-model="email.subject"
               style="border:none; border-bottom: 2px solid #0000001A; width: 100%"/>
        <p>
        <div class="email-send-icon">
          <img src="../../public/img/icons/send.svg"/>
        </div>
        <p>
          <textarea rows="5" class="email-textarea mt-4" v-model="email.body"></textarea>
        </p>
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">SEND A DIRECT MESSAGE</p>
        <p>
        <div class="email-send-icon mt-1">
          <img src="../../public/img/icons/send.svg"/>
        </div>
        <p>
          <textarea rows="5" class="email-textarea"></textarea>
        </p>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="sendEmail()">
        Send
      </b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Close <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
  import axios from "../axios-auth";
  import {mapState, mapActions} from "vuex";
  import store from "../store";

  export default {
    name: "contactModal",
    components: {},
    data() {
      return {};
    },
    methods: {
      sendEmail() {
        this.email.uid = this.userInformation.userId;
        axios
          .post("api/realtor/email/customer/", this.email)
          .then((res) => {
            this.$parent.contactModalShow = false;
            this.$toastr("success", "Email sent successfully", "Success!");
          }).catch((error) => {
          this.$toastr("error", error, "Error");
        });
      },
      cancel() {
        this.$parent.contactModalShow = false;
      }
    },
    props: {
      contactModalShow: Boolean,
      userInformation: Object,
      email: Object
    },
    computed: {
      ...mapState(["idToken", "loading"])
    },
    mounted() {
    }
  };
</script>
