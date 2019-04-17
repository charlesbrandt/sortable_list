<template>
  <div class="font-item">
    <button @:click="$emit('move-item', index, 0)">
      <!-- <font-awesome-icon :icon="up" /> -->
      up
    </button>
    {{ index }}.
    <button @:click="$emit('move-item', index, -1)">
      <!-- <font-awesome-icon :icon="down" /> -->
      down
    </button>
    <link rel="stylesheet" :href="fontSource" />
    <div class="sample-text" :style="customStyle">
      <!-- <p>Files: {{ webfont.files }}</p> -->
      <slot>Sample Text</slot>
    </div>
    <div>{{ webfont.family }}</div>
  </div>
</template>

<script>
// https://github.com/benmosher/eslint-plugin-import/issues/751
// import * as FontAwesomeIcon from '@fortawesome/vue-fontawesome'
// import faAngleDoubleUp from '@fortawesome/fontawesome-free-solid/faAngleDoubleUp'
// import faAngleDoubleDown from '@fortawesome/fontawesome-free-solid/faAngleDoubleDown'

export default {
  components: {
    // FontAwesomeIcon
  },
  props: ['webfont', 'index', 'fontSize'],
  data() {
    return {}
  },

  computed: {
    // a computed getter
    fontSource: function() {
      // `this` points to the vm instance
      return (
        'https://fonts.googleapis.com/css?family=' +
        this.webfont.family.replace(' ', '+')
      )
    },
    customStyle: function() {
      const style =
        "font-family: '" +
        this.webfont.family +
        "', serif; font-size: " +
        this.fontSize +
        'pt;'
      // console.log(style)
      return style
    }
    /*
    up() {
      return faAngleDoubleUp
    },
    down() {
      return faAngleDoubleDown
    }
    */
  }
}
</script>
<style></style>
