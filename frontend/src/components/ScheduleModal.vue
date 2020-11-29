<template>
  <b-modal v-model="scheduleModalShow" hide-header size="md" @hide="cancel()" class="scheduled-listing">
    <div class="row">
      <p class="col-md-12 modal-title">Agenda</p>
    </div>
    <div class="row">
      <div class="col-md-12 m-b-15 m-t-15">
        <p class="text-center custom-tabs">
          <span v-bind:class="{'active': agendaStatus == 'pending'}" @click="changeAgendaStatus('pending')">Pending</span>
          <span v-bind:class="{'active': agendaStatus == 'confirmed'}" @click="changeAgendaStatus('confirmed')">Confirmed</span>
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12 item-list">
        <div v-for="(schedule, k) in scheduleList" v-bind:key="k" class="item-container">
          <div class="row mb-2 align-items-center">
            <div class="col-md-6">
              <span class="date">{{schedule.proposed_start | date}}</span>
            </div>
            <div class="col-md-6">
              <a href="javascript:;" class="card-contacts-a text-uppercase mont float-right" @click="viewAgendaDetail(schedule)">view details</a>
            </div>
          </div>
          <div class="flex align-items-center">
            <span class="list-bullet lb-lo pull-left"></span>
            <div class="w-100">
              <div class="row mb-1">
                <div class="col-md-4">
                  <span class="time">{{schedule.proposed_start | time}}</span>
                </div>
                <div class="col-md-8">
                  <span class="name">{{schedule.name}}</span>
                </div>
              </div>
              <div class="row">
                <div class="col-md-4">
                  <span class="time">{{schedule.proposed_end | time}}</span>
                </div>
                <div class="col-md-8">
                  <span class="location">{{schedule.location}}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="item-seperator"></div>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="w-100 flex">
      <b-btn size="sm" class="float-left text-uppercase" variant="light" @click="cancel()">x Hide</b-btn>
    </div>
  </b-modal>
</template>
<script>
import { mapState, mapActions } from "vuex";
import moment from "moment";

export default {
  name: "scheduleModal",
  components: {},
  data() {
    return {
      currentRoute: "",
      agendaStatus: "pending",
    };
  },
  methods: {
    cancel() {
      this.$parent.scheduleModalShow = false;
    },
    changeAgendaStatus(status) {
      this.agendaStatus = status;
    },
    viewAgendaDetail(listItem) {
      this.$root.$emit("show-agenda-modal", { item: null, cid: listItem.uid });
    },
  },
  props: {
    scheduleModalShow: Boolean,
    scheduleList: Array,
  },
  computed: {
    ...mapState(["idToken", "loading"])
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
    },
    date(v) {
      var res = moment(v).local()
      return res.format("LL");
    },
    time(v) {
      var res = moment(v).local()
      return res.format("LT");
    }
  },
  mounted() {
    //this.currentRoute = this.$route.name;
  }
};
</script>
<style scoped>
  .modal-title {
    color: #808080;
    font-size: 20px;
  }

  .m-b-15 {
    margin-bottom: 15px;
  }

  .m-t-15 {
    margin-top: 15px;
  }

  .custom-tabs {
    color: #808080;
  }

  .custom-tabs span {
    padding: 15px 5px;
    margin: 0 10px;
    cursor: pointer;
  }

  .custom-tabs span.active {
    color: #2c71c7;
    border-bottom: 3px solid #2c71c7;
  }

  .item-list {
    margin-top: 25px;
  }

.list-bullet {
  height: 70px;
  border-top-right-radius: 50px;
  border-bottom-right-radius: 50px;
  background-size: cover;
}

.date {
  font-size: 20px;
  color: #3c4d69;
  text-decoration: none solid rgb(60, 77, 105);
}
.time {
  font-size: 17px;
  color: #9e9e9e;
  text-decoration: none solid rgb(158, 158, 158);
}
.name {
  font-size: 17px;
  color: #9e9e9e;
  font-weight: 700;
  text-decoration: none solid rgb(158, 158, 158);
}
.location {
  font-size: 17px;
  color: #9e9e9e;
  text-decoration: none solid rgb(158, 158, 158);
}
  .item-seperator {
    height: 2px;
    width: 200px;
    margin: 10px auto;
    background: #a4abbf;
  }

  .item-container:last-child .item-seperator {
    display: none;
  }
</style>
