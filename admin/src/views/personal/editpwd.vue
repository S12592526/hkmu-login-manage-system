<template>
    <div class="app-container">
        <el-form ref="dataForm" :rules="rules" :model="formData" label-position="left" label-width="150px" style="width: 400px; margin-left:50px;">
          <el-form-item label="account" prop="account">
            <el-input v-model="formData.account" :disabled="true" />
          </el-form-item>
            <el-form-item label="newPassword" prop="password">
            <el-input v-model="formData.password" type="password" />
            </el-form-item>
            <el-form-item label="confirmPassword" prop="checkpwd">
            <el-input v-model="formData.checkpwd" type="password" />
            </el-form-item>
          <el-form-item label="securityIssues" prop="security_issues">
            <el-input v-model="formData.security_issues" :disabled="true" />
          </el-form-item>
          <el-form-item label="securityAnswer" prop="security_answer">
            <el-input v-model="formData.security_answer" />
          </el-form-item>
        </el-form>
        <div class="footer">
          <el-button type="primary" @click="handleUpdataInfo()">save</el-button>
        </div>
    </div>
  </template>
  
  <script>
  import { getStudentInfo, studentEditPwd } from '@/api/user'
  import waves from '@/directive/waves' // waves directive
  import crypto from '@/crypto'
  
  export default {
    name: 'Info',
    directives: { waves },
    data() {
      const validatePassword = (rule, value, callback) => {
        let reg = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F])[\da-zA-Z\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F]{8,}$/;

        if (!reg.test(value)) {
          callback(new Error('Please enter the user password, which includes uppercase and lowercase English, numbers, symbols, and more than 8 characters'))
        } else {
          callback()
        }
      };
	    let validatePass2 = (rule, value, callback) => {
	      if (value === "") {
	        callback(new Error("Please enter the password again"));
	      } else if (value !== this.formData.password) {
	        callback(new Error("The two passwords entered do not match!"));
	      } else {
	        callback();
	      }
	    };
      return {
        formData: {
          account: '',
          password: '',
          checkpwd: '',
          security_issues: '',
          security_answer: ''
        },
        rules: {
          password: [{ required: true, trigger: 'blur', validator: validatePassword }],
          checkpwd: [{ required: true, trigger: 'blur', validator: validatePass2 }]
        },
      }
    },
    created() {
      this.handleGetStudentInfo()
    },
    methods: {
      handleGetStudentInfo() {
        getStudentInfo().then(response => {
          delete response.data.password
          delete response.data.security_answer
          this.formData = response.data
          if (!response.data.security_issues && !response.data.security_answer) {
            
          }
        })
      },
      handleUpdataInfo() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            let data = {...this.formData, userType: this.$store.state.user.userType}
            delete data.checkpwd
            data.password = crypto.encrypt(data.password)
            data.security_answer = crypto.encrypt(data.security_answer)
            studentEditPwd(data).then(() => {
              this.handleGetStudentInfo()
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
    }
  }
  </script>
  
  <style>
    .footer {
        padding-left: 20px;
    }
  </style>
  