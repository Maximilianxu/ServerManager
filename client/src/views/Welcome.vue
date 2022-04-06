<template>
  <div>
    <p>欢迎访问 {{ systemName }}</p>
    <h4>关于时长的更新：2卡的时长恢复至10天，但如果你申请的卡不多于1，则延长至15天；</h4>
      <h3>配额的更新：申请需要满足两种配额，个人配额：依然是3实例和4张卡；组配额：戴老师组和王老师组总量各4张卡。
        如果组配额超限（会给出提示），应当尝试减少申请数目，或者联系组内同学，争取共用或者及早释放；</h3>
      <h4> 配置更新：硬盘增大至256GB。</h4>
    <p>系统配置：系统预分配了大概11个实例，每一个实例都可以动态添加GPU。</p>
    <p>如何申请: 进入菜单——申请资源/可申请实例，选择相应的实例即可。申请时请注意选择GPU数量，也可选择只使用CPU。</p>
    <p>关于排队：当GPU数量不足时，申请实例会进入排队；每一个实例都会持续15-30天，到期自动释放</p>
    <p>关于配额：每个人最多同时申请3个实例或者4个GPU，人可真不能贪心呢</p>
    <p>如何使用：分配之后，会给一个随机密码和端口，实例会有默认用户ubuntu。
      假设端口是20000， ssh连接：ssh -p 20000 ubuntu@210.28.135.11。
      容器有root权限，root密码也是分配的随机密码，和ubuntu用户一样。</p>
    <p>备注：由于GPU数量较少，不使用还请及时释放资源哦。</p>
    <p>备注：NVIDIA 驱动用的是宿主的，所以安装时需要把cuda里包含的驱动取消勾选。推荐版本：cuda 11.2.2</p>
    <p>备注：代码地址 https://github.com/Maximilianxu/ServerManager，可以到上面提issue哦</p>
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
