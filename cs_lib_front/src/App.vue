<template>
  <div id="app">
    <UserLogin v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
    <MainPage v-else />
  </div>
</template>

<script>
import UserLogin from './components/UserLogin.vue'
import MainPage from './components/MainPage.vue';

export default {
  components: { UserLogin, MainPage },
  data() {
    return {
      isLoggedIn: false,
    };
  },
  mounted() {
    this.isLoggedIn = !!localStorage.getItem('accessToken');
  },
  methods: {
    handleLoginSuccess(email) {
      localStorage.setItem('userEmail', email);
      this.isLoggedIn = true;
    },
  },
};
</script>
