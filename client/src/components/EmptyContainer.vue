<template>
  <!--加入 key 防止不同路由组件相同的情况下不重复加载-->
  <router-view :key="$route.fullPath" />
</template>

<script>
export default {
  name: 'EmptyContainer',
};
</script>
