<template>
  <b-modal
    v-model="buyerFavoritesModalShow"
    class="favorites-view"
    title="Favorites"
    size="lg"
    @hide="cancel()"
  >
    <div class="row">
      <div v-for="(favorite, k) in favoritesList" v-bind:key="k" class="col-md-12 item">
        <div class="flex">
          <img
            src="../../../public/img/house-bkg.png"
            class="rec-avatar"
            alt
          >
          <div class="dashboard__buyer-favorites__body">
            <span class="name">{{favorite.uid}}</span>
            <span class="description">{{favorite.address}} | {{favorite.bathrooms}} Bathrooms | {{favorite.bedrooms}} Bedrooms</span>
            <div class="footer">
              <span class="price">${{favorite.target_price_minimum | numberWithCommas}} - ${{favorite.target_price_maximum | numberWithCommas}}</span>
              <button class="card-btn text-uppercase" @click="showDetailModal(favorite)">
                <i class="fas fa-pen"></i> View
              </button>
            </div>
          </div>
          <button class="card-btn text-uppercase add-btn" @click="showAgendaModal(favorite)">
            <i class="fas fa-play"></i> Add Showing
          </button>
        </div>
        <hr/>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex">
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">x Hide</b-btn>
    </div>
  </b-modal>
</template>
<script>
import { mapState, mapActions } from "vuex";
import axios from "../../axios-auth";
import store from "../../store";

export default {
  name: "buyerFavoritesModal",
  components: {},
  data() {
    return {
      currentRoute: "",
    };
  },
  methods: {
    cancel() {
      this.$parent.buyerFavoritesModalShow = false;
    },
    showAgendaModal(favorite) {
      const data = {
        address: {
          street: favorite.address,
        },
        id: favorite.id,
      };

      this.$root.$emit("show-agenda-modal", { item: data, cid: "" });
    },
    showDetailModal(favorite) {
      axios.get(`/api/realtor/listings/${favorite.uid}/`)
        .then((res) => {
          this.$root.$emit("show-listing-detail-modal", res.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  props: {
    buyerFavoritesModalShow: Boolean,
    favoritesList: Array,
  },
  computed: {
    ...mapState(["idToken", "loading"]),
  },
  filters: {
    numberWithCommas(x) {
      x = parseFloat(x)
        .toFixed(2)
        .replace(/\.00$/, "");
      const parts = x.toString().split(".");
      parts[0] = parts[0].replace(",", "");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      return parts.join(".");
    },
  },
  mounted() {
    // this.currentRoute = this.$route.name;
  },
};
</script>
<style scoped>
.dashboard__buyer-favorites__body {
  display: flex;
  flex-direction: column;
  margin-left: 20px;
}
.name {
  font-size: 25px;
  color: #3c4d69;
  font-weight: 700;
  text-decoration: none solid rgb(60, 77, 105);
  margin-bottom: 7px;
}
.description {
  font-size: 20px;
  color: #3c4d69;
  text-decoration: none solid rgb(60, 77, 105);
  margin-bottom: 14px;
}
.price {
  border-radius: 50px;
  background-color: #f26a52;
  font-size: 15px;
  color: white;
  padding: 14px;
  margin-right: 20px;
}
.footer {
  display: flex;
  flex-direction: row;
}
.add-btn {
  margin: auto 0 auto auto;
  color: #808080;
}
hr {
  margin: 35px 200px;
}
.item:last-child hr {
  display: none;
}
</style>
