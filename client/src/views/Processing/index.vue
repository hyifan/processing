<template>
  <div class="m-main-content">
    <form @submit.prevent.stop @submit="checkForm" class="form clearfix">
      <fieldset class="item">
        <legend>图像处理方式</legend>
        
        <input type="radio" id="gray" value="gray" v-model="type">
        <label for="gray">灰度图像</label>
        
        <input type="radio" id="translate" value="translate" v-model="type">
        <label for="translate">图像反转</label>
        
        <input type="radio" id="log" value="log" v-model="type">
        <label for="log">对数变换</label>
        
        <input type="radio" id="gama" value="gama" v-model="type">
        <label for="gama">伽马变换</label>
        
        <input type="radio" id="histogram" value="histogram" v-model="type">
        <label for="histogram">直方图均衡</label>
        
        <input type="radio" id="median" value="median" v-model="type">
        <label for="median">中值滤波器</label>
        
        <input type="radio" id="laplacian" value="laplacian" v-model="type">
        <label for="laplacian">Laplacian算子</label>
      </fieldset>
      
      <fieldset class="item">
        <legend>RGB参数</legend>
        <input type="number" placeholder="Red" v-model="gray.red" :disabled="type !== 'gray'" :required="type === 'gray'">
        <input type="number" placeholder="Green" v-model="gray.green" :disabled="type !== 'gray'" :required="type === 'gray'">
        <input type="number" placeholder="Blue" v-model="gray.blue" :disabled="type !== 'gray'" :required="type === 'gray'">
      </fieldset>
      
      <fieldset class="item">
        <legend>对数变换参数</legend>
        <input type="number" placeholder="c" v-model="log.c" :disabled="type !== 'log'" :required="type === 'log'">
        <input type="number" placeholder="v" v-model="log.v" :disabled="type !== 'log'" :required="type === 'log'">
      </fieldset>
      
      <fieldset class="item">
        <legend>伽马参数</legend>
        <input type="number" placeholder="gama" v-model="gama" :disabled="type !== 'gama'" :required="type === 'gama'">
      </fieldset>
      
      <fieldset class="item">
        <legend>图像类型</legend>
        
        <input type="radio" id="simple" value="simple" v-model="style" :disabled="['translate', 'log', 'gama', 'histogram'].indexOf(type) < 0">
        <label for="simple">黑白</label>
        
        <input type="radio" id="color" value="color" v-model="style" :disabled="['translate', 'log', 'gama', 'histogram'].indexOf(type) < 0">
        <label for="color">彩色</label>
      </fieldset>
      
      <fieldset class="item">
        <legend>上传图片</legend>
        <input type="file" accept="image/*" ref="pic" multiple>
      </fieldset>

      <button type="submit" class="btn">提交</button>
    </form>
    <div class="main clearfix">
      <div class="item" v-for="(url, index) in urls" :key="url">
        <img :data-src="url" :src="url" v-if="index < 9">
        <img :data-src="url" v-else>
      </div>
    </div>
    <toast-message
      :show.sync="showErrorToast"
      :message="message"
      error
    ></toast-message>
  </div>
</template>

<script>
import ToastMessage from '@/components/ToastMessage.vue'

export default {
  data() {
    return {
      showErrorToast: false,
      message: '',
      type: 'median',
      style: 'simple',
      gray: {
        red: undefined,
        green: undefined,
        blue: undefined
      },
      log: {
        c: '',
        v: ''
      },
      gama: '',
      urls: []
    }
  },
  methods: {
    checkForm() {
      if (this.$refs.pic.files.length === 0) {
        this.showErrorToast = true
        this.message = '请选择图片'
        return
      }
      this.save()
    },
    save() {
      const formData = new FormData()
      this.$refs.pic.files.forEach(async (file) => {
        formData.append('file', file)
        // const res = await this.readImage(file)
        // console.log('大小：', (file.size / 1024).toFixed(2), 'kb', '尺寸：', res.width, '*', res.height)
      });
      ['type', 'style'].forEach(key => {
        formData.append(key, this[key])
      })
      if (this.type === 'gray') {
        const all = Number(this.gray.red) + Number(this.gray.green) + Number(this.gray.blue)
        const red = Number(this.gray.red) / all
        const green = Number(this.gray.green) / all
        const blue = 1 - red - green
        formData.append('red', red)
        formData.append('green', green)
        formData.append('blue', blue)
      }
      if (this.type === 'log') {
        formData.append('logC', this.log.c)
        formData.append('logV', this.log.v)
      }
      if (this.type === 'gama') {
        formData.append('gama', this.gama)
      }
      this.$api.base.upload(formData).then(res => {
        const urls = []
        res.data.urls.forEach(val => {
          urls.push('/image/' + val)
        })
        this.urls = urls
        this.loadImg()
      })
    },
    loadImg() {
      let nowShowImgNum = 9 // 存储已加载图片数量
      function lazyload() {
        const clientHeight = document.documentElement.clientHeight // 屏幕可见区域高度
        const scrollTop = document.documentElement.scrollTop || document.body.scrollTop // 滚动条距离顶部高度，即浏览器窗口顶部与文档顶部之间的距离
        const images = document.getElementsByTagName('img')
        for (let i = nowShowImgNum || 9; i < images.length; i++) {
          const img = images[i]
          const elementTop = img.offsetTop // 元素相对于文档顶部的高度
          if (elementTop < clientHeight + scrollTop + 300) {
            // 元素即将进入可视区域以上
            if (!img.getAttribute('src')) {
              img.src = img.getAttribute('data-src')
            }
            nowShowImgNum = i + 1
          }
        }
      }
      let timer = null // 设置定时器
      let startTime = Date.now() // 上次滚动停止时间
      window.addEventListener('scroll', function() {
        const delay = 1000
        const curTime = Date.now() // 当前时间
        const remaining = delay - (curTime - startTime)
        clearTimeout(timer)
        if (remaining <= 0) {
          lazyload()
          startTime = Date.now()
        } else {
          timer = setTimeout(lazyload, remaining)
        }
      })
    },
    readImage(file) {
      return new Promise(function(resolve) {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = function(theFile) {
          const image = new Image()
          image.src = theFile.target.result
          image.onload = function() {
            const width = this.width
            const height = this.height
            resolve({ width, height })
          }
        }
      })
    }
  },
  components: {
    ToastMessage
  }
}
</script>

<style lang="scss" scoped>
.form {
  legend {
    float: left;
    width: 110px;
    text-align: right;
    margin-right: 30px;
  }
  .btn {
    margin-left: 140px;
  }
  .item {
    margin: 30px 0;
  }
  input[type='text'], [type='number'] {
    margin-right: 20px;
    &[disabled] {
      background-color: #f5f7fa;
      border-color: #e4e7ed;
      cursor: not-allowed;
    }
  }
  input[type='radio'] {
    margin-left: 20px;
    &:nth-of-type(1) {
      margin-left: 0;
    }
    &[disabled] {
      cursor: not-allowed;
    }
  }
}

.main {
  width: 100%;
  margin-top: 50px;
  .item {
    width: 350px;
    height: 300px;
    float: left;
    margin: 25px;
    img {
      width: 100%;
      height: 100%;
    }
  }
}

</style>
