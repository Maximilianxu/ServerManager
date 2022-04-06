<template>
  <div>
    <data-table
      ref="dateTable"
      :apiUrl="appliedURL"
      :row-class-name="tableRowClassName"
      :key="tableKey"
    >
    <template slot="columns" style="width: 100%" >
      <el-table-column prop="name" label="实例" align="center" :min-width="15">
      </el-table-column>
      <el-table-column prop="gpu_num" label="GPU 配置" align="center" :min-width="20"
        :formatter="gpuFormat">
      </el-table-column>
      <el-table-column prop="left_time" label="时长" align="center" :min-width="20"
        :formatter="timeFormat">
      </el-table-column>
      <el-table-column prop="status" label="状态" align="center" :min-width="10"
        :formatter="statusFormat">
      </el-table-column>
      <el-table-column prop="port" label="端口" align="center" :min-width="15"
        :formatter="portFormat">
      </el-table-column>
      <el-table-column label="密码" align="center" prop="password" :min-width="50">
        <template slot-scope="scope">
          <span style="margin-right:1.25em;">{{scope.row.password}}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <el-button
            icon="el-icon-copy-document"
            round
            size="mini"
            v-clipboard:copy="scope.row.password"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError"
          >copy</el-button>
        </template>
      </el-table-column>
      <el-table-column
      label="操作"
      align="center"
      :min-width="30">
      <template slot-scope="scope" prop="operation" >
        <el-button
          type="danger"
          size="mini"
          icon="el-icon-delete"
          @click="handleRelease(scope.$index, scope.row)">释放</el-button>
      <!-- </template>
      <template slot-scope="scope" prop="operation"> -->
        <el-button type="info" size="mini" icon="el-icon-share" 
          :disabled="handleDisable(scope.$index, scope.row)"
          @click="dialogFormShow(scope.$index, scope.row)">分享</el-button>
      </template>
    </el-table-column>
    </template>
    </data-table>
    <el-dialog title="分享实例" :visible.sync="dialogFormVisible">
          <el-form :model="form">
            <el-form-item label="目标账户" :label-width="form.formLabelWidth">
              <el-input v-model="form.to_share_id_number"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="shareInstance()">确 定</el-button>
          </div>
        </el-dialog>
  </div>
</template>

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
      appliedURL: api_routes.user.applied,
      tableKey: 0,
      dialogFormVisible: false,
      form:{
        to_share_inst: "",
        to_share_id_number: "",
        formLabelWidth: '120px',
      }
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
    statusFormat(row, column) {
      status = row.status;
      if (status == "wait") {
        return "排队中";
      }else if (status == "allocated"){
        return "已分配";
      }
      return "Error Status";
    },
    portFormat(row, column){
      if (row.status == "allocated"){
        return row.port;
      }else{
        return "xxxx";
      }
    },
    onCopy: function (e) {
      this.$message({type: 'info', message:"已复制"});
    },
    onError: function (e) {
      this.$message({type: 'warning', message:"浏览器不支持"});
      console.log(e);
    },
    tableRowClassName({row, rowIndex}) {
      if (rowIndex === 1) {
        return 'warning-row';
      } else if (rowIndex === 3) {
        return 'success-row';
      }
      return '';
    },
    shareInstance(){
      let shareURL = api_routes.user.share;
      apiCall({url: shareURL, data: {"to_share_inst": this.form.to_share_inst, 
        "to_share_id_number": this.form.to_share_id_number}, method: "PUT"})
        .then(resp => {
          this.$message({type: 'info', message: resp.message});
          this.tableKey += 1;
          console.log("table key in then: ", this.tableKey);})
          .catch(() => {
          this.$message({
            type: 'info',
            message: '分享失败'
          });   
          this.tableKey += 1;             
        });
    },
    dialogFormShow(row_index, row){
      this.dialogFormVisible = true;
      console.log("to share", row.name);
      this.form.to_share_inst = row.name;
    },
    handleRelease(row_index, row){
      let {name} = row;
      let releaseURL = api_routes.user.release;
      this.$confirm('这会释放资源，无论是否已被分配，确认吗', 'Warning', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '资源已释放'
        });
        
        apiCall({url: releaseURL, data: {name}, method: "delete"})
          .then(resp => {
            this.$message({type: 'info', message: resp.message});
            this.tableKey += 1;
            console.log("table key in then: ", this.tableKey);});
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消释放'
        });   
        this.tableKey += 1;             
      });
    },
    handleDisable(index, row){
      return row.status != "allocated";
    }
  },
};
</script>

<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>