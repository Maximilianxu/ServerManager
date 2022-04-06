import { settings } from "@/settings";
import {TOGGLE_SIDE_BAR} from "@/store/actions/user";

const state = {
  appName: settings.APP_NAME,
  sidebarCollapse: false,
};

const getters = {
  appName: state => state.appName,
  sidebarCollapse: state => state.sidebarCollapse,
};

const actions = {
  [TOGGLE_SIDE_BAR]({ commit }) {
    commit(TOGGLE_SIDE_BAR);
  },
};

const mutations = {
  [TOGGLE_SIDE_BAR](state) {
    state.sidebarCollapse = !state.sidebarCollapse;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
