<template>
  <div class="row">
    <div class="col s6 offset-s3">
      <h1>Create item</h1>

      <form @submit.prevent="submitHandler">
        <div class="input-field">
          <input id="name" v-model="name" type="text" class="validate" required>
          <label for="name">Название</label>
          <span class="helper-text" data-error="Это обязательное поле!"></span>
        </div>
        <div class="input-field">
          <input id="amount" v-model="amount" type="number" class="validate" required>
          <label for="amount">Количество</label>
          <span class="helper-text" data-error="Это обязательное поле!"></span>
        </div>

        <div class="input-field">
          <input id="distance" v-model="distance" type="number" class="validate" required>
          <label for="distance">Расстояние</label>
          <span class="helper-text" data-error="Это обязательное поле!"></span>
        </div>

        <input type="text" ref="datepicker">

        <button class="btn" type="submit">Create item</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'create',
  data: () => ({
    name: '',
    amount: null,
    distance: null,
  }),
  mounted() {
    this.date = M.Datepicker.init(this.$refs.datepicker, {
      defaultDate: new Date(),
      setDefaultDate: true
    })
  },
  methods: {
    submitHandler() {
      const path = 'http://localhost:5000/add/'
      if (this.amount < 0) {
        alert("Неподходящее значение в поле amount")
        return false
      }
      if (this.distance < 0) {
        alert("Неподходящее значение в поле amount")
        return false
      }

      let date = new Date(this.date.date)
      date.setDate(date.getDate() + 1)

      console.log(date)
      const item = {
        name: this.name,
        amount: this.amount,
        distance: this.distance,
        date: date
      }

      axios.post(path, item)
      this.name = ''
      this.amount = null
      this.distance = null
    }
  },
  destroyed() {
    if (this.date && this.date.destroy) {
      this.date.destroy()
    }
  }
}
</script>

<style scoped>

</style>