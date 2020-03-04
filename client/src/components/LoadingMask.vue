<template>
  <div class="loading-mask" v-show="show">
    <span class="msg" v-if="message">{{ message }}</span>
    <span class="msg" v-else>
      <svg class="load" viewBox="25 25 50 50">
        <circle class="loading" cx="50" cy="50" r="20" fill="none" />
      </svg>
    </span>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped lang="scss">
@keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 130, 200;
    stroke-dashoffset: -50;
  }
  100% {
    stroke-dasharray: 130, 200;
    stroke-dashoffset: -188;
  }
}
.loading-mask {
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 1000;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  .msg {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    font-size: 30px;
  }
  .load {
    width: 50px;
    height: 50px;
  }
  .loading {
    stroke: #42b983;
    stroke-width: 3;
    fill: none;
    animation: dash 1.5s linear infinite;
  }
}
</style>
