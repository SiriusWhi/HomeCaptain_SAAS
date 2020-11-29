<template>
  <b-modal v-model="modalShow" title="Edit Status" @hide="cancel()">
    <div class="row col-md-12">
      <div class="col-md-2">
        <p v-if="userInformation.user" :data-letters="userInformation.user.first_name[0]"
           class="buyer-avatar card-avatar float-left bg_4 ml-0"></p>
      </div>
      <div class="col-md-8">
        <p class="change-status-avatar" v-if="userInformation.user">{{ userInformation.user.first_name }} {{
          userInformation.user.last_name }}</p>
        <p class="card-doc flex" style="padding: 0 15px">
          <span class="card-contacts-a text-uppercase mont font-weight-bold">Status</span>
          <select class="hc-select status-filter" v-model="userInformation.milestones" style="background: transparent">
            <option v-bind:value="filter.milestones" v-for="filter in milestones">{{ filter.milestones_display }}</option>
          </select>
        </p>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="changeStatus()">
        Save Changes
      </b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Discard Changes <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>
  </b-modal>
</template>


<script>
  import axios from "../axios-auth";
  import {mapState, mapActions} from "vuex";
  import store from "../store";

  export default {
    name: "modal",
    components: {},
    data() {
      return {};
    },
    methods: {
      changeStatus() {
        delete this.userInformation.user.address;
        delete this.userInformation.requirements;

        let url = '';
        if (this.$router.app._route.name === 'homeSelling') {
          url = `/api/realtor/dashboard/home-buying/${this.userInformation.uid}/?seller=1`;
        } else {
          url = `/api/realtor/dashboard/home-buying/${this.userInformation.uid}/`;
        }

        axios
          .put(url, this.userInformation)
          .then((res) => {
            this.$toastr("success", "Status update successfully", "Success!");
            this.$parent.modalShow = false;
            this.$router.app._route.name === 'homeSelling' ? this.$parent.getSellers() : this.$parent.getBuyers()
            this.$parent.getStats();
          }).catch((error) => {
          this.$toastr("error", error, "Error");
        });
      },
      cancel() {
        this.$parent.modalShow = false;
        this.$router.app._route.name === 'homeSelling' ? this.$parent.getSellers() : this.$parent.getBuyers()
      },
    },
    props: {
      modalShow: Boolean,
      userInformation: Object,
      milestones: Array
    },
    computed: {
      ...mapState(["idToken", "loading"])
    },
    mounted() {
    }
  };
</script>
