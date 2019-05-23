<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    :width="width"
    :height="height"
    viewBox="0 0 1056 816"
    :aria-labelledby="svgName"
    role="presentation"
  >
    <title :id="svgName" lang="en">{{ svgName }} svg</title>
    <g :fill="svgBaseColor">
      <slot />
    </g>
  </svg>
</template>

<script>
export default {
  props: {
    svgName: {
      type: String,
      default: 'grid'
    },
    width: {
      type: [Number, String],
      default: '11in'
    },
    height: {
      type: [Number, String],
      default: '8.5in'
    },
    svgBaseColor: {
      type: String,
      default: 'currentColor'
    }
  }
}
</script>

<style scoped>
svg {
  display: inline-block;
  vertical-align: baseline;
  margin-bottom: -2px; /* yes, I'm that particular about formatting */
}
</style>
