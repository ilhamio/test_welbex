<template>
  <div id="app">
    <div class="col s3"><h2>WelbeX Test Case</h2></div>
    <div class="col s3">
      <router-link class="btn btn-small green" to="/table">Таблица</router-link>
    </div>

    <hr>
    <router-view/>
  </div>
</template>

<style lang="scss">
@import "materialize-css/dist/css/materialize.min.css";
</style>
