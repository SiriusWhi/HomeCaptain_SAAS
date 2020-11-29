<template>
  <div class="card" v-if="officer">
    <div class="flex-center mb-4">
      <div class="position-relative">
        <!--<img src="../../public/img/avatar3.png" class="card-avatar" alt="Avatar">-->
        <!--<span class="available"></span>-->
        <p :data-avatar-medium-popup="officer.user.first_name[0]" :class="'bg_'+i" class="buyer-avatar-medium ml-6"></p>
      </div>
      <div class="team-list">
        <p class="card-name text-left">{{officer.user.first_name}} {{officer.user.last_name}}</p>
        <span class="vote" @click="showRecommendModal(officer)">
          <i class="fas fa-thumbs-up"></i> {{officer.recommend_count}}
        </span>
        <span class="vote" @click="showDiscourageModal(officer)">
          <i class="fas fa-thumbs-down"></i> {{officer.discourage_count}}
        </span>
      </div>
      <p class="clients-panel" @click="showFavoritesModal(officer)">
        <span class="faves-qty">{{officer.realtor_users? officer.realtor_users.length : 0}}</span>
        <span class="faves-label"># of Clients</span>
      </p>
    </div>
    <div class="content">
      <ul class="list-reset search-list">
        <li class="team-card-list-item card-list-item flex-center">
          <span class="list-bullet lb-l"></span>
          <span class="list-label lo-list-label text-uppercase mont">location:</span>
          <span class="list-value lo-list-value">{{officer.user.address}}</span>
        </li>
        <li class="team-card-list-item card-list-item flex-center">
          <span class="list-bullet lb-lo"></span>
          <span class="list-label lo-list-label text-uppercase mont">lender:</span>
          <span class="list-value lo-list-value name">{{officer.lender? officer.lender.name : ""}}</span>
          <a href="#" class="card-contacts-a text-uppercase mont contact" @click="showContactModalForLender(officer.lender)">Contact</a>
        </li>
      </ul>
    </div>
    <div class="flex-center justify-content-between">
      <button class="submit card-contact" @click="showContactModal(officer)">Contact</button>
      <div class="flex-center card-btn-wrap">
        <button class="card-btn text-uppercase mont" @click="showViewModal(officer)">
          <i class="fas fa-pen"></i> View
        </button>
        <button class="card-btn text-uppercase mont" @click="onRestore !== undefined? onRestore(officer.uid) : showArchiveModal(officer.uid)">
          {{onRestore !== undefined? 'restore' : 'archive'}}
          <i class="far fa-trash-alt"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "cardLoanOfficer",
  data() {
    return {
    };
  },
  props: {
    officer: Object,
    i: Number,
    onRestore: Function,
  },
  methods: {
    showRecommendModal(officer) {
      this.$parent.recommendModalShow = true;
      this.$parent.selectedUser = officer;
    },
    showDiscourageModal(officer) {
      this.$parent.discourageModalShow = true;
      this.$parent.selectedUser = officer;
    },
    showFavoritesModal(officer) {
      this.$parent.favoritesModalShow = true;
      this.$parent.selectedUser = officer;
      let realtor_users = officer.realtor_users;
      for(let user in realtor_users) {
        realtor_users[user].first_name = realtor_users[user].customer__user__first_name;
        realtor_users[user].uid = realtor_users[user].customer__user__uid;
      }
      this.$parent.selectedUser.favoriting_buyers = officer.realtor_users;
    },
    showContactModalForLender(lender) {
      this.$parent.contactModalShow = true;
      this.$parent.selectedUser = lender;
    },
    showContactModal(officer) {
      this.$parent.contactModalShow = true;
      this.$parent.selectedUser = officer;
    },
    showViewModal(officer) {
      this.$parent.selectedUser = officer;
      this.$parent.viewModalShow = true;
    },
    showArchiveModal(uid) {
      this.$parent.archiveModalShow = true;
      this.$parent.url = `/api/realtor/team/loan-officer/${uid}/archive/`;
      this.$parent.uid = uid;
    },
  },
}
</script>
