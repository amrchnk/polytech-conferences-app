<template>
  <div class="main">
    <div class="form">
      <div class="form_header">
        <h2>
          Вход в систему для организаторов
        </h2>
        <i class="material-icons" @click="$emit('close')">close</i>
      </div>

      <div class="form_fields">
        <div class="form_fields_field">
          <label class="form-label">Логин</label>
          <input class="form-control">
        </div>
        <div class="form_fields_field">
          <label class="form-label">Пароль</label>
          <input class="form-control">
        </div>
      </div>

      <div class="form_buttons">
        <button class="btn">Войти</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AuthForm"
}
</script>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form {
  width: 30%;
  background-color: white;
  border-radius: 10px;
  border: 0.5px solid #E5E5E5;
  margin-top: 30px;
  padding: 25px;
}

.form_header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.6em;
}

.form_fields {
  margin: 30px 0;
}

.form_fields_field {
  width: 100%;
  margin-bottom: 20px;
  clear: both;
  text-align: left;
}

.form-label {
  font-size: 1.2em;
}

h2, i {
  font-size: 1em;
}

i {
  color: gray;
}

i:hover {
  cursor: pointer;
}

.btn {
  background-color: #4B6EB9;
  color: white;
  font-size: 1.2em;
  padding: 6px 20px;
}

.btn:hover {
  background-color: #4B6EB9;
  color: white;
}
</style>