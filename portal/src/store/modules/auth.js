import authAPI from './../../api/auth-api';

const state = {
  token: localStorage.getItem('token') || null
};

const getters = {
  isAuthenticating: (state) => {
    return state.isAuthenticating;
  },
  isAuthenticated: (state) => {
    return !!state.token;
  }
};

const actions = {
  login({dispatch, commit, state}, credentials) {
    return new Promise((resolve, reject) => {
      authAPI.login(credentials, (res) => {
        if(res.user.user_type == 'Realtor') {
          // Change when the Realtor Portal merged to new UI codebase
          window.location.href = '/realtor/';
        } else {
          commit('loginSuccess', res);
          resolve({
            status: 'success',
            user: res.user
          });
        }
      }, (err) => {
        reject(err);
      });
    })
  },
  register({dispatch, commit, state}, credentials) {
    return new Promise((resolve, reject) => {
      authAPI.register(credentials, (res) => {
        commit('registerSuccess', res);
        resolve({status: 'success'});
      }, (err) => {
        reject(err);
      });
    })
  },
  logout({dispatch, commit, state}) {
    return new Promise((resolve, reject) => {
      let params = {
        key: state.token
      };

      authAPI.logout(params, (res) => {
        commit('logoutSuccess');
        resolve({status: 'success'});
      }, (err) => {
        reject(err);
      })
    })
  }
};

const mutations = {
  loginSuccess(state, result) {
    localStorage.setItem('token', result.key);
    localStorage.setItem('user', JSON.stringify(result.user));

    state.token = result.key;
  },
  registerSuccess(state, result) {
    localStorage.setItem('token', result.key);
    localStorage.setItem('user', JSON.stringify(result.user));

    state.token = result.key;
  },
  logoutSuccess(state) {
    localStorage.clear();

    state.token = null;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
