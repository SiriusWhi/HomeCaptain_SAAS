import axios from 'axios';

const BASE_URL = 'https://staging.homecaptain.com/api/auth';

export default {
  login (params, cb, errCb) {
    axios({
      method: 'post',
      url: BASE_URL + '/login/',
      data: params
    }).then(function(response) {
      cb(response.data);
    }).catch(function(error) {
      errCb(error);
    })
  },
  register(params, cb, errCb) {
    axios({
      method: 'post',
      url: BASE_URL + '/registration/',
      data: params
    }).then(function(response) {
      cb(response.data);
    }).catch(function(error) {
      errCb(error);
    })
  },
  logout(params, cb, errCb) {
    axios({
      method: 'post',
      url: BASE_URL + '/logout/',
      data: params
    }).then(function(response) {
      cb(response.data);
    }).catch(function(error) {
      errCb(error);
    })
  }
}
