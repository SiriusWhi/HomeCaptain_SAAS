<template>
  <div>
    <gmap-map
        :center="center"
        :zoom="18"
        ref="gmap"
        v-bind:options="mapStyle"
        style="width:100%;  height: 600px;">
      <gmap-info-window :options="infoOptions" :position="infoPosition" :opened="infoOpened"
                        @closeclick="infoOpened=false" class="custom-gmap-info">
        <div class="text-center" style="font-size: 14px">
          <p v-if="infoContent.address" style="font-weight: 600; color: #808080;">
            {{infoContent.address.street}}
            <br/>
            {{infoContent.address.state + ' ' + infoContent.address.city}}
          </p>
          <p><span class="float-left mb-1 map-rooms"># of bedrooms: </span><span
              class="float-right mb-1 map-rooms-number">{{infoContent.bedrooms}}</span></p>
          <p><span class="float-left mb-2 map-rooms"># of bathrooms: </span><span
              class="float-right mb-2 map-rooms-number">{{infoContent.bathrooms}}</span></p>
          <p class="card-doc map-price-widget">$ {{infoContent.target_price_maximum | Commas}}</p>
        </div>
      </gmap-info-window>
      <gmap-marker v-for="(item, key) in coordinates" :key="key" :position="getPosition(item)" :clickable="true"
                   :icon="icon"
                   @click="toggleInfo(item, key)"/>
    </gmap-map>
  </div>
</template>

<script>
import $ from "jquery";
import axios from "../axios-auth";
import Commas from "@/filters/commas";

export default {
  name: "GoogleMap",
  filters: {
    Commas,
  },
  data() {
    return {
      mapStyle: { mapTypeId: "satellite" },
      icon: {
        url: "/img/icons/marker-icon.png",
        size: {
          width: 45, height: 45, f: "px", b: "px",
        },
        scaledSize: {
          width: 45, height: 45, f: "px", b: "px",
        },
        style: { background: "blue" },
      },
      startLocation: {
        lat: 10.3157,
        lng: 123.8854,
      },
      coordinates: [],
      infoPosition: null,
      infoContent: {},
      infoOpened: false,
      infoCurrentKey: null,
      infoOptions: {
        pixelOffset: {
          width: 0,
          height: -35,
        },
      },
      places: [],
      currentPlace: null,
      center: {
        lat: 39.77768,
        lng: -104.826,
      },
    };
  },

  mounted() {
    this.getAddresses();
  },

  methods: {
    getAddresses() {
      const self = this;
      const list = [];
      this.showLoading = true;
      const url = "/api/realtor/listings/?recommended=true&location=denver";

      axios
        .get(url)
        .then((res) => {
          this.addresses = res.data.results;

          $.each(this.addresses, (key, value) => {
            self.$refs.gmap.$mapPromise.then((res) => {
              const geocoder = new google.maps.Geocoder();
              const address = `${value.address.country} ${value.address.state} ${value.address.city} ${value.address.street}`;
              geocoder.geocode({ address }, (results, status) => {
                if (status === google.maps.GeocoderStatus.OK) {
                  const lat = results[0].geometry.location.lat();
                  const lng = results[0].geometry.location.lng();
                  self.coordinates.push({
                    lat,
                    lng,
                    info: value,
                  });
                }
              });
            });
          });
          this.showLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.showLoading = false;
        });
    },
    getPosition(marker) {
      return {
        lat: parseFloat(marker.lat),
        lng: parseFloat(marker.lng),
      };
    },
    toggleInfo(marker, key) {
      this.infoPosition = this.getPosition(marker);
      this.infoContent = marker.info;
      if (this.infoCurrentKey === key) {
        this.infoOpened = !this.infoOpened;
      } else {
        this.infoOpened = true;
        this.infoCurrentKey = key;
      }
    },
  },
};
</script>
