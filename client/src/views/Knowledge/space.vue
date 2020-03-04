<template>
  <div class="m-side-content m-algorithm">
    <article>
      <h1>简单空间域滤波器</h1>
      <section>
        <h2>一、滤波器</h2>
        <h3>1、空间域滤波器</h3>
        <p>
          空间域指图像平面本身，这类图像处理方法直接操作图像中的像素。空间域滤波器包括平滑空间滤波器和锐化空间滤波器。
        </p>
        <h3>2、频率域滤波器</h3>
        <p>
          频率域的图像处理首先把一副图像变换到频率域，在频率域中进行处理，然后通过反变换把处理结果返回到空间域。频率域滤波器包括低通滤波器（平滑图像）和高通滤波器（锐化图像）。
        </p>
      </section>
      <section>
        <h2>二、平滑空间滤波器 —— 中值滤波器</h2>
        <p>中值滤波器使用一个像素邻域中的中值代替图像中的值，表达式如下：</p>
        <p class="text-formula">g(x,y) = median<sub>(x,y)∈S<sub>xy</sub></sub>f(x,y)</p>
        <p>中值滤波器的应用非常普遍，因为对于某些类型的随机噪声，它们能提供良好的去噪能力，且与相同尺寸的线性平滑滤波器相比，引起的模糊更少。</p>
        <h4>效果：</h4>
        <div class="example">
          <img src="@/assets/images/space/median_before.jpg" alt="图像处理前">
          <span>--- 变换 ---></span>
          <img src="@/assets/images/space/median_after.jpg" alt="图像处理后">
        </div>
      </section>
      <section>
        <h2>三、锐化空间滤波器 —— 拉普拉斯算子</h2>
        <h3>1、基础</h3>
        <p>
          锐化处理的主要目的是突出灰度的过渡部分。在逻辑上，我们得出锐化处理可由空间微分来实现。基本上，微分算子的响应强度与图像在用算子操作的这一点的突变程度成正比，这样，图像微分会增强边缘和其他突变（如噪声），削弱灰度变化缓慢的区域。
        </p>
        <p>一维函数 f(x) 的一阶微分的基本定义是差值：</p>
        <p class="text-formula">
          <span class="space-for">
            <span class="den den-short">
              <span class="top">∂f</span>
              <span class="bottom">∂x</span>
            </span>
            <span class="normal normal-short">= f(x+1) − f(x)</span>
          </span>
        </p>
        <p>二阶微分定义为如下差分：</p>
        <p class="text-formula">
          <span class="space-for">
            <span class="den den-long">
              <span class="top">∂<sup>2</sup>f</span>
              <span class="bottom">∂x<sup>2</sup></span>
            </span>
            <span class="normal normal-long">= f(x+1) + f(x−1) − 2f(x)</span>
          </span>
        </p>
        <p>从下图可以看出微分在图像边缘的变化情况：</p>
        <img src="@/assets/images/space/integral.png" alt="微分在图像边缘的变化情况" class="img-formula">
        <h3>2、拉普拉斯（Laplacian）算子</h3>
        <p>Laplacian算子使用二阶微分锐化图像。</p>
        <p>一个二维图像函数 f(x,y) 的拉普拉斯算子定义为：</p>
        <p class="text-formula">
          <span class="space-for">
            <span class="normal normal-left">∇<sup>2</sup>f =</span>
            <span class="den den-right1">
              <span class="top">∂<sup>2</sup>f</span>
              <span class="bottom">∂x<sup>2</sup></span>
            </span>
            <span class="normal" style="left: 211px;">+</span>
            <span class="den den-right2">
              <span class="top">∂<sup>2</sup>f</span>
              <span class="bottom">∂y<sup>2</sup></span>
            </span>
          </span>
        </p>
        <p class="no-indent">因为任意阶微分都是线性操作，所以拉普拉斯变换也是一个线性算子。为了以离散形式描述这一公式，在 x 方向上，有</p>
        <p class="text-formula">
          <span class="space-for">
            <span class="den den-long">
              <span class="top">∂<sup>2</sup>f</span>
              <span class="bottom">∂x<sup>2</sup></span>
            </span>
            <span class="normal normal-long">= f(x+1,y) + f(x−1,y) − 2f(x,y)</span>
          </span>
        </p>
        <p class="no-indent">在 y 方向上，有</p>
        <p class="text-formula">
          <span class="space-for">
            <span class="den den-long">
              <span class="top">∂<sup>2</sup>f</span>
              <span class="bottom">∂y<sup>2</sup></span>
            </span>
            <span class="normal normal-long">= f(x,y+1) + f(x,y−1) − 2f(x,y)</span>
          </span>
        </p>
        <p class="no-indent">所以，满足这三个公式的两个变量的离散拉普拉斯算子是</p>
        <p class="text-formula">
          <span class="first">
            ∇<sup>2</sup>f(x,y) = f(x+1,y) + f(x−1,y) + f(x,y+1) + f(x,y−1) − 4f(x,y)
          </span>(1)
        </p>
        <p class="no-indent">这个公式可以用图1(a)的滤波模板来实现。</p>
        <p>
          使用拉普拉斯算子将产生暗色背景中叠加有浅灰色边线和突变点的图像。将原图像和拉普拉斯图像叠加在一起的简单方法，可以复原背景特性并保持拉普拉斯锐化处理的效果。公式如下：
        </p>
        <p class="text-formula">g(x,y) = f(x,y) + c[∇<sup>2</sup>f(x,y)]</p>
        <p class="no-indent">
          式中，f(x,y) 和 g(x,y) 分别为输入图像和锐化后的图像，如果使用图1(a)或(b)的拉普拉斯滤波器，则常数 c = −1；如果使用图1(c)或(d)的拉普拉斯滤波器，则常数 c = 1（因为锐化的是输入图像的亮度区域，即使用(1)式后为负的像素点）
        </p>
        <figure>
          <img src="@/assets/images/space/easy.png" alt="拉普拉斯算子" class="img-formula">
          <figcaption>图1 (a)实现式(1)所用模板；(b)用于实现带有对角项的公式的扩展模板；(c)~(d)实践中常用的其他两个拉普拉斯实现</figcaption>
        </figure>
        <h4>效果：</h4>
        <img src="@/assets/images/space/laplacian_example.jpeg" alt="拉普拉斯算子锐化图像" width="800" class="img-formula">
      </section>
    </article>
  </div>
</template>
<style lang="scss" scoped>
.space-for {
  position: relative;
  width: 330px;
  height: 74px;
  display: inline-block;
  .normal, .den, .top, .bottom {
    position: absolute;
  }
  .normal {
    top: 21px;
  }
  .den {
    height: 100%;
    .top, .bottom {
      position: absolute;
      width: 40px;
    }
    .top {
      top: 0;
      border-bottom: 1px solid red;
    }
    .bottom {
      bottom: 0;
    }
  }
  .normal-long {
    width: 227px;
    right: 0;
  }
  .normal-short {
    width: 260px;
    right: 0;
  }
  .den-short {
    left: 100px;
  }
  .den-long {
    left: 60px;
  }
  .normal-left {
    width: 270px;
    left: 0;
  }
  .den-right1 {
    right: 165px;
  }
  .den-right2 {
    right: 100px;
  }
}
.after-for {
  position: relative;
  top: -30px;
}
</style>