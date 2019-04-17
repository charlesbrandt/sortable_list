<template>
  <section class="container">
    <div>
      <input v-model="sample" placeholder="edit me" />
      <input v-model="font_size" placeholder="14" />
      <button @:click="onGetList">get</button>
      <textarea v-model="order" placeholder=""></textarea>
      <button @:click="onSetList">set</button>

      <draggable
        v-model="fonts"
        class="all-fonts"
        @start="drag = true"
        @end="drag = false"
      >
        <font-sample
          v-for="(webfont, index) in fonts"
          :key="webfont.family"
          :webfont="webfont"
          :index="index"
          :font_size="font_size"
          @:move-item="onMoveItem"
        >
          {{ sample }}
        </font-sample>
      </draggable>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import draggable from 'vuedraggable'
import FontSample from '~/components/FontSample.vue'
// import AppLogo from '~/components/AppLogo.vue'

// https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-an-object-in-javascript
function findFont(fontlist, name) {
  let i = fontlist.length
  while (i--) {
    console.log('Checking: ', fontlist[i].family, ' vs. ', name)
    if (fontlist[i].family === name) {
      const match = fontlist.splice(i, 1)
      return match[0]
    }
  }
  return false
}

export default {
  components: {
    draggable,
    FontSample
  },
  data() {
    return {
      loading: false,
      // the actual font objects
      fonts: [],
      // a list of just the font names, in the desired order
      order: [],

      // http://clagnut.com/blog/2380/
      // https://en.wikipedia.org/wiki/The_quick_brown_fox_jumps_over_the_lazy_dog
      // The quick brown fox jumps over the lazy dog
      sample: 'The five boxing wizards jump quickly.',
      font_size: '16',
      error: null
    }
  },

  created() {
    // fetch the data when the view is created and the data is
    // already being observed
    this.fetchData()
  },

  methods: {
    onMoveItem(index, destination) {
      // console.log(index, destination)
      const item = this.fonts.splice(index, 1)[0]
      this.fonts.splice(destination, 0, item)
      // console.log( this.fonts )
    },

    fetchData() {
      // console.log(this.post)
      this.loading = true
      axios
        .get(
          'https://www.googleapis.com/webfonts/v1/webfonts?key=AIzaSyBx7rQumhCDeLW9kdamvr82A6k3tA92a6Y'
        )
        .then(response => {
          this.loading = false
          // console.log(response)
          // full set:
          this.fonts = response.data.items
          // limited list:
          // this.fonts = response.data.items.slice(0, 10)
        })
        .catch(error => {
          this.error = error.toString()
        })
    },

    onGetList() {
      // console.log("made it to onGetList")
      let font
      // clear the array
      this.order = []
      for (let i = 0; i < this.fonts.length; i++) {
        font = this.fonts[i]
        this.order.push(font.family)
      }
      // console.log(this.order)
    },

    onSetList() {
      let curname
      let curfont = false
      let names
      if (!Array.isArray(this.order)) {
        names = this.order.split(',')
      } else {
        names = this.order
      }

      // console.log("made it to onGetList")
      const originalfonts = this.fonts
      // clear the font array
      this.fonts = []
      // console.log(original_fonts)
      for (let i = 0; i < names.length; i++) {
        curname = names[i]
        // console.log("original fonts length: ", original_fonts.length)
        curfont = findFont(originalfonts, curname)
        console.log(curfont)
        if (curfont) {
          this.fonts.push(curfont)
        }
      }
      // console.log(this.order)
    }
  }
}
</script>
<style>
.all-fonts {
  display: flex;
  flex-wrap: wrap;
}

.font-item {
  flex: 1 1 250px;
  margin-bottom: 10px;
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
