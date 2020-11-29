<template>
  <b-modal v-model="modalShow" hide-header hide-footer size="md" @hide="hideRecommendModal()">
    <div class="row">
      <div class="col-md-12">
        <div class="recommend-description">
          <img src="/img/recommend.svg" alt="recommend" />
          <p>Recommend Home Captain to your co-workers and business friends.</p>
          <div class="clearfix"></div>
        </div>
      </div>
      <div class="col-md-12">
        <div class="custom-input-div">
          <div class="custom-input-container" v-bind:class="{'input-has-value': email}">
            <label>Enter email</label>
            <input type="email" v-model="email" @keyup.enter="recommendUS()"/>
            <span @click="recommendUS()"><i class="fas fa-paper-plane"></i></span>
          </div>
        </div>

        <div class="custom-dropdown-container">
          <label>USER TYPE:</label>
          <b-dropdown>
            <template slot="button-content">
              {{userType}}
            </template>
            <b-dropdown-item v-for="type in userTypes" @click="setUserType(type)">{{type}}</b-dropdown-item>
          </b-dropdown>
          <i class="fas fa-angle-down type-dropdown"></i>
        </div>
      </div>
      <div class="col-md-12 m-t-10">
        <b-button class="btn-cancel float-right" :size="'sm'" @click="hideRecommendModal()">
          CANCEL &nbsp;<i class="fas fa-times"></i>
        </b-button>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { mapState, mapActions } from "vuex";
import $ from "jquery";
import axios from "../axios-auth";
import store from "../store";


export default {
  name: "recommendUsModal",
  components: { },
  data() {
    return {
      email: "",
      userType: "Home Buyer",
      userTypes: ["Home Buyer", "Home Seller", "Realtor", "Loan Officer"],
    };
  },
  methods: {
    hideRecommendModal() {
      this.$parent.showRecommendModal = false;
    },
    setUserType(type) {
      this.userType = type;
    },
    recommendUS() {
      const self = this;

      let data = {
        email: this.email,
        user_type: "",
      };

      let tempArray = this.userType.split(" ");
      for(let i=0; i<tempArray.length; i++) {
        tempArray[i] = tempArray[i].toLowerCase();
      }

      data.user_type = tempArray.join("-");
      axios
        .post("/api/realtor/recommend-us/", data)
        .then((res) => {
          self.$toastr("success", "HomeCaptain has been recommended", "Success!");
          self.hideRecommendModal();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  props: {
    modalShow: Boolean,
  },
  computed: {
    ...mapState(["idToken", "loading"]),
  },
  mounted() {
    $(".custom-input-container input").focusin((e) => {
      $(e.target).parent().addClass("input-focused");
    });

    $(".custom-input-container input").focusout((e) => {
      $(e.target).parent().removeClass("input-focused");
    });
  },
};
</script>

<style scoped>
  .m-t-10 {
    margin-top: 10px;
  }
</style>
