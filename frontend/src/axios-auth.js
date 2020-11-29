import axios from "axios";

const instance = axios.create({
  baseURL: "https://staging.homecaptain.com",
});

//https://staging.homecaptain.com",

//instance.defaults.headers.common['SOMETHING'] = 'something'

export default instance;
