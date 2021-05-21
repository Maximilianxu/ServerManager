/**
 * 菜单资源，每个菜单资源有一个唯一的名称（name）
 *
 * 用户可以访问的菜单、接口、特殊权限标记等统称为资源
 *
 * 图标：https://fontawesome.com/v4.7.0/icons/
 */

// 页面布局框架
import Layout from '@/views/Layout';

// 用于多级子菜单切换时内容显示
import EmptyContainer from '@/components/EmptyContainer';

// 菜单资源，用于生成路由和左侧菜单树
// 菜单 name 命名方式为 x.x.x，对应 views 文件夹下的文件名，如 name: 'welcome.index' 对应 @views/welcome/index.vue 组件
const menu = [
  {
    name: 'welcome',
    path: '/',
    component: Layout,
    redirect: '/welcome',
    meta: {
      title: '首页',
      icon: 'fa fa-yx-home',
    },
    children: [
      {
        name: 'welcome',
        path: 'welcome',
        component: () => import('@/views/Welcome'),
        meta: {
          title: '首页',
          icon: 'fa fa-yx-home',
        },
      },
    ],
  },
  {
    name: 'apply',
    path: '/apply',
    component: Layout,
    redirect: '/apply/instances',
    meta: {
      title: '申请资源',
      icon: 'fa fa-yx-feature',
    },
    children: [
      {
        name: 'apply.instances',
        path: 'instances',
        meta: {
          title: '可申请实例',
        },
        component: () => import('@/views/Instances'),
      },
      {
        name: 'apply.applied',
        path: 'applied',
        meta: {
          title: '申请队列',
        },
        component: () => import('@/views/Applied'),
      },
    ],
  },
];

export default menu;
