<template>
  <transition name="fade">
    <div v-if="show" class="toast" :class="{ 'error': error }">
      <slot>{{ message }}</slot>
    </div>
  </transition>
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
    },
    error: {
      type: Boolean,
      default: false
    }
  },
  watch: {
    show(val) {
      if (val) {
        setTimeout(() => {
          this.$emit('update:show', false)
        }, 3000)
      }
    }
  }
};
</script>

<style lang="scss">
.toast {
  width: 380px;
  position: fixed;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #edf2fc;
  border-radius: 4px;
  border: 1px solid #ebeef5;
  padding: 12px 18px;
  &.error {
    background-color: #fef0f0;
    color: #f56c6c;
    border-color: #eac6c6;
  }
  &.fade-enter-active, &.fade-leave-active {
    transition: opacity 0.5s;
  }
  &.fade-enter, &.fade-leave-to  {
    opacity: 0;
  }
  
}
</style>
