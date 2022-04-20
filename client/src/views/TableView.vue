<template>
  <div class="row">
    <div class="input-field col s3">
      <select ref="select_column" v-model="filter_column">
        <option value="" disabled selected>Выберите</option>
        <option value="date">Дата</option>
        <option value="name">Название</option>
        <option value="amount">Количество</option>
        <option value="distance">Расстояние</option>
      </select>
      <label>Выберите колонку</label>
    </div>
    <div class="input-field col s3">
      <select ref="select_condition" v-model="filter_condition">
        <option value="" disabled selected>Выберите</option>
        <option value="equals">Равно</option>
        <option value="includes">Содержит</option>
        <option value="more">Больше</option>
        <option value="less">Меньше</option>
      </select>
      <label>Выберите условие</label>
    </div>

    <div v-if="filter_column !== 'date'" class="input-field col s3">
      <input id="value" type="text" class="validate" v-model="filter_value">
      <label for="value">Значение</label>
    </div>
    <div v-if="filter_column === 'date'" class="input-field row">
      <div class="input-field col s3">
        <input id="date" type="date" v-model="date">
        <label for="date">Дата</label>
      </div>
    </div>

    <div class="input-field col s3">
      <button v-if="filter_condition || filter_column" class="btn btn-small red"
              @click="filter_column = ''; filter_condition = ''; filter_value = ''; day=null; month=null; year=null">
        Clear filter
      </button>
    </div>
    <table v-if="items.length">
      <thead>
      <tr>
        <th>id</th>
        <th><a class="waves-effect waves-teal btn-flat" @click="sort('name')"
               v-bind:class="{active: sort_key === 'name'}">Название</a>
        </th>
        <th><a class="waves-effect waves-teal btn-flat" @click="sort('amount')"
               v-bind:class="{active: sort_key === 'amount'}">Количество</a></th>
        <th><a class="waves-effect waves-teal btn-flat" @click="sort('distance')"
               v-bind:class="{active: sort_key === 'distance'}">Расстояние</a></th>
        <th><a class="waves-effect waves-teal btn-flat" @click="sort('date')"
               v-bind:class="{active: sort_key === 'date'}">Дата</a></th>
        <th>
          <router-link class="btn btn-small green"
                       to="/add">Добавить
          </router-link>
        </th>

      </tr>
      </thead>
      <tbody>
      <TableItem
          v-for="item in this.sortedItems"
          v-bind:item="item"
          v-on:remove_item="removeItem"
      />
      </tbody>
    </table>
    <p v-else>Пока что нет никаких записей!
      <router-link class="btn btn-small green"
                   to="/add">Добавить
      </router-link>
    </p>

  </div>
  <ul>
    <li>
      <button class="waves-effect waves-light btn-small" type="button" @click="prevPage"
              :disabled="current_page === 1">Назад
      </button>
      <button class="waves-effect waves-light btn-small" type="button" @click="nextPage"
              :disabled="current_page === this.pageCount">Вперед
      </button>
    </li>
  </ul>
</template>

<script>
import TableItem from "@/components/TableItem";
import axios from 'axios';

export default {
  components: {TableItem},
  data() {
    return {
      items: [],
      sort_key: 'name',
      direction: 'asc',

      filter_column: '',
      filter_condition: '',
      filter_value: '',
      date: null,

      current_page: 1,
      items_per_page: 2,
    }
  },
  mounted() {
    M.FormSelect.init(this.$refs.select_column)
    M.FormSelect.init(this.$refs.select_condition)
  },
  methods: {
    getItems() {
      const path = `http://localhost:5000/`;
      axios.get(path)
          .then((res) => {
            this.items = res.data;
          })
          .catch((error) => {
            console.error(error);
          });
    },
    removeItem(id) {
      const path = `http://localhost:5000/remove/${id}`;
      axios.delete(path).then(this.getItems);
    },
    prevPage() {
      this.current_page--;
    },
    nextPage() {
      this.current_page++;
    },
    sort: function (s) {
      if (s === this.sort_key) {
        this.direction = this.direction === 'asc' ? 'desc' : 'asc';
      }
      this.sort_key = s;
    },
    nameFilter(item) {
      if (this.filter_condition === 'includes') return item.name.toLowerCase().indexOf(this.filter_value.toLowerCase()) >= 0;
      if (this.filter_condition === 'equals') return item.name.toLowerCase() === this.filter_value.toLowerCase();
      if (this.filter_condition === 'more') return item.name.toLowerCase() > this.filter_value.toLowerCase();
      if (this.filter_condition === 'less') return item.name.toLowerCase() < this.filter_value.toLowerCase();
    },
    amountFilter(item) {
      if (isNaN(parseInt(this.filter_value))) return true
      if (this.filter_condition === 'includes') return item.amount.toString().indexOf(this.filter_value) >= 0;
      const filter_value = parseInt(this.filter_value)
      if (this.filter_condition === 'equals') return item.amount === filter_value;
      if (this.filter_condition === 'more') return item.amount > filter_value;
      if (this.filter_condition === 'less') return item.amount < filter_value;
    },
    distanceFilter(item) {
      if (isNaN(parseInt(this.filter_value))) return true
      if (this.filter_condition === 'includes') return item.distance.toString().indexOf(this.filter_value) >= 0;
      const filter_value = parseInt(this.filter_value)
      if (this.filter_condition === 'equals') return item.distance === filter_value;
      if (this.filter_condition === 'more') return item.distance > filter_value;
      if (this.filter_condition === 'less') return item.distance < filter_value;
    },
    dateFilter(item) {
      let item_date = new Date(item.date)
      let search_date = new Date(this.date)

      if (this.filter_condition === 'equals') return item_date.toString() === search_date.toString();
      if (this.filter_condition === 'more') return item_date > search_date;
      if (this.filter_condition === 'less') return item_date < search_date;
    }
  },
  created() {
    this.getItems();
  },
  computed: {
    filteredItems() {
      return this.items.filter(item => {
        if (this.filter_column === 'date' && this.date) return this.dateFilter(item);
        if (this.filter_value === '' || this.filter_condition === '' || this.filter_column === '') return true;
        if (this.filter_column === 'name') return this.nameFilter(item);
        if (this.filter_column === 'amount') return this.amountFilter(item);
        if (this.filter_column === 'distance') return this.distanceFilter(item);
      })
    },
    pageCount() {
      let l = this.items.length,
          s = this.items_per_page;

      return Math.ceil(l / s);
    },
    sortedItems: function () {
      return this.filteredItems.sort((a, b) => {
        let modifier = 1;
        if (this.direction === 'desc') modifier = -1;
        if (this.sort_key === 'date') {
          if (Date.parse(a.date) > Date.parse(b.date)) return modifier
          else if (Date.parse(a.date) < Date.parse(b.date)) return -1 * modifier
          else return 0
        }
        if (a[this.sort_key] < b[this.sort_key]) return -1 * modifier;
        if (a[this.sort_key] > b[this.sort_key]) return modifier;
        return 0;
      }).filter((row, index) => {
        let start = (this.current_page - 1) * this.items_per_page;
        let end = this.current_page * this.items_per_page;
        if (index >= start && index < end) return true;
      });
    }
  },
  destroyed() {
    if (this.date && this.date.destroy) {
      this.date.destroy()
    }
  }
}
</script>
<style>
.active {
  font-weight: bold;
  color: red;
}
</style>