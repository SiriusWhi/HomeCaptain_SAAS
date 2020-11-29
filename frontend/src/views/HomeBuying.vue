<template>
  <div class="dashboard buying-page">
    <div class="loading-wrapper" v-show="showLoading">
      <img src="../../public/img/loading.svg" alt="">
    </div>
    <Sidebar/>
    <div class="page-content" data-simplebar data-simplebar-auto-hide="false">
      <HcHeader/>
      <input type="text"
             class="hiddenSearch"
             placeholder="Search buyers, sellers, or lenders"
             v-on:input="searchUser" v-model="searchString">
      <StatusModal :modalShow="modalShow" :userInformation="selectedUser" :milestones="filters"/>
      <ContactModal :contactModalShow="contactModalShow" :userInformation="selectedUser" :email="{}" :role="userRole"/>
      <EditModal :editModalShow="editModalShow" :userInformation="selectedUser" :role="userRole"/>
      <section class="cards-row row users-list">
        <article class="col-md-8">
          <div class="card">
            <div class="row">
              <div class="col-md-12">
                <div class="flex">
                  <p class="flex">
                    <span class="buyers-title">Buyers</span>
                  </p>
                  <span class="fa-stack buyers-count">
                    <i class="fa fa-circle fa-stack-2x"></i>
                    <strong class="fa-stack-1x text-white">{{ count }}</strong>
                  </span>
                  <div class="position-relative styled-select-wrap sqft-wrap">
                    <div
                      class="hc-select buyers-filter ml-4 styled-select sqft-styled-select pointer"
                      @click="showFilterOptions = !showFilterOptions"
                      :class="{dropSelect: showFilterOptions}">
                      <span>
                        <i class="styled-select-plus fas fa-plus"></i>
                        <span class="styled-select-label">
                          <b v-show="milestone === ''">Add Filters</b>
                          <b v-show="milestone !== ''">{{milestone.substr(0,15)}}<span v-if="milestone.length > 15" style="display: inline-flex">...</span></b>
                        </span>
                      </span>
                      <p class="styled-select-options sqft-options">
                        <span><b>Status</b></span>
                        <span
                          v-for="filter in filters"
                          @click="filterUser(filter.milestones)">{{ filter.milestones_display }}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="buyer-row">
              <p class="text-center text-uppercase table-title">Favorites</p>
              <div class="row">
                <div class="col-md-12 table-container" data-simplebar data-simplebar-auto-hide="false">
                  <table class="col-md-12">
                    <tr v-for="(buyer, key) in buyers">
                      <td width="40px" style="padding: 0 10px;">
                        <label class="custom-checkbox">
                          <input type="checkbox" v-on:click="getChecked(buyer.user.uid, $event); getExportArray(buyer.uid, $event)">
                          <span class="checkmark"></span>
                        </label>
                      </td>
                      <td width="75px">
                        <p :data-letters="buyer.user.first_name[0]" :class="'bg_'+key" class="buyer-avatar ml-6"></p>
                      </td>
                      <td width="160px">
                        <span class="card-name user-name">{{ buyer.user.first_name }} {{ buyer.user.last_name }}</span>
                      </td>
                      <td width="255px">
                        <p class="card-doc flex mt-3" @click="showStatusModal(buyer.uid)">
                          <span class="pulse-outside">
                            <span class="pulse"></span>
                          </span>
                          <span class="milestones-text">{{ buyer.milestones }}</span>
                          <i class="fas fa-pen doc-pen pointer"></i>
                        </p>
                      </td>
                      <td>
                        <span class="faves-qty mt-3">
                          {{ buyer.customer_favorite_count }} <img src="../../public/img/arrow-up.svg" class="number-up pointer" alt>
                        </span>
                      </td>
                      <td width="320px">
                        <span class="card-contacts-a text-uppercase mont pointer" @click="showEditModal(buyer.uid)">
                          <i class="fa fa-pen"></i> Edit
                        </span>
                            <span class="card-contacts-a text-uppercase mont pointer" @click="exportData(buyer.uid)">
                          <img src="../../public/img/export-icon.svg" class="buyer-icons pointer" alt>Export
                        </span>
                            <span class="card-contacts-a text-uppercase mont pointer" @click="showContactModal(buyer.uid)">
                          <img src="../../public/img/send-icon.svg" class="buyer-icons pointer" alt>Contact
                        </span>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>
            <div class="row flex">
              <div class="col-md-6 mt-5">
                <div v-if="count>10">
                  <b-pagination class="text-left"
                                size="md"
                                :total-rows="count"
                                v-model="currentPage"
                                :per-page="10"
                                @input="getBuyers()"
                  ></b-pagination>
                </div>
              </div>
              <div class="col-md-6 mt-5">
                <div class="float-right">
                  <span class="selected-count mr-4"
                        v-if="checkedArray.length > 0"><span>{{ checkedArray.length }}</span> Customers selected</span>
                  <span class="mr-4">
                    <span class="card-contacts-a text-uppercase mont pointer" @click="showContactModal()">
                      <img src="../../public/img/send-icon.svg" class="buyer-icons pointer" alt>Contact</span>
                  </span>
                  <span>
                    <span class="card-contacts-a text-uppercase mont pointer" @click="exportData()">
                      <img src="../../public/img/export-icon.svg" class="buyer-icons pointer" alt>Export</span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </article>
        <article class="col-md-4 p-3">
          <div class="row">
            <div class="flex col-md-12">
              <span class="buyers-title">Stats</span>
            </div>
            <div class="col-md-6" v-for="stats_item in filters">
              <span class="stats-count"> {{ stats_item.milestones__count }}</span>
              <p class="stats-text">{{ stats_item.milestones_display }}</p>
            </div>
          </div>

        </article>
      </section>
    </div>
  </div>
</template>

<script>
  import axios from "../axios-auth";
  import HcHeader from "@/components/HcHeader.vue";
  import Sidebar from "@/components/Sidebar.vue"
  import StatusModal from "@/components/StatusModal.vue"
  import ContactModal from "@/components/ContactModal.vue"
  import EditModal from "@/components/EditModal.vue"

  import $ from "jquery";

  import {mapState, mapActions} from "vuex";

  export default {
    name: "homeBuying",
    components: {
      HcHeader,
      Sidebar,
      StatusModal,
      ContactModal,
      EditModal,
    },
    data() {
      return {
        showLoading: false,
        currentPage: 1,
        buyers: [],
        filters: [],
        count: 0,
        modalShow: false,
        contactModalShow: false,
        editModalShow: false,
        selectedUser: {},
        checkedArray: [],
        exportArray: [],
        selectedUsers: [],
        searchString: '',
        milestone: '',
        userRole: '',
        showFilterOptions: false,
      };
    },
    methods: {
      ...mapActions(["logout"]),
      ...mapActions({
        handleLogout: "logout"
      }),
      getBuyers() {
        this.showLoading = true;
        let offSet;
        this.currentPage === 1 ? (offSet = 0) : (offSet = this.currentPage * 10 - 10);
        let url = `/api/realtor/dashboard/home-buying/?limit=10&offset=${offSet}`;
        if (this.searchString !== "") {
          url += `&search=${this.searchString}`;
        }
        if (this.milestone !== "") {
          url += `&milestones=${this.milestone}`;
        }
        axios
          .get(url)
          .then((res) => {
            this.count = res.data.count;
            this.buyers = res.data.results;
            this.showLoading = false;
          }).catch((error) => {
          this.showLoading = false;
          console.log(error)
        });
      },
      showStatusModal(uid) {
        this.modalShow = true;
        this.contactModalShow = false;
        this.editModalShow = false;
        this.selectedUser = (this.buyers).find(obj => {
          return obj.uid === uid
        });
      },
      showContactModal(uid) {
        if (this.checkedArray.length > 0 || uid) {
          this.contactModalShow = true;
          this.modalShow = false;
          this.editModalShow = false;
          this.userRole = '';
          if (uid) {
            this.selectedUser = (this.buyers).find(obj => {
              return obj.uid === uid
            });
          } else {
            let self = this;
            $.each(this.checkedArray, function (index, value) {
              self.selectedUsers.push((self.buyers).find(obj => {
                return obj.user.uid === value
              }));
            });
          }
        } else {
          this.showLoading = false;
          this.$toastr("warning", "Please choose buyers to contact", "Warning!");
        }
      },
      showEditModal(uid) {
        this.editModalShow = true;
        this.contactModalShow = false;
        this.modalShow = false;
        this.selectedUser = (this.buyers).find(obj => {
          return obj.uid === uid
        });
      },
      notImplementedYet() {
        this.$toastr("info", "Not implemented because can't find the popup for it'", "Info!");
      },
      getChecked(value, event) {
        if (event.target.checked) {
          this.checkedArray.push(value)
        } else {
          this.checkedArray.splice(this.checkedArray.indexOf(value), 1);
        }
      },
      getExportArray(value, event) {
        if (event.target.checked) {
          this.exportArray.push(value)
        } else {
          this.exportArray.splice(this.exportArray.indexOf(value), 1);
        }
      },
      randomColor() {
        const r = () => Math.floor(256 * Math.random());
        return `rgb(${r()}, ${r()}, ${r()})`;
      },
      exportData(uid) {
        this.showLoading = true;
        let data = [];
        uid ? data = [uid] : data = this.exportArray;
        if (this.exportArray.length > 0 || uid) {
          axios({
            url: `https://staging.homecaptain.com/api/realtor/dashboard/home-buying/export-customers/?uids=${data.join()}`,
            method: 'GET',
            responseType: 'blob',
          }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'Realtor-Buyers-Export.xlsx');
            document.body.appendChild(link);
            link.click();
          });
          this.showLoading = false;
        } else {
          this.showLoading = false;
          this.$toastr("warning", "Please choose buyers to export", "Warning!");
        }
      },
      getStats() {
        axios
          .get("/api/realtor/dashboard/home-buying/stats/")
          .then((res) => {
            this.filters = res.data.filters;
          }).catch((error) => {
          console.log(error)
        });
      },

      searchUser: _.debounce(function () {
        this.getBuyers();
      }, 1000),

      filterUser(milestone) {
        this.milestone = milestone;
        this.getBuyers();
      }
    },

    computed: {
      ...mapState(["idToken", "loading"])
    },

    watch: {
      loading: function (load) {
        if (load === true) {
          this.showLoading = true;
        } else {
          this.showLoading = false;
        }
      }
    },

    mounted() {
      this.getBuyers();
      this.getStats();
    }
  };
</script>

<style>
  .table-container {
    height: 500px;
  }

  .buyer-avatar {
    margin-left: 10px;
  }

  .card-contacts-a {
    margin: 0 10px;
  }
</style>
