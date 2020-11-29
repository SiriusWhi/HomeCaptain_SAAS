<template>
  <b-modal v-model="archiveModalShow" title="Do you really want to archive this buyer?" @hide="cancel()">
    <div class="row">
      <div class="col-md-12">
        <p class="card-contacts-a text-uppercase mont font-weight-bold m-10">You can access archived buyers from your Archive tab later on.</p>
        <p>
          <textarea rows="5" class="email-textarea" placeholder="leave a note so you know why you have archived this buyer"></textarea>
        </p>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="archive()">Confirm</b-btn>
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">
        Cancel <img src="../../public/img/icons/close-icon.svg" width="18"/>
      </b-btn>
    </div>

  </b-modal>
</template>


<script>
import axios from "../axios-auth";
import { mapState, mapActions } from "vuex";
import store from "../store";

export default {
  name: "archiveModal",
  components: {},
  data() {
    return {};
  },
  methods: {
    archive() {
      axios
        .post(this.url)
        .then(res => {
          this.$parent.archiveModalShow = false;
          this.$toastr("success", "Archived successfully", "Success!");
        })
        .catch(error => {
          this.$toastr("error", error, "Error");
        });
    },
    cancel() {
      this.$parent.archiveModalShow = false;
    }
  },
  props: {
    archiveModalShow: Boolean,
    uid: String,
    url: String,
  },
  computed: {
    ...mapState(["idToken", "loading"])
  },
  mounted() {}
};
</script>
