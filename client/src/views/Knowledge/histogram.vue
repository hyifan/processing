<template>
  <div class="m-side-content m-algorithm">
    <article>
      <h1>直方图均衡</h1>
      <section>
        <h2>一、灰度图像直方图均衡</h2>
        <h3>1、直方图</h3>
        <p>灰度级范围为 [0,L-1] 的数字图像的直方图是离散函数 h(r<sub>k</sub>)=n<sub>k</sub>，其中 r<sub>k</sub> 是第k级灰度值，n<sub>k</sub> 是图像中灰度为 r<sub>k</sub> 的像素个数。在实践中，经常用乘积 MN 表示的图像总像素除每个分量来归一化直方图，通常 M 和 N 是图像的行数和列数。因此，归一化后的直方图由下式给出，其中 k=0,1,...,L-1，归一化直方图的所有分量之和应等于1。</p>
        <p class="text-formula">
          <span class="histogram-for">
            <span class="normal">p(r<sub>k</sub>) = </span>
            <span class="top">n<sub>k</sub></span>
            <span class="bottom">MN</span>
          </span>
        </p>
        <p>
          直观上，可以得出这样的结论：若一幅图像的像素倾向于占据整个可能的灰度级并且分布均匀，则该图像会有高对比度的外观并展示灰色调的较大变换。最终效果将是一幅灰度细节丰富且动态范围较大的图像。为实现该效果，我们需要一个变换函数，将输入图像直方图信息进行变换，得到均匀分布的图像。
        </p>
        <img src="@/assets/images/histogram/pic.png" alt="直方图" class="img-formula">
        <h3>2、变换函数应满足条件</h3>
        <p>
          考虑连续灰度值，并用变量 r 表示待处理图像的灰度。通常，我们假设 r 的取值区间为 [0,L-1]，且 r=0 表示黑色，r=L-1 表示白色。在 r 满足这些条件的情况下，我们将注意力集中到变换函数
        </p>
        <p class="text-formula"><span class="first">s = T(r)</span>0≤r≤L−1</p>
        <p class="no-indent">
          上，对于输入图像中每个具有 r 值的像素产生一个输出灰度值 s。为了实现变换后的灰度值均匀分布的效果，变换函数需满足以下条件：
        </p>
        <p class="no-indent">(a) T(r) 在区间 [0,L-1] 上为单调递增函数；</p>
        <p class="no-indent">(b) 当 0≤r≤L-1 时，0≤T(r)≤L−1，且 T(r) 均匀分布。</p>
        <p>为了能用反函数</p>
        <p class="text-formula"><span class="first">r = T<sup>−1</sup>(s)</span>0≤s≤L−1</p>
        <p class="no-indent">计算原色图像，在这种情况下，条件(a)改为：(a`) T(r) 在区间 [0,L-1] 上为严格单调递增函数。</p>
        <div class="prove">
          <h4>证明：</h4>
          <p>(a) 要求 T(r) 单调递增，可保持原来输入值大小关系不变，即无论如何映射，较亮区域依然亮，较暗区域依然暗。</p>
          <p>(b) 保证输出灰度值的范围与输入灰度值的范围相同，且变换后的灰度值需均匀分布。</p>
          <p>(a`) 要求 T(r) 严格单调递增，可保证从 s 到 r 的反映射是一对一的，防止出现二义性。</p>
        </div>
        <h3>3、变换函数</h3>
        <p>
          一幅图像的灰度级可视为区间[0,L-1]内的随机变量。随机变量的基本描述子是其概率密度函数(PDF)。令 p<sub>r</sub>(r) 和 p<sub>s</sub>(s) 分别表示随机变量 r 和 s 的概率密度函数，其中 p 的下标用于指示 p<sub>r</sub>(r) 和 p<sub>s</sub>(s) 是不同的函数。
        </p>
        <p>在图像处理中，特别重要的变换函数有如下形式：</p>
        <p class="text-formula">
          <span class="first">
            s = T(r) = (L−1)
            <i style="font-size: 30px;">∫</i>
            <sup style="position: relative; top: -10px;">r</sup>
            <sub style="position: relative; left: -6px;">0</sub>
            p<sub>r</sub>(w)dw
          </span>(1)
        </p>
        <p class="no-indent">式中，w 是积分的假变量。该公式满足上述条件(a`)(b)。</p>
        <h3>4、直方图均衡</h3>
        <p>
          对于离散值，我们处理其概率与求和来代替处理概率密度函数与积分。如前所述，一幅数字图像中灰度级 r<sub>k</sub> 出现的概率近似为
        </p>
        <p class="text-formula clearfix">
          <span class="first histogram-for">
            <span class="normal">p<sub>r</sub>(r<sub>k</sub>) = </span>
            <span class="top">n<sub>k</sub></span>
            <span class="bottom">MN</span>
          </span>
          <span class="after-for">k=0,1,...,L−1</span>
        </p>
        <p class="no-indent">代入式 (1) 可得离散形式为</p>
        <img src="@/assets/images/histogram/discrete.jpg" alt="离散形式公式" class="img-formula" width="600">
        <p class="no-indent">
          通过计算上式，即可实现直方图均衡化。均衡后的图像的灰度级会跨越更宽的灰度级范围，最终结果是增强来对比度。
        </p>
      </section>
      <section>
        <h2>二、彩色图像直方图均衡</h2>
        <p>
          如果单独对RGB彩色空间的各个分量进行直方图均衡，将产生不正确的彩色。一种更合乎逻辑的方法是，均匀地展开这种彩色灰度，而保持彩色本身（即色调）不变。HSV 彩色空间是适合这种方法的理想空间，即只对 V 分量进行均衡化。
        </p>
      </section>
    </article>
  </div>
</template>
<style lang="scss" scoped>
.histogram-for {
  position: relative;
  width: 120px;
  height: 74px;
  display: inline-block;
  .normal, .top, .bottom {
    position: absolute;
  }
  .normal {
    width: 60px;
    left: 0px;
    top: 21px;
  }
  .top, .bottom {
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
.after-for {
  position: relative;
  top: -30px;
}
</style>