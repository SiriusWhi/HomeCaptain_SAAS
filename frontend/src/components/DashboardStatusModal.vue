<template>
  <b-modal v-model="modalShow" title="Edit Status" @hide="cancel()">
    <div class="row col-md-12">
      <div class="col-md-2">
        <p v-if="userInformation.fullName" :data-letters="userInformation.fullName[0]"
           class="buyer-avatar card-avatar float-left bg_4 ml-0"></p>
      </div>
      <div class="col-md-8">
        <p class="change-status-avatar" v-if="userInformation">{{ userInformation.fullName }}</p>
        <p class="card-doc flex">
          <span class="card-contacts-a text-uppercase mont font-weight-bold">Status</span>
          <!-- <span class="ml-3" v-if="userInformation">{{ userInformation.milestones }}</span> -->
          <select class="hc-select status-filter" v-model="userInformation.milestones">
            <template v-for="m in milestones">
              <option v-if="m[0] !== ''" :value="m[0]" v-bind:key="m[0]">{{ m[0] }}</option>
            </template>
          </select>
        </p>
      </div>
    </div>
    <div class="row col-md-12">
      <div class="col-md-12">
        <label>Status Change History</label>
      </div>
      <div class="col-md-12">
        <div v-for="history in userInformation.customer_update_history">{{history.previous_milestone}}</div>
        <!-- <v-select v-model="userInformation.milestones" :options="milestones"></v-select> -->
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="changeStatus()">
        Save Changes
      </b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Discard Changes x
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
        delete this.userInformation.userId;
        axios
          .patch(`/api/realtor/dashboard/customer/${this.userInformation.uid}/`, this.userInformation)
          .then((res) => {
            this.$toastr("success", "Status updated successfully", "Success!");
            this.$parent.modalShow = false;
            this.$parent.populateDashboard();
            this.$parent.getStats();
          }).catch((error) => {
          this.$toastr("error", error, "Error");
        });
      },
      cancel() {
        this.$parent.modalShow = false;
        this.$parent.populateDashboard();
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
      //alert(JSON.stringify(this.userInformation));
    }
  };
</script>
<style scoped>
.card-doc {
  display: inline-block;
  padding: 0 15px;
}
</style>
