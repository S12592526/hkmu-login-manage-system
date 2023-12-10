<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" autocomplete="on"
      label-position="left" v-show="!showRegister">

      <div class="title-container">
        <h3 class="title">login</h3>
      </div>

      <el-form-item prop="account">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input ref="account" v-model="loginForm.account" placeholder="account" name="account" type="text" tabindex="1"
          autocomplete="on" />
      </el-form-item>
      <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input :key="passwordType" ref="password" v-model="loginForm.password" :type="passwordType" placeholder="password"
            name="password" tabindex="2" autocomplete="on" @keyup.native="checkCapslock" @blur="capsTooltip = false"
            @keyup.enter.native="handleLogin" />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>
      </el-tooltip>

      <el-form-item prop="captcha">
        <div class="captcha">
          <span class="svg-container">
            <svg-icon icon-class="guide" />
          </span>
          <el-input ref="captcha" v-model="loginForm.captcha" placeholder="captcha" name="captcha" type="text" tabindex="1"
            autocomplete="on" />
          <img class="captcha_img" :src="'data:image/jpeg;base64,' + captcha.image" @click="handleGetCaptcha">
        </div>
      </el-form-item>

      <el-form-item prop="userType">
        <div class="userType">
          <span class="svg-container">
            <svg-icon icon-class="list" />
          </span>
          <el-radio-group v-model="loginForm.userType" style="margin-left: 16px;">
            <el-radio :label="0">student</el-radio>
            <el-radio :label="1">teacher</el-radio>
            <el-radio :label="2">administrator</el-radio>
          </el-radio-group>
        </div>
      </el-form-item>
      <div class="register" v-show="loginForm.userType === 0">
        <div class="btn" @click="showRegister = true">register student</div>
      </div>
      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;"
        @click.native.prevent="handleLogin">login</el-button>
    </el-form>

    <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="login-form" autocomplete="on"
      label-position="left" v-show="showRegister">

      <div class="title-container">
        <h3 class="title">register</h3>
      </div>

      <el-form-item prop="account">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input ref="account" v-model="registerForm.account" placeholder="account" name="account" type="text" tabindex="1"
          autocomplete="on" />
      </el-form-item>
      <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input :key="passwordType" ref="password" v-model="registerForm.password" :type="passwordType" placeholder="password"
            name="password" tabindex="2" autocomplete="on" @keyup.native="checkCapslock" @blur="capsTooltip = false"
            @keyup.enter.native="handleLogin" />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>
      </el-tooltip>

      <el-form-item prop="captcha">
        <div class="captcha">
          <span class="svg-container">
            <svg-icon icon-class="guide" />
          </span>
          <el-input ref="captcha" v-model="registerForm.captcha" placeholder="captcha" name="captcha" type="text" tabindex="1"
            autocomplete="on" />
          <img class="captcha_img" :src="'data:image/jpeg;base64,' + captcha.image" @click="handleGetCaptcha">
        </div>
      </el-form-item>

      <div class="register">
        <div class="btn" @click="showRegister = false">return login</div>
      </div>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;"
        @click.native.prevent="handleRegister">register</el-button>
    </el-form>

  </div>
</template>

<script>
import { uuid } from '@/utils/uuid'
import { getCaptcha, registerStudent } from '@/api/user'
import crypto from '@/crypto'
export default {
  name: 'Login',
  data() { 
    const validateAccount = (rule, value, callback) => {
      if (!value) {
        callback(new Error('enter one user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      let reg = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F])[\da-zA-Z\x21-\x2f\x3a-\x40\x5b-\x60\x7B-\x7F]{8,}$/;

      if (!reg.test(value)) {
        callback(new Error('Please enter the user password, which includes uppercase and lowercase English, numbers, symbols, and more than 8 characters'))
      } else {
        callback()
      }
    }
    const validateCaptcha = (rule, value, callback) => {
      if (!value) {
        callback(new Error('Please enter the verification code'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        account: '',
        password: '',
        uuid: '',
        captcha: '',
        userType: 0
      },
      loginRules: {
        account: [{ required: true, trigger: 'blur', validator: validateAccount }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        captcha: [{ required: true, trigger: 'blur', validator: validateCaptcha }]
      },
      registerForm: {
        account: '',
        password: '',
        uuid: '',
        captcha: '',
      },
      registerRules: {
        account: [{ required: true, trigger: 'blur', validator: validateAccount }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        captcha: [{ required: true, trigger: 'blur', validator: validateCaptcha }]
      },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      showDialog: false,
      redirect: undefined,
      otherQuery: {},
      captcha: {
        uuid: '',
        image: ''
      },
      showRegister: false
    }
  },
  watch: {
    $route: {
      handler: function (route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          this.otherQuery = this.getOtherQuery(query)
        }
      },
      immediate: true
    }
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  mounted() {
    if (this.loginForm.account === '') {
      this.$refs.account.focus()
    } else if (this.loginForm.password === '') {
      this.$refs.password.focus()
    }
    this.handleGetCaptcha()
  },
  destroyed() {
    // window.removeEventListener('storage', this.afterQRScan)
  },
  methods: {
    handleGetCaptcha() {
      const id = uuid()
      this.captcha.uuid = id
      this.loginForm.uuid = id
      this.registerForm.uuid = id
      getCaptcha(id).then((res) => {
        this.captcha.image = res.data
      })
    },
    checkCapslock(e) {
      const { key } = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm)
            .then(() => {
              this.$router.push({ path: this.redirect || '/', query: this.otherQuery })
              this.loading = false
            })
            .catch(() => {
              this.loading = false
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleRegister() {
      this.$refs['registerForm'].validate((valid) => {
        if (valid) {
          let data = this.registerForm
          data.password = crypto.encrypt(data.password)
          registerStudent(this.registerForm).then(() => {
            this.handleGetCaptcha()
            this.showRegister = false
            this.$notify({
              title: 'notice',
              message: 'register successful',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }

  .captcha {
    display: inline-flex;
    flex-direction: row;
    width: 100%;
    border-radius: 5px;
    overflow: hidden;

    .captcha_img {
      height: 47px;
      width: 120px;
    }

    .el-input {
      flex: 1;
    }
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;

    .register {
      padding: 0 10px 10px 10px;

      .btn {
        color: #f5f5f5;
        cursor: pointer;
        text-align: right;
      }
    }
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
