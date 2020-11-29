<template>
  <b-modal v-model="viewModalShow" class="favorites-view" size="lg" @hide="cancel()" >
    <div class="row">
      <div class="col-md-2">
        <p
          v-if="userInformation.user"
          class="buyer-avatar user-avatar-popup card-avatar float-left bg_8 ml-6"
          :data-avatar-popup="userInformation.user.first_name[0]"
        ></p>
      </div>
      <div class="col-md-10">
        <div class="row">
          <div v-if="userInformation.user" class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Full Name</p>
            <p class="bordered-input pointer bordered-text">{{userInformation.user.first_name}} {{userInformation.user.last_name}}</p>
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Location</p>
            <p class="bordered-input pointer bordered-text">{{userInformation.user.address}}</p>
          </div>
          <div class="col-md-6" v-if="userInformation.lender">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Lender Name</p>
            <p class="bordered-input pointer bordered-text">{{userInformation.lender.name}}</p>
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Pre-Qualification Amount</p>
            <p class="bordered-input pointer bordered-text">$100.000/$200.000</p>
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Closing Scheduled</p>
            <p class="bordered-input pointer bordered-text">Jan 23, 2019</p>
          </div>
        </div>
        <hr>
        <div>
          <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">About Theodore</p>
          <textarea rows="3" style="resize: none;" class="email-textarea mb-4" disabled></textarea>
        </div>
        <div>
          <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Lender Bio</p>
          <textarea rows="3" style="resize: none;" class="email-textarea mb-4" disabled></textarea>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="save()">Save Changes</b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Cancel <img src="../../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
import axios from "../../axios-auth";
import { mapState, mapActions } from "vuex";
import store from "../../store";

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
    recommend(){
      this.$parent.viewModalShow = false;
      this.$parent.recViewModalShow = true;
    }
  },
  props: {
    viewModalShow: Boolean,
    userInformation: Object,
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
