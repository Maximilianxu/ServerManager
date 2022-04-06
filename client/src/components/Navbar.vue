<template>
  <el-row type="flex" class="navbar" justify="space-between">
    <el-col :span="18">
      <breadcrumb :is-collapse="isCollapse"></breadcrumb>
    </el-col>
    <el-col :span="6">
      <topbar></topbar>
    </el-col>
  </el-row>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb';
import Topbar from '@/components/Topbar';

export default {
  name: 'Navbar',
  components: {
    Breadcrumb,
    Topbar,
  },
  props: {
    isCollapse: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
