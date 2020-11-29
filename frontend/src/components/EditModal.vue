<template>
  <b-modal v-model="editModalShow" size="lg" title="Edit" @hide="cancel()">
    <div class="row col-md-12">
      <div class="col-md-2">
        <p v-if="userInformation.user" :data-avatar-popup="userInformation.user.first_name[0]"
           class="buyer-avatar user-avatar-popup card-avatar float-left bg_8 ml-0"></p>
      </div>
      <div class="col-md-10">
        <div class="row">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">FULL NAME</p>
            <p class="change-status-avatar bordered-input bordered-text pb-0" v-if="userInformation.user">
              {{ userInformation.user.first_name }} {{userInformation.user.last_name }}
            </p>
          </div>
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">BATHROOMS</p>
            <input type="text" placeholder="Enter a number" v-if="userInformation.requirements"
                   class="bordered-input" v-model="userInformation.requirements[0].bathrooms"/>
          </div>
        </div>
        <div class="row mt-5">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">ASSIGNED LOAN OFFICER</p>
            <p class="bordered-input pointer bordered-text" v-if="userInformation.requirements">{{
              userInformation.requirements[0].loan_officer.user.first_name }}
              {{ userInformation.requirements[0].loan_officer.user.last_name }}
              <span class="float-right contact-icon" @click="openContactModal('officer')"><img width="16"
                                                                                               src="../../public/img/icons/contact.svg"/> Contact</span>
            </p>
          </div>
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">BEDROOMS</p>
            <input type="text" placeholder="Enter a number" v-if="userInformation.requirements" class="bordered-input"
                   v-model="userInformation.requirements[0].bedrooms"/>
          </div>
        </div>
        <div class="row mt-5">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">ASSIGNED CONCIERGE</p>
            <p class="bordered-input pointer bordered-text" v-if="userInformation.requirements">{{
              userInformation.requirements[0].concierge.user.first_name }}
              {{ userInformation.requirements[0].concierge.user.last_name }}
              <span class="float-right contact-icon" @click="openContactModal('concierge')"><img width="16"
                                                                                                 src="../../public/img/icons/contact.svg"/> Contact</span>
            </p>
          </div>
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">SQFT</p>
            <input type="text" placeholder="Enter a number" class="bordered-input" v-if="userInformation.requirements"
                   v-model="userInformation.requirements[0].square_feet"/>
          </div>
        </div>
        <div class="row mt-5" v-if="currentRoute === 'HomeBuying'">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0"># OF FAVORITES</p>
            <input type="text" placeholder="How many?" class="bordered-input" v-if="userInformation.requirements"
                   v-model="userInformation.requirements[0].favorites"/>
          </div>
          <div class="col-md-6" v-if="userInformation.requirements">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">DESIRED LOCATIONS</p>
            <p><span>{{userInformation.requirements[0].desired_city_1}}<span
                v-if="userInformation.requirements[0].desired_state_1">, </span>{{ userInformation.requirements[0].desired_state_1 }}</span><a
                href="#"><span v-if="userInformation.requirements[0].desired_city_1"
                               class="fa fa-trash float-right"></span></a></p>
            <p><span>{{userInformation.requirements[0].desired_city_2}}<span
                v-if="userInformation.requirements[0].desired_state_2">, </span>{{ userInformation.requirements[0].desired_state_2 }}</span><a
                href="#"><span v-if="userInformation.requirements[0].desired_city_2"
                               class="fa fa-trash float-right"></span></a></p>
            <p><span>{{userInformation.requirements[0].desired_city_3}}<span
                v-if="userInformation.requirements[0].desired_state_3">, </span>{{ userInformation.requirements[0].desired_state_3 }}</span><a
                href="#"><span v-if="userInformation.requirements[0].desired_city_3"
                               class="fa fa-trash float-right"></span></a></p>
          </div>
        </div>
        <div class="row mt-5" v-if="currentRoute === 'HomeBuying'">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">APPOINTMENTS PENDING</p>
            <input type="text" placeholder="Enter a number" class="bordered-input"/>
          </div>
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">&nbsp;</p>
            <p class="bordered-input pointer bordered-text">Click to add new</p>
          </div>
        </div>
        <div class="row mt-5 mb-5">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">Price Range</p>
            <div class="row price_inputs mt-3">
              <div class="input-group col-5">
                <div class="input-group-prepend">
                  <span class="input-group-text font-weight-bold pr-1">$</span>
                </div>
                <input type="text" class="form-control pl-1" v-if="userInformation.requirements"
                       v-model="userInformation.requirements[0].target_price_minimum"
                       aria-label="Amount (to the nearest dollar)">
              </div>
              <span class="mt-1"> - </span>
              <div class="input-group col-5">
                <div class="input-group-prepend">
                  <span class="input-group-text font-weight-bold pr-1">$</span>
                </div>
                <input type="text" class="form-control pl-1" v-if="userInformation.requirements"
                       v-model="userInformation.requirements[0].target_price_maximum"
                       aria-label="Amount (to the nearest dollar)">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="save()">
        Save Changes
      </b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Cancel <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
  import axios from "../axios-auth";
  import {mapState, mapActions} from "vuex";
  import store from "../store";

  export default {
    name: "editModal",
    components: {},
    data() {
      return {
        currentRoute: ""
      };
    },
    methods: {
      save() {
        delete this.userInformation.user.address;
        delete this.userInformation.requirements[0].loan_officer.user.address;
        delete this.userInformation.requirements[0].concierge.user.address;

        let url = '';
        if (this.$router.app._route.name === 'homeSelling') {
          url = `/api/realtor/dashboard/home-buying/${this.userInformation.uid}/?seller=1`
        } else {
          url = `/api/realtor/dashboard/home-buying/${this.userInformation.uid}/`;
        }

        axios
          .put(url, this.userInformation)
          .then((res) => {
            this.$toastr("success", "Status update successfully", "Success!");
            this.$parent.editModalShow = false;
          }).catch((error) => {
          this.$toastr("error", error, "Error");
        });
      },
      cancel() {
        this.$parent.editModalShow = false;
      },
      openContactModal(role) {
        this.$parent.userRole = role;
        this.$parent.editModalShow = false;
        this.$parent.contactModalShow = true;
      }
    },
    props: {
      editModalShow: Boolean,
      userInformation: Object,
      userRole: String
    },
    computed: {
      ...mapState(["idToken", "loading"])
    },
    mounted() {
      this.currentRoute = this.$route.name;
    }
  };
</script>
