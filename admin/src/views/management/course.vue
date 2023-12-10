<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.keywords" placeholder="course name" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
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
      <el-table-column label="courseName" prop="course_name" min-width="110px" />
      <el-table-column label="sort" prop="sort" min-width="110px" />
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
      <el-form ref="dataForm" :rules="rules" :model="formData" label-position="left" label-width="110px" style="width: 400px; margin-left:50px;">
        <el-form-item label="courseName" prop="course_name">
          <el-input v-model="formData.course_name" />
        </el-form-item>
        <el-form-item label="sort" prop="sort">
          <el-input v-model="formData.sort" />
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
import { getCourseList, createCourse, updateCourse, deleteCourse } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import crypto from '@/crypto'

export default {
  name: 'Course',
  components: { Pagination },
  directives: { waves },
  data() {
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
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      formData: {
        course_name: '',
        sort: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'edit',
        create: 'create'
      },
      rules: {
        course_name: [{ required: true, message: 'Please enter the course name', trigger: 'change' }]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getCourseList(this.listQuery).then(response => {
        this.list = response.data

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
        category_id: '1',
        name: '',
        describe: '',
        avatar_url: '',
        sort: 0
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
          createCourse(data).then(() => {
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
          updateCourse(data).then(() => {
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
      deleteCourse({ id: row.id, userType: this.$store.state.user.userType }).then(() => {
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
</style>
