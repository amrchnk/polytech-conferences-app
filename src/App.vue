<template>
  <div id="app">
    <Header @open="show_auth_modal = true"/>
    <AuthForm v-if="show_auth_modal" @close="show_auth_modal = false"/>
    <router-view></router-view>
  </div>
</template>

<script>

import Header from "./components/Header";
import AuthForm from "./components/AuthForm";

export default {
  name: 'App',
  components: {
    AuthForm,
    Header,
  },
  data() {
    return {
      show_auth_modal: false
    }
  },
  mounted() {

  }
}
</script>

<style>
#app {
  font-family: Gilroy, Avenir, Helvetica, Arial, sans-serif;
}

router-link {
  text-decoration: none !important;
}

@import url("assets/fonts/gilroy/stylesheet.css");
</style>
