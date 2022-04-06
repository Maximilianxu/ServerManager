<template>
  <div class="topbar">
    <el-dropdown placement="bottom">
      <span class="el-dropdown-link">
        <i class="fa fa-user-circle-o"></i>&nbsp;&nbsp;{{ getProfile.name}}
        <i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native="logout">退出系统</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import settings from '@/settings';
import {AUTH_LOGOUT} from '@/store/actions/auth';
import {USER_REQUEST} from "@/store/actions/user";

export default {
  name: 'Topbar',
  data() {
    return {
      systemName: settings.APP_NAME,
    };
  },
  computed: {
    getProfile() {
      let profile = this.$store.getters.getProfile;
      console.log("profile", profile);
      if (!("name" in profile)){
        this.$store.dispatch(USER_REQUEST);
        profile = this.$store.getters.getProfile;
      }
      return profile;
    },
  },
  methods: {
    logout() {
      this.$confirm('是否退出系统？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      })
        .then(() => {
          this.$store.dispatch(AUTH_LOGOUT).then(() => {
            this.$router.push({ path: '/login' });
          });
        })
        .catch(() => {});
    },
  },
};
</script>
