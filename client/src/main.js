import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueSnackbar from "vue-snack";
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
import ButtonSpinner from "@/components/ButtonSpinner";
import Alert from '@/components/Alert.vue';
import VueClipboard from 'vue-clipboard2'
// import BootstrapVue from 'bootstrap-vue';
// import 'bootstrap/dist/css/bootstrap.css';
// 引入 CSS resets，统一各浏览器下基础样式表现 http://necolas.github.io/normalize.css/
import 'normalize.css/normalize.css';

// 引入 ElementUI http://element-cn.eleme.io
// 因为用于后台管理系统，一般是内网使用，所以不做按需引入
import ElementUI from 'element-ui';
import locale from 'element-ui/lib/locale/lang/zh-CN'; // 语言文件

// 进度条样式
import 'nprogress/nprogress.css';

// font-awesome
import 'font-awesome/css/font-awesome.css';

// 引入全局样式，所有 global 样式设置在这里
import './assets/main.less';

// 引入权限
import '@/utils/permission';

Vue.use(ElementUI, { locale });
// Vue.use(BootstrapVue);
Vue.use(Alert);
Vue.use(VueClipboard);
UIkit.use(Icons);
window.UIkit = UIkit;

// loads the Icon plugin
window._ = require("lodash");

require("./styles/index.scss");
require("vue-snack/dist/vue-snack.min.css");

Vue.config.productionTip = false;

window.Event = new Vue();

Vue.use(VueSnackbar, {});

Vue.component("button-spinner", ButtonSpinner);
// Vue.component("alert", Alert);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");

