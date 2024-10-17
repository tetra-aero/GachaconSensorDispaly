import { createStore } from 'vuex'
import axios from 'axios';

const store = createStore({
  state() {
    return {
      dataFromServer: null,
      errorMessege:null,
      retryCount:0,
    };
  },
  mutations: {
    setData(state, payload) {
      state.dataFromServer = payload;
      state.retryCount = 0; // 成功したらリトライカウントをリセット
    },
    setError(state, payload) {
      state.errorMessage = payload;
    },
    incrementRetryCount(state) {
      state.retryCount += 1;
    },
  },
  actions: {
    async fetchData({ commit, state }) {
      try {
        const response = await axios.get('/json');
        commit('setData', response.data);
        commit('setError', null);
      } catch (error) {
        commit('setError', '通信エラーが発生しました。');
        console.error('Error fetching data:', error);
        // リトライ: 最大3回まで再試行
        if (state.retryCount < 3) {
          commit('incrementRetryCount');
          setTimeout(() => {
            this.dispatch('fetchData');  // 1秒後に再試行
          }, 1000);
        } else {
          commit('setError', '通信エラーが発生しました。再試行に失敗しました。');
        }
      }
    }
  },
  getters: {
    dataFromServer: (state) => state.dataFromServer,
    errorMessage: (state) => state.errorMessage,
  },
});

export default store;