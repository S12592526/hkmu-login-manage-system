<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.keywords" placeholder="名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        add
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="account" prop="account" min-width="110px">
        <template slot-scope="{row}">
          <span>{{ row.account }}</span>
        </template>
      </el-table-column>
      <el-table-column label="userName" prop="user_name" min-width="110px" />
      <el-table-column label="phone" align="center">
        <template slot-scope="{row}">
          <span>{{ row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column label="email" prop="email" />
      <el-table-column label="college" prop="college" />
      <el-table-column label="gender" prop="gender">
        <template slot-scope="{row}">
          <span>{{ row.gender | typeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="operate" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            edit
          </el-button>
          <el-popconfirm
            :key="row.id"
            title="Are you sure to delete it?"
            @onConfirm="handleDelete(row,$index)"
          >
            <el-button slot="reference" v-if="row.status!='deleted'" size="mini" type="danger">
              delete
            </el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="formData" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
        <el-form-item label="account" prop="account">
          <el-input v-model="formData.account" />
        </el-form-item>
        <el-form-item label="password" prop="password">
          <el-input v-model="formData.password" type="password" />
        </el-form-item>
        <el-form-item label="userName" prop="user_name">
          <el-input v-model="formData.user_name" />
        </el-form-item>
        <el-form-item label="phone" prop="phone">
          <el-input v-model="formData.phone" type="phone" />
        </el-form-item>
        <el-form-item label="email" prop="email">
          <el-input v-model="formData.email" />
        </el-form-item>
        <el-form-item label="college" prop="college">
          <el-input v-model="formData.college" />
        </el-form-item>
        <el-form-item label="gender" prop="gender">
          <el-select v-model="formData.gender" class="filter-item" placeholder="Please select">
            <el-option v-for="item in genderOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          confirm
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getTeacherList, createTeacherUser, updateTeacherUser, deleteTeacherUser, imageUpload } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import crypto from '@/crypto'

const genderOptions = [
  { key: 0, display_name: 'unknown' },
  { key: 1, display_name: 'male' },
  { key: 2, display_name: 'Female' }
]

const genderKeyValue = genderOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'User',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return genderKeyValue[type]
    },
  },
  data() {
      const validatePassword = (rule, value, callback) => {
        let reg = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F])[\da-zA-Z\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F]{8,}$/;


        if (!reg.test(value)) {
          callback(new Error('Please enter the user password, which includes uppercase and lowercase English, numbers, symbols, and more than 8 characters'))
        } else {
          callback()
        }
      };
    const validateEmail = (rule, value, callback) => {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!re.test(value)) {
          callback(new Error('Please enter the correct user email'))
        } else {
          callback()
        }
      };
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        keywords: undefined,
        sort: '-id'
      },
      importanceOptions: [1, 2, 3],
      genderOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      formData: {
        account: '',
        password: '',
        user_name: '',
        phone: '',
        email: '',
        college: '',
        gender: 0
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'edit',
        create: 'create'
      },
      rules: {
        account: [{ required: true, message: '请输入账户', trigger: 'change' }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        email: [{ required: true, trigger: 'blur', validator: validateEmail }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getTeacherList({...this.listQuery, userType: this.$store.state.user.userType}).then(response => {
        this.list = response.data.results
        this.total = response.data.count

        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: 'Operation Success',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = 'id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.formData = {
        account: '',
        password: '',
        user_name: '',
        phone: '',
        email: '',
        college: '',
        gender: 0
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          let data = {...this.formData, userType: this.$store.state.user.userType}
          data.password = crypto.encrypt(data.password)
          createTeacherUser(data).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: 'notice',
              message: 'Created successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      console.log(row)
      this.formData = Object.assign({}, row) // copy obj
      this.formData.password = crypto.decrypt(this.formData.password)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          let data = {...this.formData, userType: this.$store.state.user.userType}
          data.password = crypto.encrypt(data.password)
          updateTeacherUser(data).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: 'notice',
              message: 'Successfully modified',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row) {
      deleteTeacherUser({ id: row.id, userType: this.$store.state.user.userType}).then(() => {
        this.getList()
        this.$notify({
          title: 'notice',
          message: 'Successfully deleted',
          type: 'success',
          duration: 2000
        })
      })
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>

<style>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
