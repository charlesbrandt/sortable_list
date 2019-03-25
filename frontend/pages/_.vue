<template>
  <section class="container">
    <ul>
      <Content
        v-for="item in items"
        v-bind:item="item"
        v-bind:key="item.name"
      ></Content>
  <!--
      <li v-for="item in items">
        <content :item="item"/>
      </li>
    -->
    </ul>
  </section>
</template>

<script>
import axios from 'axios'
import Content from '~/components/Content.vue'
// import router from 'vue-router'

//console.log(router.currentRoute)
//console.log(params)

export default {
  async asyncData ({ params }) {
    // https://nuxtjs.org/guide/routing/#unknown-dynamic-nested-routes
    //console.log("params", params)
    var source = 'http://localhost:8888/' + params[0]
    var data
    //let { data } = await axios.get(`http://localhost:8888/json-path/c/charles`)
    await axios
      .get(source)
      .then(response => (data = response.data))
      .catch(error => console.log('ERROR', error))

    // let { data } = await axios.get(source)
    return { items: data }
  },
  components: {
    Content
  }
}
</script>

<style>
.items {
  display: grid;
	grid-template-columns: 22% 4% 74%;
	grid-template-rows: auto ;
	grid-template-areas:
	"header header header"
	"main main aside"
  "related .,"
	"footer footer footer";
}
</style>
