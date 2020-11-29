<template>
  <b-modal v-model="modalShow" hide-header hide-footer size="lg" @hide="hideAgendaModal()">
    <div class="row">
      <div class="col-md-6">
        <div class="col-md-12 calendar-wrapper">
          <p class="agenda-item-label">TODAY IS:</p>
          <p class="today-date">{{todayString}}</p>
          <date-pick v-model="todayDate" :hasInputElement="false"></date-pick>
        </div>
        <div class="col-md-12 agenda-list-wrapper">
          <p>Agenda</p>
          <div class="agenda-list">
            <div class="agenda-list-item" v-for="agenda in agendas" @click="changeAgenda(agenda)">
              <span class="list-bullet lb-bs"></span>
              <div class="list-detail">
                <div class="agenda-date">
                  <span>{{agenda.proposed_date}}</span>
                </div>
                <div class="agenda-time">
                  <span>{{agenda.start_time | advancedTime}}</span>
                  <span>{{agenda.end_time | advancedTime}}</span>
                </div>
                <div class="agenda-detail">
                  <span>{{agenda.name}}</span>
                  <span>{{agenda.location}}</span>
                </div>
              </div>
              <div class="clearfix"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="col-md-12" v-show="!editAgenda">
          <div class="agenda-nothing">
            <i class="far fa-calendar"></i>
            <p class="agenda-status">Nothing Here</p>
            <p>Select a date to add the schedule type or edit an existing one from your Agenda</p>
          </div>
        </div>
        <div class="col-md-12 edit-agenda-wrapper" v-show="editAgenda">
          <div class="edit-agenda-item">
            <p class="agenda-item-label">SCHEDULE TYPE</p>
            <div class="agenda-type">
              <b-dropdown>
                <template slot="button-content">
                  {{agendaData.name}}
                </template>
                <b-dropdown-item v-for="type in agendaTypes" @click="setAgendaType(type)">{{type}}</b-dropdown-item>
              </b-dropdown>
              <i class="fas fa-circle type-bullet"></i>
              <i class="fas fa-angle-down type-dropdown"></i>
            </div>
          </div>
          <div class="edit-agenda-item">
            <p class="agenda-item-label">HOURS</p>
            <b-form-input class="agenda-timepicker" :type="'time'"
                          v-model="agendaData.start_time"></b-form-input>
            <span> - </span>
            <b-form-input class="agenda-timepicker" :type="'time'"
                          v-model="agendaData.end_time"></b-form-input>
          </div>
          <div class="edit-agenda-item">
            <p class="agenda-item-label">NOTE</p>
            <b-form-textarea class="agenda-textarea" placeholder="Lorem ip sum dollar sit met"
                             v-model="agendaData.note" :rows="4" :size="'1000'"
                             :no-resize="true"></b-form-textarea>
            <p class="agenda-note-length">{{note.length}}/1000</p>
          </div>
          <p class="agenda-note-info">
            <i class="fas fa-info-circle"></i> Your note will be sent out to all attendees
          </p>
          <div class="edit-agenda-item">
            <p class="agenda-item-label">ATTENDEES</p>
            <b-form-checkbox v-model="agendaData.is_buyer_loan_officer_required" value="1" unchecked-value="0">
              Loan Officer
            </b-form-checkbox>
            <b-form-checkbox v-model="agendaData.is_buyer_concierge_required" value="1" unchecked-value="0">
              Concierge
            </b-form-checkbox>
            <b-form-checkbox v-model="agendaData.is_buyer_realtor_required" value="1" unchecked-value="0" disabled>
              Buyer Realtor
            </b-form-checkbox>
            <b-form-checkbox v-model="agendaData.is_seller_realtor_required" value="1" unchecked-value="0">
              Seller Realtor
            </b-form-checkbox>
            <b-form-checkbox v-model="agendaData.is_buyer_required" value="1" unchecked-value="0">
              Owner
            </b-form-checkbox>

            <div class="attendee-list">
              <div class="attendee-item" v-for="(attendee, index) in attendees">
                <i class="fas fa-circle attendee-bullet"></i>
                <span class="attendee-name">{{attendee}}</span>
                <span class="attendee-action" @click="removeAttendee(index)">
                  <i class="far fa-trash-alt"></i>
                </span>
              </div>
            </div>

            <input class="agenda-input" type="text" placeholder="Press enter to add new"
                   v-model="newAttendee" @keyup.enter="addAttendee()">

            <div class="buyer-list">
              <div class="buyer-item" v-for="(buyer, index) in agendaData.buyers">
                <i class="fas fa-circle buyer-bullet"></i>
                <span class="buyer-name">{{buyer}}</span>
                <span class="buyer-action" @click="removeBuyer(index)">
                  <i class="far fa-trash-alt"></i>
                </span>
              </div>
            </div>

            <vue-bootstrap-typeahead class="custom-typeahead" v-model="newBuyer" :data="buyerList"
                                     @hit="addBuyer()" placeholder="Type an buyer..."
                                     :disabled="agendaData.buyers.length == 1" />
          </div>
          <div class="edit-agenda-item">
            <p class="agenda-item-label">LOCATION</p>
            <vue-bootstrap-typeahead class="custom-typeahead" v-model="location" :data="locationList"
                                     @hit="selectLocation()" placeholder="Location Goes Here" ref="locationTypeahead"/>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="col-md-6 float-right">
          <b-button class="btn-save" :size="'sm'" :variant="'primary'" :disabled="!editAgenda" @click="saveAgenda()">
            <span v-if="agendaData.uid">Update</span>
            <span v-else>Add</span> Showing
          </b-button>
          <b-button class="btn-cancel float-right" :size="'sm'" @click="hideAgendaModal()">
            <i class="fas fa-times"></i> CANCEL
          </b-button>
        </div>
      </div>
    </div>
  </b-modal>
</template>

<script>
import { mapState, mapActions } from "vuex";
import DatePick from "vue-date-pick";
import _ from "lodash";
import jQuery from "jquery";
import axios from "../axios-auth";
import store from "../store";


import "vue-date-pick/dist/vueDatePick.css";

export default {
  name: "agendaModal",
  components: {
    DatePick,
  },
  data() {
    return {
      weekDays: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      todayString: "",
      todayDate: "",
      note: "",
      editAgenda: false,
      createAgenda: false,
      agendas: [],
      agendaTypes: [],
      buyerList: [],
      locationList: [],
      propertyList: [],
      agendaData: {
        name: "--- Select Schedule Type ---",
        is_buyer_loan_officer_required: 0,
        is_buyer_concierge_required: 0,
        is_buyer_required: 0,
        is_buyer_realtor_required: 1,
        is_seller_required: 0,
        is_seller_realtor_required: 0,
        is_service_provider_required: 0,
        buyers: [],
      },
      attendees: [],
      newAttendee: "",
      newBuyer: "",
      location: "",
    };
  },
  methods: {
    init() {
      const self = this;

      axios
        .get("/api/realtor/agenda/")
        .then((res) => {
          self.agendas = [];
          _.each(res.data, (result) => {
            const agenda = result;
            const agendaStart = new Date(result.proposed_start);
            const agendaEnd = new Date(result.proposed_end);

            agenda.proposed_date = `${agendaStart.getFullYear()}-`;
            if (agendaStart.getMonth() + +1 < 10) agenda.proposed_date += `0${agendaStart.getMonth() + +1}-`;
            else agenda.proposed_date += `${agendaStart.getMonth() + +1}-`;

            if (agendaStart.getDate() < 10) agenda.proposed_date += `0${agendaStart.getDate()}`;
            else agenda.proposed_date += `${agendaStart.getDate()}`;

            if (agendaStart.getHours().toString().length === 1) agenda.start_time = `0${agendaStart.getHours()}:`;
            else agenda.start_time = `${agendaStart.getHours()}:`;

            if (agendaStart.getMinutes().toString().length === 1) agenda.start_time += `0${agendaStart.getMinutes()}`;
            else agenda.start_time += `${agendaStart.getMinutes()}`;

            if (agendaEnd.getHours().toString().length === 1) agenda.end_time = `0${agendaEnd.getHours()}:`;
            else agenda.end_time = `${agendaEnd.getHours()}:`;

            if (agendaEnd.getMinutes().toString().length === 1) agenda.end_time += `0${agendaEnd.getMinutes()}`;
            else agenda.end_time += `${agendaEnd.getMinutes()}`;

            agenda.attendees = _.concat(agenda.additional_attendees, agenda.emails);
            agenda.buyers = [];
            agenda.buyers.push(agenda.buyer);

            self.agendas.push(agenda);
          });

          axios
            .get("/api/realtor/agenda/extras/")
            .then((res) => {
              this.agendaTypes = res.data.event_names;
              this.buyerList = res.data.buyers;

              _.each(res.data.addresss, (address) => {
                self.locationList.push(address[0]);
                self.propertyList.push(address[1]);
              });

              for (let i = 0; i < self.agendas.length; i++) {
                if (self.agendas[i].uid == this.uid) self.changeAgenda(self.agendas[i]);
              }
            })
            .catch((error) => {
              console.log(error);
            });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    changeAgenda(agenda) {
      this.editAgenda = true;
      this.agendaData = _.cloneDeep(agenda);
      this.agendaData.is_buyer_loan_officer_required = String(Number(this.agendaData.is_buyer_loan_officer_required));
      this.agendaData.is_buyer_concierge_required = String(Number(this.agendaData.is_buyer_concierge_required));
      this.agendaData.is_buyer_realtor_required = String(Number(this.agendaData.is_buyer_realtor_required));
      this.agendaData.is_seller_required = String(Number(this.agendaData.is_seller_required));
      this.agendaData.is_seller_realtor_required = String(Number(this.agendaData.is_seller_realtor_required));
      this.agendaData.is_service_provider_required = String(Number(this.agendaData.is_service_provider_required));
      this.attendees = _.cloneDeep(this.agendaData.attendees);

      this.$refs.locationTypeahead.inputValue = this.agendaData.location;
    },
    setAgendaType(type) {
      this.agendaData.name = type;
    },
    addAttendee() {
      const attendee = this.newAttendee.trim();
      if (attendee && this.attendees.indexOf(attendee) === -1) {
        this.attendees.push(attendee);
        this.newAttendee = "";
      }
    },
    removeAttendee(index) {
      this.attendees.splice(index, 1);
    },
    addBuyer() {
      if (this.agendaData.buyers.length < 1) {
        this.agendaData.buyers.push(this.newBuyer);

        const index = this.buyerList.indexOf(this.newBuyer);
        this.buyerList.splice(index, 1);
        this.agendaData.is_buyer_required = true;
      }
    },
    removeBuyer(index) {
      this.buyerList.push(this.agendaData.buyers[index]);
      this.agendaData.buyers.splice(index, 1);
      this.agendaData.is_buyer_required = false;
    },
    selectLocation() {
      const index = this.locationList.indexOf(this.location);

      this.agendaData.location = this.location;
      this.agendaData.property = this.propertyList[index];
    },
    saveAgenda() {
      const self = this;

      this.agendaData.is_buyer_loan_officer_required = Boolean(Number(this.agendaData.is_buyer_loan_officer_required));
      this.agendaData.is_buyer_concierge_required = Boolean(Number(this.agendaData.is_buyer_concierge_required));
      this.agendaData.is_buyer_realtor_required = Boolean(Number(this.agendaData.is_buyer_realtor_required));
      this.agendaData.is_seller_required = Boolean(Number(this.agendaData.is_seller_required));
      this.agendaData.is_seller_realtor_required = Boolean(Number(this.agendaData.is_seller_realtor_required));
      this.agendaData.is_service_provider_required = Boolean(Number(this.agendaData.is_service_provider_required));
      if (this.agendaData.buyers.length) this.agendaData.buyer = `@${this.agendaData.buyers[0]}`;
      this.agendaData.additional_attendees = [];

      const mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

      for (let i = 0; i < this.attendees.length; i++) {
        if (mailformat.test(this.attendees[i])) this.agendaData.additional_attendees.push(this.attendees[i]);
        else this.agendaData.additional_attendees.push(`@${this.attendees[i]}`);
      }

      if (this.agendaData.uid) {
        this.agendaData.proposed_start = new Date(`${this.agendaData.proposed_date}T${this.agendaData.start_time}`);
        this.agendaData.proposed_end = new Date(`${this.agendaData.proposed_date}T${this.agendaData.end_time}`);

        axios
          .put(`/api/realtor/agenda/${this.agendaData.uid}/`, this.agendaData)
          .then((res) => {
            self.init();
            self.$toastr("success", "Agenda has been updated!", "Success!");
            self.hideAgendaModal();
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        this.agendaData.proposed_start = new Date(`${this.todayDate}T${this.agendaData.start_time}`);
        this.agendaData.proposed_end = new Date(`${this.todayDate}T${this.agendaData.end_time}`);

        axios
          .post("/api/realtor/agenda/", this.agendaData)
          .then((res) => {
            self.init();
            self.$toastr("success", "New Agenda has been scheduled.", "Success!");
            self.hideAgendaModal();
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    hideAgendaModal() {
      this.todayDate = "";
      this.editAgenda = false;
      this.$parent.showAgendaModal = false;
    },
  },
  props: {
    modalShow: Boolean,
    item: Object,
    uid: String,
  },
  computed: {
    ...mapState(["idToken", "loading"]),
  },
  mounted() {
    const today = new Date();
    this.todayString = `${this.weekDays[today.getDay()]}, ${this.months[today.getMonth()]} ${today.getDate()}`;
  },
  filters: {
    advancedTime(value) {
      const tempArray = value.split(":");
      let half = "";

      if (Number(tempArray[0]) > 11) {
        tempArray[0] = Number(tempArray[0]) - 12;
        half = "PM";
      } else half = "AM";

      if (tempArray[0].toString().length === 1) tempArray[0] = `0${tempArray[0].toString()}`;
      if (tempArray[1].toString().length === 1) tempArray[1] = `0${tempArray[1].toString()}`;

      return `${tempArray[0]}:${tempArray[1]} ${half}`;
    },
  },
  watch: {
    todayDate(newVal, oldVal) {
      if (newVal) {
        this.editAgenda = true;
        this.agendaData = {
          name: "--- Select Schedule Type ---",
          is_buyer_loan_officer_required: 0,
          is_buyer_concierge_required: 0,
          is_buyer_required: 0,
          is_buyer_realtor_required: 1,
          is_seller_required: 0,
          is_seller_realtor_required: 0,
          is_service_provider_required: 0,
          buyers: [],
        };

        if (this.item) {
          this.$refs.locationTypeahead.inputValue = this.item.address.street;
          this.agendaData.location = this.item.address.street;
          this.agendaData.property = this.item.id;
        }
      }
    },
    modalShow(newVal, oldVal) {
      if (newVal) {
        this.init();
      }
    },
  },
};
</script>

<style scoped>

</style>
