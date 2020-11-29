<template>
  <div class="card" v-if="item">
    <div class="row">
      <div class="search-bkg"></div>
      <div class="card-av card-av-search flex mont ml-2">
        <span class="card-name text-left" v-if="item.address">
          {{item.address.street}}
          <br>
          {{item.address.city}} {{item.address.state}} {{item.address.postalcode}}
        </span>
      </div>
      <span class="rec-date search-rec-date mont text-center">30 Dec 2018</span>
      <span class="card-range search-range pull-right">${{item.target_price_maximum | Commas}}</span>
      <div class="actions">
        <button class="small" @click="onFavorite(item)">
          <i class="fas fa-star"></i>
        </button>
        <button class="large" @click="onShowInfo(item)">
          <i class="fas fa-info-circle"></i>
        </button>
        <button class="small" @click="onRecommend(item)">
          <i class="fas fa-share-alt"></i>
        </button>
      </div>
      <article class="card-container">
        <div class="row">
          <div class="col-md-6">
            <ul class="list-reset search-list">
              <!--Commented for now, cause MLS have no integrated yet-->
              <!--<li class="card-list-item">-->
              <!--<span class="list-bullet lb-l"></span>-->
              <!--<span class="list-label text-uppercase mont">mls:</span>-->
              <!--<span class="list-value pull-right"></span>-->
              <!--</li>-->
              <li class="card-list-item">
                <span class="list-bullet lb-lo"></span>
                <span class="list-label text-uppercase mont">SQFT:</span>
                <span class="list-value pull-right">{{item.square_feet}} sq/ft</span>
              </li>
              <li class="card-list-item">
                <span class="list-bullet lb-c"></span>
                <span class="list-label text-uppercase mont">Bedrooms:</span>
                <span class="list-value pull-right">{{item.bedrooms}}</span>
              </li>
              <li class="card-list-item">
                <span class="list-bullet lb-g"></span>
                <span class="list-label text-uppercase mont">Bathrooms:</span>
                <span class="list-value pull-right">{{item.bathrooms}}</span>
              </li>
            </ul>
          </div>
          <div class="col-md-6">
            <p class="scheduled-showing" @click="showSchedules(item)">
              <span
                class="schedule-qty"
              >{{item.scheduled_showings? item.scheduled_showings.count : 0}}</span>
              <span class="schedule-label"># of Schedules</span>
            </p>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <button class="submit card-contact" @click="showAgendaModal(item)">
              <i class="fas fa-play"></i> &nbsp;
              Request Showing
            </button>
          </div>
          <div class="flex card-btn-wrap col-md-6">
            <button class="card-btn text-uppercase mont" @click="onRestore !== undefined? onRestore(item.uid) : onArchiveItem(item)">
              {{onRestore !== undefined? 'restore' : 'archive'}}
              <i class="far fa-trash-alt"></i>
            </button>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import axios from "../axios-auth";
import Commas from "@/filters/commas";

export default {
  name: "cardSearch",
  data() {
    return {
      thumbsDown: false
    };
  },
  props: {
    item: Object,
    i: Number,
    onRestore: Function,
  },
  filters: {
    Commas
  },
  methods: {
    onFavorite(item) {
      // axios
      //   .get(`/api/realtor/listings/${item.uid}/add_favorite/`)
      //   .then((res) => {
      //     this.$toastr("info", "", res.data[0]);
      //     console.log(res);
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //     this.showDismissibleAlert = true;
      //   });
    },
    onRecommend(item) {
      // axios
      //   .get(`/api/realtor/listings/${item.uid}/add_recommend/`)
      //   .then((res) => {
      //     this.$toastr("info", "", res.data[0]);
      //     console.log(res);
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //     this.showDismissibleAlert = true;
      //   });
    },
    onShowInfo(item) {
      this.$parent.detailModalShow = true;
      this.$parent.detailItem = item;
    },
    showSchedules(item) {
      if (item.scheduled_showings.count) {
        this.$parent.scheduleModalShow = true;
        this.$parent.scheduleList = item.scheduled_showings.showings;
      }
    },
    showAgendaModal(listItem) {
      this.$root.$emit("show-agenda-modal", { item: listItem, cid: "" });
    },
    onArchiveItem(item) {
      const self = this.$parent;

      axios
        .post("/api/realtor/listings/" + item.uid + "/archive/")
        .then(res => {
          self.getLists();
          self.$toastr("success", "Archived Successfully.", "Success!");
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>
<style scoped>
.actions button {
  cursor: pointer;
}
.card-btn-wrap {
  justify-content: flex-end;
}
.card-btn {
  font-size: 13px;
}
</style>
