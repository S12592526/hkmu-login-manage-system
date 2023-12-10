<template>
    <div class="app-container">
      <div class="filter-container">
        <el-input v-model="listQuery.keywords" placeholder="courseName" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          search
        </el-button>
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleDownload">
          Download Transcript
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
        <el-table-column label="course" prop="course_id" min-width="110px">
            <template slot-scope="{row}">
            <span>{{ getCourseKeyValue(row.course_id) }}</span>
            </template>
        </el-table-column>
        <el-table-column label="grade" prop="grade" min-width="110px" />
        <el-table-column label="midtermExamScore" prop="midterm_exam_score" />
        <el-table-column label="finalExamScore" prop="final_exam_score" />
      </el-table>
  
      <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    </div>
  </template>
  
  <script>
  import { getStudentScoreList, getCourseList, updateUser, deleteUser, imageUpload } from '@/api/user'
  import waves from '@/directive/waves' // waves directive
  import Pagination from '@/components/Pagination' // secondary package based on el-pagination
  
  export default {
    name: 'User',
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
        courseList: [],
        importanceOptions: [1, 2, 3],
        sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      }
    },
    created() {
      this.handleGetCourseList()
      this.getList()
    },
    methods: {
      getList() {
        this.listLoading = true
        getStudentScoreList({...this.listQuery, uid: this.$store.state.user.uid}).then(response => {
          this.list = response.data
  
          this.listLoading = false
        })
      },
      handleGetCourseList() {
          getCourseList().then(response => {
              this.courseList = response.data
          })
      },
      getCourseKeyValue(type) {
          const courseKeyValue = this.courseList.reduce((acc, cur) => {
                  acc[cur.id] = cur.course_name
                  return acc
              }, {})
          return courseKeyValue[type]
      },
      handleDownload() {
        this.exportToExcel(this.list, 'test')
      },
      exportToExcel(data, fileName) {
        const csv = this.convertToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `${fileName}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      },
      convertToCSV(data) {

        const rows = ['course,grade,midtermExamScore,finalExamScore'];
        for (let i = 0; i < data.length; i++) {
          let dataObj = [this.getCourseKeyValue(data[i].course_id), data[i].grade, data[i].midterm_exam_score, data[i].final_exam_score]
          rows.push(dataObj.join(','));
          
        }
        return rows.join('\n');
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
      getSortClass: function(key) {
        const sort = this.listQuery.sort
        return sort === `${key}` ? 'ascending' : 'descending'
      }
    }
  }
  </script>
  
  <style>
  </style>
  