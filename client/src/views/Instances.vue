<template>
  <div>
    <data-table
      ref="dateTable"
      :apiUrl="instancesURL"
      :row-class-name="tableRowClassName"
      :key="tableKey"
    >
    <template slot="columns">
      <el-table-column
      type="index"
      width="50"
      label="实例"
      align="center">
      </el-table-column>
      <el-table-column prop="name" label="Servant" align="center"></el-table-column>
      <el-table-column prop="user" label="Master" align="center" :formatter="userFormat"></el-table-column>
      <el-table-column prop="left_time" label="时长" align="center" 
        :formatter="timeFormat">
      </el-table-column>
      <el-table-column prop="status" label="状态" align="center" 
        :formatter="statusFormat">
      </el-table-column>
      <el-table-column prop="gpu_num" label="GPU数量">
        <template slot-scope="scope">
          <el-select v-model="scope.row.gpu_num" placeholder="请选择" :disabled="handleDisable(scope.$index, scope.row)">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          </template>
      </el-table-column>
      <el-table-column
      label="操作"
      align="center">
      <template slot-scope="scope">
        <el-button
          type="warning"
          size="mini"
          icon="el-icon-edit"
          :disabled="handleDisable(scope.$index, scope.row)"
          @click="handleApply(scope.$index, scope.row)">申请</el-button>
      </template>
    </el-table-column>
    </template>
    </data-table>
  </div>
</template>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>

<script>
import {api_routes, apiCall} from '@/utils/api';
import DataTable from '@/components/DataTable';

export default {
  name: 'bigTable',
  components: {
    DataTable,
  },
  data() {
    return {
      instancesURL: api_routes.user.instances,
      method: "post",
      tableKey: 0,
      options: [{
        value: 0,
        label: '仅CPU资源'
      }, {
        value: 1,
        label: '1卡'
      }, {
        value: 2,
        label: '2卡'
      },{
        value: 3,
        label: '3卡'
      },{
        value: 4,
        label: '4卡'
      },],
    };
  },
  mounted() {},
  methods: {
    gpuFormat(row, column) {
      return row.gpu_num + "卡";
    },
    timeFormat(row, column) {
      return row.left_time + "天";
    },
    userFormat(row, column) {
      if(row.user){
        return row.user.name;
      }
      return "";
    },
    statusFormat(row, column) {
      if (row.status == "free"){
        return "空闲";
      }else if (row.status == "wait"){
        return "已被申请";
      }else{
        return "已被分配";
      }
    },
    tableRowClassName({row, rowIndex}) {
      console.log("row class ", rowIndex, rowIndex % 2, rowIndex == 1);
      if ((rowIndex % 3) == 1) {
        return 'warning-row';
      } else{
        return 'success-row';
      }
    },
    handleApply(row_index, row){
      let {name, gpu_num, opt_gpu_num} = row;
      let applyURL = api_routes.user.apply;
      this.$confirm('这会提交一次申请，确认吗', 'Warning', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '申请已提交'
        });
        apiCall({url: applyURL, data: {name, gpu_num, opt_gpu_num}, method: "post"})
          .then(resp => {this.$message({type: 'info', message: resp.message}); this.tableKey += 1;});
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '申请取消'
        });          
      });
    },
    handleDisable(index, row){
      return row.status != "free";
    }
  },
};
</script>
