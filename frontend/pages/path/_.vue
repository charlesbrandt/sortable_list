<template>
  <section class="container">
    <ul>
      <p>{{ path() }}</p>

      <!--
      <li v-for="item in items">
        <content :item="item"/>
      </li>
      -->

      <draggable
        v-model="items"
        group="directory"
        :move="onMove"
        @start="drag = true"
        @end="save"
      >
        <!--
        <div v-for="element in myArray" :key="element.id">{{element.name}}</div>
        -->

        <Content v-for="item in items" :key="item.name" :item="item"></Content>
      </draggable>
    </ul>
  </section>
</template>

<script>
import axios from 'axios'
import draggable from 'vuedraggable'
import Content from '~/components/Content.vue'
// import router from 'vue-router'

// console.log(router.currentRoute)
// console.log(params)

// https://github.com/David-Desmaisons/draggable-example/blob/master/src/components/Hello.vue
// this is a good source of information

export default {
  components: {
    draggable,
    Content
  },
  data() {
    return {
      items: null,
      loading: true,
      errored: false,
      showModal: false
    }
  },

  // this is the vue approach
  // https://vuejs.org/v2/cookbook/using-axios-to-consume-apis.html
  // has access to context
  // but what about getting the route?
  /*
  mounted() {
    axios
      .get('https://api.coindesk.com/v1/bpi/currentprice.json')
      .then((response) => {
        this.items = response.data.bpi
      })
      .catch((error) => {
        console.log(error)
        this.errored = true
      })
      .finally(() => (this.loading = false))
  },
  */
  computed: {},
  // this is the nuxt approach:
  // https://nuxtjs.org/guide/async-data/
  async asyncData({ params, error }) {
    // https://nuxtjs.org/guide/routing/#unknown-dynamic-nested-routes
    // console.log('params', params)
    // let path = params.pathMatch
    const source = `http://localhost:8888/json-path/${params.pathMatch}`
    let data
    await axios
      .get(source)
      .then((response) => (data = response.data))
      // .catch((error) => error({ statusCode: 404, message: 'Post not found' }))
      .catch((error) => console.log('ERROR', error))

    // console.log('source', source)
    // let { data } = await axios.get(source)
    return { items: data }
  },

  methods: {
    path() {
      return this.$nuxt.$route.params.pathMatch
    },
    save({ params }) {
      // console.log('Saved!')
      this.drag = false
      // console.log(this.items)
      // const order = this.items.toArray()
      // console.log(order);
      // localStorage.setItem(sortable.options.group.name, order.join('|'));
      // let result = ''
      let item
      const names = []
      for (let i = 0; i < this.items.length; i++) {
        item = this.items[i].name
        // result += item + '\n'
        names.push(item)
      }
      console.log(names)
      // this does NOT WORK!!!
      // frequently bitten by this for construct... bah
      // for (var item in order) {
      //   console.log(item);
      //   result += item + '\n';
      // }

      // const data = { content: result, format: 'list' }
      // const data = { content: names, format: 'list' }
      // https://developer.mozilla.org/en-US/docs/Web/API/FormData
      const formData = new FormData()
      formData.append('content', names)
      formData.append('format', 'list')
      // do the ajax POST now
      const url = 'http://localhost:8888/save/' + this.path()
      // console.log(url);
      // console.log(data);
      // callback = function () {};
      axios.post(url, formData)
      // console.log(order);
    },
    onMove({ relatedContext, draggedContext }) {
      // console.log('Moved!')
      const relatedElement = relatedContext.element
      const draggedElement = draggedContext.element
      return (!relatedElement || !relatedElement.fixed) && !draggedElement.fixed
    }
  }
}
</script>

<style>
.items {
  display: grid;
  grid-template-columns: 22% 4% 74%;
  grid-template-rows: auto;
  grid-template-areas:
    'header header header'
    'main main aside'
    'related .,'
    'footer footer footer';
}
</style>
