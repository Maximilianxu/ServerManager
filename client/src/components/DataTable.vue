<template>
  <div class="data-table">
    <div class="search"></div>

    <div class="table">
      <el-table
        :data="listData"
        :empty-text="emptyText"
        :default-sort="defaultSort"
        :row-class-name="tableRowClassName"
        @sort-change="sortChange"
        v-loading.body="showLoading"
        element-loading-text="拼命加载中"
        size="small"
        border
      >
        <slot name="columns"></slot>
      </el-table>
    </div>

    <div class="pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPageData"
        :page-sizes="pageSizes"
        :page-size="pageSizeData"
        layout="total, prev, pager, next, jumper, sizes"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>
<script>
import {apiCall} from '@/utils/api';
import settings from '@/settings';
import event from '@/utils/event';

export default {
  name: 'DataTable',
  props: {
    // 默认排序
    defaultSort: {
      type: Object,
    },
    // 是否显示pageIndex列
    showPageIndex: {
      type: Boolean,
      default: false,
    },
    // 没有数据显示文字
    emptyText: {
      type: String,
      default: '暂无数据',
    },
    // 当前页数
    currentPage: {
      type: Number,
      default: 1,
    },
    // 每页数据数量
    pageSize: {
      type: Number,
      default: settings.PAGE_SIZE,
    },
    // 附加查询条件
    queryParams: {
      type: Object,
    },
    // 数据接口地址
    apiUrl: {
      type: String,
    },
    // 数据载入成功后回调
    loadCallback: {
      type: Function,
      required: false,
    },
    //  是否默认渲染
    defaultRender: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data() {
    return {
      currentPageData: this.currentPage,
      pageSizeData: this.pageSize,
      pageSizes: [10, 20],
      total: 0,
      listData: [],
      showLoading: false,
      sortParams: {},
    };
  },
  created: function() {
    // 刷新全部数据
    this.$on(event.REFRESH_ALL_DATA, function() {
      this.reload();
    });
    // 刷新当前页数据
    this.$on(event.REFRESH_CURRENT_DATA, function() {
      this.load();
    });
    if (this.defaultRender) {
      this.load();
    }
  },
  methods: {
    tableRowClassName({row, rowIndex}) {
      if (rowIndex % 4 == 0) {
        return 'success-row';
      } else if (rowIndex % 2 == 0){
        return 'warning-row';
      }
      return '';
    },
    handleSizeChange(val) {
      this.pageSizeData = val;
      this.load();
    },
    handleCurrentChange(val) {
      this.currentPageData = val;
      this.load();
    },
    reload() {
      this.currentPageData = 1;
      this.load();
    },
    // 排序改变，向参数注入排序字段
    sortChange(sort) {
      // 参数格式根据需要修改
      this.sortParams = sort.prop
        ? {
            prop: sort.prop,
            order: sort.order,
          }
        : {};
      this.reload();
    },
    // 载入数据
    load() {
      this.showLoading = true;

      const queryParams = Object.assign(
        {
          pageNum: this.currentPageData,
          pageSize: this.pageSizeData,
          order: this.sortParams,
        },
        this.queryParams
      );
      console.log("table call method:", this.method);
      apiCall({
        url: this.apiUrl,
        method: "post",
        data: queryParams,
      })
        .then(d => {
          console.log("get in data table:", d);
          let data = JSON.parse(d["data"]);
          this.listData =
            data &&
            data.map(function(item, index) {
              // 增加序号
              item.pageIndex = (queryParams.pageNum - 1) * queryParams.pageSize + index + 1;
              return item;
            });
          this.total = d["total"];
          return data;
        })
        .then(d => {
          if (this.loadCallback) {
            this.loadCallback(d, queryParams);
          }
        })
        .finally(() => {
          this.showLoading = false;
        });
    },
  },
};
</script>

<style lang="less" scoped>
.data-table {
  width: 100%;
  position: relative;
}

.data-table .pagination {
  display: block;
  text-align: right;
  margin-top: 15px;
  width: 100%;
}
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
