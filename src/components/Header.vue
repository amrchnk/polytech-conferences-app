<template>
  <header>
    <div class="navbar">
      <router-link class="navbar-brand" to="/"><b class="header">Московский политех. Конференции</b></router-link>

      <ul class="links justify-content-center">
        <li>
          <router-link class="nav-link" to="/">Главная</router-link>
        </li>
      </ul>
      <ul class="btns">
        <li>
          <router-link to="/autho" type="button" class="btn btn-outline-primary">Авторизация</router-link>
        </li>
        <li>
          <router-link to="/reg" type="button" class="btn btn-outline-primary">Регистрация</router-link>
        </li>
      </ul>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  props: {},
  data() {
    return {}
  }
}
</script>

<style scoped>
header {
  background-color: white;
  display: flex;
}

.navbar {
  display: flex;
  align-items: center;
  width: 100%;
}
</style>