<template>
  <header>
    <div class="navbar">
      <router-link class="navbar_logo" to="/">
        <div class="img navbar_logo_item"><img src="@/assets/logo.png"></div>
        <b class="navbar_logo_item header">Конференции</b></router-link>

      <ul class="navbar_links">
        <li>
          <router-link class="navbar_links_item" to="/">Главная</router-link>
        </li>
        <li>
          <router-link class="navbar_links_item" to="/">Мероприятия</router-link>
        </li>
      </ul>
      <ul class="btns">
        <li>
          <div type="button" class="btn btn-outline-primary" @click="$emit('open')">Войти в аккаунт</div>
        </li>
      </ul>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style scoped>

header {
  background-color: white;
  display: flex;
  font-family: Gilroy;
}

.navbar {
  display: flex;
  align-items: center;
  width: 100%;
  margin: 20px 30px;
}

.navbar_logo {
  display: flex;
  justify-content: center !important;
  align-items: center !important;
  text-decoration: none;
}

ul {
  display: flex !important;
  align-items: center !important;
  margin-bottom: 0;
  padding-left: 0;
}

li {
  list-style-type: none;
}

.navbar_links {
  font-weight: normal;
  text-transform: uppercase;
  font-size: 1.2em;
}

.navbar_links_item {
  color: black !important;
  margin-right: 30px;
}

a {
  text-decoration: none !important;
}

.header {
  color: #4B6EB9;
  font-weight: bold;
  font-size: 2em;
  margin-left: 30px;
  background-color: white;
  font-weight: 600;
}

.btn {
  color: #4B6EB9;
  border-color: #4B6EB9;
  font-size: 1.2em;
  float: right;
}

.btn:hover {
  background-color: #4B6EB9;
  color: white;
}
</style>