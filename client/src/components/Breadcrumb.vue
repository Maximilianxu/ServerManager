<template>
  <div class="breadcrumb">
    <span class="toggle-sidebar" :class="{ collapse: isCollapse }" @click.prevent="TOGGLE_SIDE_BAR">
      <i class="fa fa-icon-bars"></i>
    </span>
    <el-breadcrumb>
      <el-breadcrumb-item v-for="(item, index) in levelList" :key="item.name">
        <span
          v-if="item.redirect === 'noredirect' || index == levelList.length - 1"
          class="no-redirect"
          :class="{ current: index == levelList.length - 1 }"
        >
          {{ item.meta.title || item.name }}
        </span>
        <router-link v-else :to="{ name: item.name }">
          {{ item.meta.title || item.name }}
        </router-link>
      </el-breadcrumb-item>
    </el-breadcrumb>
    <div id="loading-container"></div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import {TOGGLE_SIDE_BAR} from '@/store/actions/user';

export default {
  name: 'Breadcrumb',
  created() {
    this.getBreadcrumb();
  },
  data() {
    return {
      levelList: null,
    };
  },
  props: {
    isCollapse: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    $route() {
      this.getBreadcrumb();
    },
  },
  methods: {
    ...mapActions([TOGGLE_SIDE_BAR]),
    getBreadcrumb() {
      let matched = this.$route.matched.filter(item => item.name);
      const first = matched[0];
      if (first && first.name !== 'welcome') {
        // matched = [
        //   {
        //     name: 'welcome',
        //     path: '/welcome',
        //     meta: { title: '首页' },
        //   },
        // ].concat(matched);
      } else {
        matched.shift();
      }
      this.levelList = matched;
    },
  },
};
</script>
