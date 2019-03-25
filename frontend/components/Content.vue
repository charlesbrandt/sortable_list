<template>
  <div v-bind:data-id="item.name" class="content item">
    <!-- <p>item: {{ item }}</p> -->
    <!-- <p>THumb: {{ item.thumb }}</p> -->
    <div v-if="item.thumb" class="thumbnail">
      <img v-bind:src="imagePath" class="content">
    </div>
    <div v-else>
      {{ item.name.replace('_', ' ') }}
    </div>

    <div class="guide">
      <img src="/img/guide.png" class="content">

      <div class="handle">
        <!-- handle -->
      </div>

    </div>

  </div>
</template>

<script>
export default {
  props: [
    'item'
  ],
  computed: {
    // a computed getter
    imagePath: function () {
      // `this` points to the vm instance
      return "http://localhost:8888/image/" + this.item.thumb
    }
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

.guide {
    position: absolute;
    top: 0;
    left: 0;
    text-align: left;
    opacity: 0;
}

.guide:hover {
    opacity: .25;
}

.handle {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 50%;
    text-align: left;
}

.modal {
    position: absolute;
    top: 50%;
    left: 0;
    width: 50%;
    height: 50%;
    text-align: left;
}

.follow {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 50%;
    height: 50%;
    text-align: left;
}


.sortable-chosen {
    /* width: 200px;
    display: block; */
}

.sortable-ghost {
    opacity: .2;
}



</style>
