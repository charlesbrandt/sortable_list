<template>
  <section class="container">
    <svg-base width="11in" height="8.5in" icon-name="write">
      <g-3x3x4 /><icon-write />
    </svg-base>
  </section>
</template>

<script>
// import axios from 'axios'
import SvgBase from '~/components/svg/Base.vue'
import IconWrite from '~/components/svg/IconWrite.vue'
import G3x3x4 from '~/components/svg/3x1/3x3x4.vue'
export default {
  components: {
    SvgBase,
    IconWrite,
    G3x3x4
  }
}
</script>
<style>
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
