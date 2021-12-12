<template>
  <div id="app">
    <Header/>
    <router-view></router-view>
  </div>
</template>

<script>

import Header from "./components/Header";
export default {
  name: 'App',
  components: {
    Header,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

router-link{
  text-decoration: none!important;
}

@import url("assets/fonts/gilroy/stylesheet.css");
</style>
