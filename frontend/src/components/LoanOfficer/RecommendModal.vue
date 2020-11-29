<template>
  <b-modal v-model="recommendModalShow" class="favorites-view" size="lg" @hide="cancel()">
    <div class="row">
      <div class="col-md-2">
        <p
          v-if="userInformation.user" :data-avatar-popup="userInformation.user.first_name[0]"
          class="buyer-avatar user-avatar-popup card-avatar float-left bg_8 ml-6"
        ></p>
      </div>
      <div class="col-md-10">
        <div class="flex flex-column mb-4">
          <h3 v-if="userInformation.user" class="rec-title">{{userInformation.user.first_name}} {{userInformation.user.last_name}}</h3>
          <div>
            <article class="team-stars" v-b-tooltip.hover :title="rating + ' Star(s)'">
              <i v-for="(num, key) in ratings" v-bind:key="key" v-bind:class="[num<=Math.round(rating)? 'fas fa-star': 'far fa-star']"></i>
              <!-- <i class="fas fa-star"></i>
              <i class="fas fa-star-half-alt"></i> -->
            </article>
            <span class="based-on">Based on
              <strong>{{userInformation.recommend_count + userInformation.discourage_count}}</strong> reviews
            </span>
          </div>
        </div>

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
        <p class="rec-message mont text-uppercase">Message</p>
        <textarea rows="3" class="email-textarea mb-4" v-model="message" placeholder="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis"></textarea>

        <div class="row">
          <div class="col-md-9">
            <p class="d-flex align-items-center">
              <i class="add-showing-info mr-2 fas fa-info-circle"></i>
              <span class="add-showing-text">Your message will be posted to public on Theodore profile
              </span>
            </p>
          </div>
          <div class="col-md-3">
            <toggle-button
              color="#4f83c3"
              :width="84"
              :height="30"
              :labels="{checked: 'PUBLIC', unchecked: 'PRIVATE'}"
              v-model="is_public"
            />
          </div>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex justify-content-between">
      <b-btn size="sm" class="float-left mr-2" variant="primary" @click="recommend()">Save Changes</b-btn>
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
      currentRoute: "",
      myUsers: [],
      addedUser: "",
      allUsersAdded: false,
      message: "",
      ratings: [1, 2, 3, 4, 5],
      is_public: true,
    };
  },
  methods: {
    loadUsers() {
      this.$parent.showLoading = true;
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
    },

    addUsers(a) {
      this.myUsers.push(a);
    },

    recommend() {
      this.$parent.showLoading = true;
      let url = `/api/realtor/team/loan-officer/${this.userInformation.uid}/recommend/`;
      axios
        .post(url, {
          receivers: this.myUsers,
          comments: this.message,
          // rating: 2,
          is_public: this.is_public
        })
        .then(res => {
          console.log(res)
          this.$toastr("success", "Recommendation Sent!", "Success!");
          this.$parent.recommendModalShow = false;
          this.$parent.showLoading = false;
          this.$parent.getLoanOfficers();
        })
        .catch(error => {
          this.$toastr("error", error, "Error");
          this.$parent.showLoading = false;
        });
    },

    cancel() {
      this.$parent.recommendModalShow = false;
    },

    openContactModal(role) {
      this.$parent.userRole = role;
      this.$parent.viewModalShow = false;
      this.$parent.contactModalShow = true;
    }
  },
  props: {
    recommendModalShow: Boolean,
    userInformation: Object,
    userRole: String,
  },
  computed: {
    ...mapState(["idToken", "loading"]),
    rating: function() {

      let rate = (this.userInformation.recommend_count + this.userInformation.discourage_count !== 0) ?
        5*this.userInformation.recommend_count / (this.userInformation.recommend_count + this.userInformation.discourage_count)
        : 0;
      return rate;
    }
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
