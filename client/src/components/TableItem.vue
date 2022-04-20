<template>
  <tr>
    <td>{{ item.id }}</td>
    <td>{{ item.name }}</td>
    <td>{{ item.amount }}</td>
    <td>{{ item.distance }}</td>
    <td>{{ item.date }}</td>
    <td><button class="btn-floating btn-small waves-effect waves-light red"
            v-on:click="$emit('remove_item', item.id)"
    >&times;</button></td>
  </tr>
</template>

<script>
export default {
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  name: "TableItem"
}
</script>

<style scoped>
</style>