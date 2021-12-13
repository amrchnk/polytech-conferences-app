<template>
  <div class="main">
    <div class="main_body">
      <div class="main_body_images">
        <div class="main_image image1">
          <img class="" src="@/assets/main.jpg" alt="">
        </div>
        <div class="main_image image2">
          <img class="" src="@/assets/main2.jpg" alt="">
        </div>
      </div>
      <div class="main_body_text">
        <h1>Единая платформа для научных конференций</h1>
        <p class="main_text">Добро пожаловать на сайт конференций Московского Политеха, где вы можете посмотреть новости об актуальных событиях научной жизни университета,
          ознакомиться с материалами прошедших конференций, а так же принять в них участие</p>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "Main"
}
</script>

<style scoped>
.main {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.main_body {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 0 60px;

}

.main_body_images {
  width: 60%;
  display: flex;
  padding-right: 40px;
  padding-left: 20px;
}

.main_image{
  width: 50%;
}

.image1{
  margin-right: 20px;
}

img {
  width: 100%;
}

.main_body_text{
  width: 40%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start!important;
}

h1{
  font-size: 1.8em;
  font-weight: bold;
}

.main_text{
  font-size: 1.5em;
}
</style>