<template>
  <div v-if="show" class="modal-dialog">
    <div class="content" :style="contentStyle">
      <header v-if="!hideHeader" class="clearfix">
        <span class="title">{{ title }}</span>
        <slot name="header"></slot>
        <span v-if="!noClose" class="i-close" @click="closeModal">x</span>
      </header>
      <main>
        <slot></slot>
      </main>
      <footer v-if="!hideFooter" class="clearfix">
        <slot name="footer"></slot>
        <button v-if="!noCancel" class="btn-right" @click="closeModal">取消</button>
      </footer>
    </div>
    <div class="mask"></div>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      default: false
    },
    hideHeader: {
      type: Boolean,
      default: false
    },
    hideFooter: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ''
    },
    noClose: {
      type: Boolean,
      default: false
    },
    noCancel: {
      type: Boolean,
      default: false
    },
    contentStyle: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  data() {
    return {
    }
  },
  methods: {
    closeModal() {
      this.$emit('update:show', false)
    }
  }
}
</script>

<style lang="scss">
.modal-dialog {
  .content {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 101;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 1px 3px rgba(0,0,0,.3);
  }
  header {
    padding: 12px;
    .i-close {
      float: right;
      color: #909399;
      transform: scale(1, 0.9);
      cursor: pointer;
    }
  }
  footer {
    padding: 12px 0;
    width: 100%;
    position: absolute;
    bottom: 0;
    .btn-right {
      margin-right: 12px;
      float: right;
    }
  }
  main {
    padding: 12px;
  }
  .mask {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 100;
    width: 100%;
    height: 100%;
    opacity: .5;
    background: #000;
  }
}
</style>
