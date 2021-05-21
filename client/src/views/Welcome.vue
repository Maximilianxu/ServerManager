<template>
  <div>
    <p>欢迎访问 {{ systemName }} </p>
    <p>一些说明: 系统预分配了大概11个实例，每一个实例可以动态添加GPU，申请时请注意选择GPU数量，或者选择只使用CPU。</p>
    <p>当GPU数量不足时，会排队；每一个实例都会持续10天，到期自动释放。</p>
  </div>
</template>

<script>
import settings from '@/settings';

export default {
  name: 'welcome',
  data() {
    return {
      systemName: settings.APP_NAME,
    };
  },
};
</script>
