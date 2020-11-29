<template>
  <b-modal v-model="editModalShow" size="lg" title="Edit" @hide="cancel()">
    <div class="row col-md-12">
      <div class="col-md-2">
        <p v-if="userInformation.fullName" :data-avatar-popup="userInformation.fullName[0]"
           class="buyer-avatar user-avatar-popup card-avatar float-left bg_8 ml-0"></p>
      </div>
      <div class="col-md-10">
        <div class="row">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">FULL NAME</p>
            <p class="change-status-avatar bordered-input bordered-text pb-0" v-if="userInformation.fullName">
              {{ userInformation.fullName }}
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
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">LOAN OFFICER</p>
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
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">CONCIERGE</p>
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
        <div class="row mt-5">
          <div class="col-md-6" v-if="userInformation.favorites">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0"># OF FAVORITES</p>
            {{userInformation.favorites.length}}
          </div>
          <div class="col-md-6" v-if="userInformation.requirements">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">DESIRED LOCATIONS</p>

            <div class="attendee-list">
              <div class="attendee-item" v-for="(location, index) in userInformation.locations" v-bind:key="location">
                <i class="fas fa-circle attendee-bullet"></i>
                <span class="attendee-name">{{location}}</span>
                <span class="attendee-action" @click="removeLocation(index)">
                  <i class="far fa-trash-alt"></i>
                </span>
              </div>
            </div>
            <input class="agenda-input" type="text" placeholder="Press enter to add new"
                    v-model="newLocation" @keyup.enter="addLocation">

            <!-- <p><span>{{userInformation.requirements[0].desired_city_1}}<span
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
                               class="fa fa-trash float-right"></span></a></p> -->
          </div>
        </div>
        <div class="row mt-5">
          <div class="col-md-6">
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">APPOINTMENTS PENDING</p>
            <input type="text" placeholder="Enter a number" class="bordered-input"/>
          </div>
          <div class="col-md-6">
            <!-- <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">&nbsp;</p> -->
            <!-- <p class="bordered-input pointer bordered-text">Click to add new</p> -->
            <p class="card-contacts-a text-uppercase mont font-weight-bold m-0">LANGUAGES</p>

            <div class="attendee-list">
              <div class="attendee-item" v-for="(language, index) in userInformation.languages_spoken" v-bind:key="language">
                <i class="fas fa-circle attendee-bullet"></i>
                <span class="attendee-name">{{language}}</span>
                <span class="attendee-action" @click="removeLanguage(index)">
                  <i class="far fa-trash-alt"></i>
                </span>
              </div>
            </div>
            <input class="agenda-input" type="text" placeholder="Press enter to add new"
                    v-model="newLanguage" @keyup.enter="addLanguage">

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

  import EditModal from "@/components/DashboardEditModal.vue";

  export default {
    name: "editModal",
    components: {},
    data() {
      return {
        newLocation: "",
        newLanguage: "",
      };
    },
    methods: {
      addLocation() {
        const loc = this.newLocation.trim();
        if (loc && this.userInformation.locations.indexOf(loc) === -1) {
          this.userInformation.locations.push(loc);
          this.newLocation = "";
        }
      },
      removeLocation(index) {
        this.userInformation.locations.splice(index, 1);
      },
      addLanguage() {
        const lang = this.newLanguage.trim();
        if (lang && this.userInformation.languages_spoken.indexOf(lang) === -1) {
          this.userInformation.languages_spoken.push(lang);
          this.newLanguage = "";
        }
      },
      removeLanguage(index) {
        this.userInformation.languages_spoken.splice(index, 1);
      },
      save() {
        //delete this.userInformation.user.address;
        //delete this.userInformation.requirements[0].loan_officer.user.address;
        //delete this.userInformation.requirements[0].concierge.user.address;
        delete this.userInformation.userId;

        let url = '';
        for(let i=0; i<this.userInformation.locations.length; i++) {
          let ll = this.userInformation.locations[i].split(",");
          let city = ll[0].trim();
          if(this.userInformation.buyer_seller == "Buyer") {
            this.userInformation.requirements[0][`desired_city_${i+1}`] = city;
            this.userInformation.requirements[0][`desired_state_${i+1}`] = "";
          } else if(this.userInformation.buyer_seller == "Seller") {
            this.userInformation.properties[0][`desired_city_${i+1}`] = city;
            this.userInformation.properties[0][`desired_state_${i+1}`] = "";
          }
          if(ll.length > 1) {
            let state = ll[1].trim();
            if(this.userInformation.buyer_seller == "Buyer") {
              this.userInformation.requirements[0][`desired_state_${i+1}`] = state;
            } else if(this.userInformation.buyer_seller == "Seller") {
              this.userInformation.properties[0][`desired_state_${i+1}`] = state;
            }
          }
        }

        url = `/api/realtor/dashboard/customer/${this.userInformation.uid}/`;
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
    }
  };
</script>
