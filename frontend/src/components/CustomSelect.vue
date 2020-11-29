<template>
   <div :class="{ __disabled: disabled }" class="select">
    <div @click="toggle" class="select_label">
      <span class="count">{{ getCount(value) }}</span> {{ getLabel(value) }}
    </div>
    <div v-if="opened" class="select_options">
      <div v-for="o in options" v-bind:key="getVal(o)" :value="getVal(o)" @click="change(o)" :class="{select_options__active: getVal(o) == getVal(value)}" class="select_option">
        <span class="count">{{ getCount(o) }}</span> {{ getLabel(o) }}
      </div>
    </div>
    <div v-if="opened" @click="toggle" class="select_overlay"></div>
  </div>
</template>

<script>
import axios from "../axios-auth";

export default {
  name: "customSelect",
  data() {
    return {
      opened: false,
      // value: this.options? this.options[0]: "",
    };
  },
  props: {
    options: Array,
    value: {
      required: true
    },
    valueKey: String,
    labelKey: String,
    countKey: String,
    onChange: Function,
    disabled: Boolean,
    noStatusLabel: String,
  },
  methods: {
    getVal (opt) {
      if (opt === "") return opt;
      return !this.valueKey ? opt : opt[this.valueKey]
    },
    getLabel (opt) {
      if (opt === "") return this.noStatusLabel;
      return !this.labelKey ? opt : (opt[this.labelKey] === "" ? this.noStatusLabel : opt[this.labelKey])
    },
    getCount (opt) {
      return !this.countKey ? opt : (opt[this.countKey] != null ? opt[this.countKey] : "")
    },
    change (opt) {
      this.$emit('input', opt)
      this.opened = false

      if (this.onChange !== undefined) {
        this.onChange(this.value)
      }
    },
    toggle () {
      if ( this.disabled ) {
        return
      }
      this.opened = !this.opened
    }
  },
}
</script>
<style scoped>
.select {
  font-size: 15px;
  display: flex;
  position: relative;
  justify-content: center;
}
.select * {
  box-sizing: border-box;
}
.count {
  display: inline-flex;
  justify-content: center;
  margin-right: 10px;
  width: 22px;
  height: 22px;
  background-color: #9e9e9e;
  line-height: 22px;
  font-size: 14px;
  color: #ffffff;
  border-radius: 50%;
  text-align: center;
}
.select .select_label {
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.2);
  background-size: cover;
  box-shadow: 5px 15px 30px rgba(164,171,191,0.2);
  font-size: 20px;
  color: #808080;

  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  transition: color ease-in-out 0.05s;
  white-space: nowrap;
  padding: 10px;
}

.select .select_label .count {
  background-color: #4a6491;
  color: #ffffff;
}

.select .select_label:hover {
  /* color: #929292; */
}

.select .select_options {
  position: absolute;
  background-color: white;
  box-shadow: 5px 15px 30px rgba(164,171,191,0.2);
  border-radius: 10px;
  z-index: 11001;
  top: 28px;
}
.select .select_option {
  cursor: default;
  color: #808080;
  padding: 7px 13px;
  white-space: nowrap;
  text-align: left;
}
.select .select_options__active {
  /* color: red; */
  background-color: #f0f6ff;
}

.select_options__active .count {
  background-color: #2c71c7;
}

.select .select_option:first-child {
  border-radius: 2px 2px 0 0;
}
.select .select_option:last-child {
  border-radius: 0 0 2px 2px;
}
.select .select_option:hover {
  background: #f0f6ff;
}
.select .select_overlay {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  z-index: 1000;
}
.select .select__disabled {
  opacity: 0.5;
}
.select .select__disabled .select_label:hover{
  color: #4C4C4C;
  cursor: default;
}
</style>
