<template>
  <div class="main-container">
    <div class="home-manage">
      <div class="people-container">
        <div class="d-flex align-items-center">
          <span class="container-title">Buyers</span>
          <span class="manage-people-count">29</span>

          <div class="custom-filter-div" @click="showFilter = !showFilter">
            <div class="custom-filter-container" v-bind:class="{'open': showFilter}">
              <font-awesome-icon icon="plus-circle"/>
              <label>{{currentFilter || 'Add Filter'}}</label>
              <div class="filter-container">
                <div class="filter-group">
                  <span class="filter-item filter-title">Status</span>
                  <span class="filter-item" @click="setFilter('Agent Signed Documents')">Agent Signed Documents</span>
                  <span class="filter-item" @click="setFilter('Still Searching for Home')">Still Searching for Home</span>
                  <span class="filter-item" @click="setFilter('Offer Submitted')">Offer Submitted</span>
                  <span class="filter-item" @click="setFilter('Ratified Contract')">Ratified Contracts</span>
                  <span class="filter-item" @click="setFilter('Closing Confirmed')">Closing Confirmed</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <span class="manage-table-title">Favorites</span>

        <div class="table-container mt-1 mb-4">
          <table class="table manage-table">
            <tr v-for="i in 10" v-bind:key="i">
              <td width="50px">
                <b-form-checkbox value="accepted" unchecked-value="not_accepted" />
              </td>
              <td width="90px">
                <img class="user-avatar" src="./../../../assets/images/user-avatar_2.jpg" />
              </td>
              <td width="180px">
                <span class="people-name">Zoey Fletcher</span>
              </td>
              <td width="280px">
                <div class="d-flex align-items-center people-status">
                  <span class="status-bullet"></span>
                  <span class="status-text">Agent Document Signed</span>
                  <font-awesome-icon icon="pen" />
                </div>
              </td>
              <td>
              <span class="favorite-count">
                7 <font-awesome-icon icon="caret-up" />
              </span>
              </td>
              <td width="320px">
                <div class="d-flex justify-content-end">
                <span class="action-button">
                  <font-awesome-icon icon="pen" /> Edit
                </span>
                  <span class="action-button">
                  <font-awesome-icon icon="upload" /> Export
                </span>
                  <span class="action-button">
                  <font-awesome-icon icon="paper-plane" /> Contact
                </span>
                </div>
              </td>
            </tr>
          </table>
        </div>

        <div class="d-flex justify-content-between">
          <b-pagination size="sm" :total-rows="100" v-model="currentPage" :per-page="10">
          </b-pagination>

          <div class="table-action">
            <span class="selected-items">2 Customers selected</span>
            <span class="action-button">
            <font-awesome-icon icon="upload" /> Export
          </span>
            <span class="action-button">
            <font-awesome-icon icon="paper-plane" /> Contact
          </span>
          </div>
        </div>
      </div>

      <div class="stats-container">
        <div class="d-flex align-items-center">
          <span class="container-title">Stats</span>
        </div>
        <div class="d-flex flex-wrap">
          <div class="state-item">
            <span class="state-count">12</span>
            <span class="state-text">Archived</span>
          </div>
          <div class="state-item">
            <span class="state-count">10</span>
            <span class="state-text">No Longer Available</span>
          </div>
          <div class="state-item">
            <span class="state-count">5</span>
            <span class="state-text">No Longer Responding</span>
          </div>
          <div class="state-item">
            <span class="state-count">5</span>
            <span class="state-text">Still Searching For Home</span>
          </div>
          <div class="state-item">
            <span class="state-count">45</span>
            <span class="state-text">Offer Submitted</span>
          </div>
          <div class="state-item">
            <span class="state-count">23</span>
            <span class="state-text">Ratified Contract</span>
          </div>
          <div class="state-item">
            <span class="state-count">45</span>
            <span class="state-text">Closing Confirmed</span>
          </div>
          <div class="state-item">
            <span class="state-count">23</span>
            <span class="state-text">Searching Reset</span>
          </div>
          <div class="state-item">
            <span class="state-count">12</span>
            <span class="state-text">Search On Hold</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "HomeBuying",
    data() {
      return {
        showFilter: false,
        currentFilter: '',
        currentPage: 1
      };
    },
    methods: {
      setFilter: function(filter) {
        this.currentFilter = filter;

        setTimeout(function() {
          this.showFilter = false;
        });
      }
    }
  }
</script>
