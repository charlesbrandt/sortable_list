<template>
  <section class="container">
    Icon: <app-typography-icon />
    <ul>
      <li v-for="item in items" :key="item" class="list-group-item">
        {{ item }}
      </li>
    </ul>
    <article class="content">
      <header>
        Header Title
        <section class="path">tags</section>
        <section class="timestamp">2018</section>
      </header>
      <section class="main">
        <p>
          Don't need to worry about creating vue components right away. Focus on
          creating the page to look the way you want it to. All elements are
          optional
        </p>
        <p>
          Need a grid? Add a grid. Grids are CSS properties applied to container
          elements.
        </p>
      </section>
      <aside class="one-more-thing">Aside</aside>
      <section class="related">More Info</section>
      <footer>Footer</footer>
    </article>
  </section>
</template>

<script>
// import axios from 'axios'
import AppTypographyIcon from '~/components/TypographyIcon.vue'

export default {
  components: { AppTypographyIcon }
  /*
  async asyncData({ params }) {
    const { data } = await axios.get(`http://localhost:8888/server-check`)
    return { items: data }
  }
  */
}
</script>

<style>
.content {
  display: grid;
  grid-template-columns: 22% 4% 74%;
  grid-template-rows: auto;
  grid-template-areas:
    'header header header'
    'main main aside'
    'related .,'
    'footer footer footer';
}
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; /* 1 */
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
