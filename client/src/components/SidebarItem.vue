<template>
  <div class="menu-item">
    <template v-for="item in menu">
      <template v-if="item.children && !item.hidden">
        <!--只有一个子元素的菜单资源直接单独显示-->
        <el-menu-item
          v-if="item.children.length === 1"
          :index="item.children[0].name"
          :key="item.children[0].name"
          :class="{ 'submenu-title-noDropdown': !isNest }"
        >
          <i :class="[item.children[0].meta.icon || 'fa fa-navicon']"></i>
          <span slot="title">{{ item.children[0].meta.title }}</span>
        </el-menu-item>

        <!--有多个子元素的菜单资源多级显示-->
        <el-submenu v-else :index="item.name" :key="item.name" popper-class="popper-item">
          <template slot="title">
            <i :class="[item.meta.icon || 'fa fa-navicon']"></i>
            <span slot="title">{{ item.meta.title }}</span>
          </template>

          <template v-for="child in item.children">
            <template v-if="!child.hidden">
              <!--多级子菜单循环嵌套-->
              <sidebar-item
                v-if="child.children && child.children.length > 0"
                :is-nest="true"
                class="nest-menu"
                :menu="[child]"
                :key="child.name"
              >
              </sidebar-item>

              <el-menu-item v-else :index="child.name" :key="child.name">
                <i :class="[child.meta.icon || 'fa fa-navicon']"></i>
                <span slot="title">{{ child.meta.title }}</span>
              </el-menu-item>
            </template>
          </template>
        </el-submenu>
      </template>
    </template>
  </div>
</template>

<script>
export default {
  name: 'SidebarItem',
  props: {
    menu: {
      type: Array,
    },
    isNest: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
