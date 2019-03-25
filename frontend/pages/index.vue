<template>
  <section class="container">
<ul>
  <li v-for="item in items">{{ item }}</li>
</ul>
    <article class="content">
      <header>Header Title
        <section class="path">tags</section>
        <section class="timestamp">2018</section>
      </header>
      <section class="main">
      <p>Don't need to worry about creating vue components right away.<br>
         Focus on creating the page to look the way you want it to.<br>
         All elements are optional<br>
       </p>
       <p>
         Need a grid? Add a grid. Grids are CSS properties applied to container elements.<br>
      </p>
      </section>
      <aside class="one-more-thing">Aside</aside>
      <section class="related">More Info</section>
      <footer>Footer</footer>
    </article>

  </section>
</template>

<script>
import AppLogo from '~/components/AppLogo.vue'
import axios from 'axios'
import router from 'vue-router'

console.log(router.currentRoute)

export default {
  async asyncData ({ params }) {
    let { data } = await axios.get(`http://localhost:8888/json-path/c/charles`)
    return { items: data }
  },
  components: {
    AppLogo
  }
}
</script>

<style>
.content {
  display: grid;
	grid-template-columns: 22% 4% 74%;
	grid-template-rows: auto ;
	grid-template-areas:
	"header header header"
	"main main aside"
  "related .,"
	"footer footer footer";
}
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
