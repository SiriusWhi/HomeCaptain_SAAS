<template>
  <div class="card" v-if="concierge">
    <div class="flex mb-4">
      <div class="position-relative">
        <p
          :data-letters="concierge.user.first_name[0]"
          :class="'bg_'+i"
          class="buyer-avatar co-buyer-avatar ml-6"
        ></p>
        <span class="available"></span>
      </div>
      <div class="team-list">
        <p
          class="card-name text-left"
        >{{concierge.user.first_name}} {{concierge.user.last_name}}</p>
        <div class="c-reviews justify-content-between d-flex">
          <p class="mb-1 thumbs-up" @click="thumbsDown = false, showRecommendModal(concierge.uid)">
            <i class="fas fa-thumbs-up mr-1"></i>
            <span>43</span>
          </p>
          <p class="mb-1 thumbs-up" @click="thumbsDown = true, showRecommendModal(concierge.uid)">
            <i class="fas fa-thumbs-down mr-1"></i>
            <span>12</span>
          </p>
        </div>
        <ul class="list-reset search-list">
          <li class="team-card-list-item card-list-item">
            <div>
              <span class="list-bullet lb-l"></span>
              <span class="list-label co-list-label text-uppercase mont">location:</span>
              <span class="list-value co-list-value pull-right">United States</span>
            </div>
          </li>
        </ul>
      </div>
      <div>
        <p class="faves-p faves-first position-absolute" @click="showFavoritesModal(i)">
          <span class="faves-qty">{{concierge.realtor_users? concierge.realtor_users.length : 0}}</span>
          <span class="faves-label"># of Clients</span>
        </p>
      </div>
    </div>
    <div class="flex justify-content-between">
      <button class="submit card-contact" @click="showContactModal(i)">Contact</button>
      <div class="flex card-btn-wrap">
        <button class="card-btn text-uppercase mont" @click="onRestore !== undefined? onRestore(concierge.uid) : archiveCon(i)">
          {{onRestore !== undefined? 'restore' : ($parent.priorFilter === false ? "Archive" : "Restore")}}
          <i class="far fa-trash-alt"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";

export default {
  name: "cardConcierge",
  data() {
    return {
      thumbsDown: false,
    };
  },
  props: {
    concierge: Object,
    i: Number,
    onRestore: Function,
  },
  methods: {
    showRecommendModal(uid) {
      this.$parent.recViewModalShow = true;
      this.$parent.modalShow = false;
      var list = this.$parent.concierges ? this.$parent.concierges : this.$parent.archives

      this.$parent.selectedUser = list.find(obj => {
        console.log(JSON.stringify(obj));
        return obj.uid === uid;
      });
      this.$parent.selectedUser.parentPage = "concierge";
      //alert(this.thumbsDown);
      //if(this.thumbsDown === true ) {
        this.$parent.selectedUser.thumbsDown = this.thumbsDown;
      //}
    },
    showFavoritesModal(i) {
      this.$parent.favoritesModalShow = true;
      this.$parent.modalShow = false;
      this.$parent.viewModalShow = false;
      var list = this.$parent.concierges ? this.$parent.concierges : this.$parent.archives
      this.$parent.selectedUser = list[i];
      this.$parent.selectedUser.parentPage = "concierge";
    },
    showContactModal(i) {
      this.$parent.contactModalShow = true;
      this.$parent.userRole = "concierge";
      let obj = {};
      var list = this.$parent.concierges ? this.$parent.concierges : this.$parent.archives
      obj.concierge = list[i];
      this.$parent.selectedUser = obj;
    },
    archiveCon(i) {
      this.$parent.showLoading = true;

      var arr = this.$parent.concierges ? this.$parent.concierges : this.$parent.archives
      let url;

      if (this.$parent.priorFilter === true) {
        url = `api/realtor/team/concierge/${arr[i].uid}/unarchive/?prior=1`;
      } else {
        url = `api/realtor/team/concierge/${arr[i].uid}/archive/`;
      }

      axios
        .post(url)
        .then(res => {
          console.log(res);
          this.$parent.populateDashboard();
          this.$parent.showLoading = false;

          if (this.$parent.priorFilter === true) {
            this.$parent.$toastr("success", "Concierge Restored", "Success!");
          } else {
            this.$parent.$toastr("success", "Concierge Archived", "Success!");
          }
        })
        .catch(error => {
          console.log(error);
          this.$parent.showLoading = false;
          this.$parent.showDismissibleAlert = true;
          this.$parent.$toastr("error", error, "Error");
        });
    }
  },
}
</script>
