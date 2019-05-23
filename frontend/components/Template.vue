<template>
  <div :data-id="item.name" class="content item">
    <!--
    https://vuejs.org/v2/guide/components-slots.html
    -->
    <slot />
  </div>
</template>

<script>
export default {
  props: ['item'],
  computed: {
  }
}
</script>

<style>
.content {
  position: relative;
  text-align: left;
  display: inline-block;
  margin: 0;
  width: 150px;
  height: 150px;
  vertical-align: top;
  /*width:500px;
  margin-left:auto;
  margin-right:auto;
  margin-top: 50;
  margin-bottom: 50;
  float: left;
  */
}
</style>
