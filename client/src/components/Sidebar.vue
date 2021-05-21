<template>
  <el-scrollbar wrapClass="scrollbar-wrapper">
    <span class="brand"></span>
    <el-menu
      mode="vertical"
      :show-timeout="200"
      :default-active="$route.name"
      :collapse="isCollapse"
      @select="handleSelect"
      background-color="#F9F7E8"
      text-color="#000"
      active-text-color="#00c1de"
    >
      <sidebar-item :menu="menu"></sidebar-item>
    </el-menu>
  </el-scrollbar>
</template>

<script>
import SidebarItem from '@/components/SidebarItem';
import permission from '@/utils/permission';

export default {
  name: 'Sidebar',
  components: {
    SidebarItem,
  },
  data() {
    return {
      menu: permission.filteredMenu(), // 只显示授权访问的菜单
    };
  },
  props: {
    isCollapse: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    // 导航菜单的点选处理
    handleSelect(index) {
      this.$router.push({ name: index });
    },
  },
};
</script>
