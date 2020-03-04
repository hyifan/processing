<template>
  <div class="m-side-content m-algorithm">
    <article>
      <h1>灰度图像</h1>
      <section>
        <h2>一、RGB彩色模型</h2>
        <p>
          在RGB模型中，每种颜色出现在红(Red)、绿(Green)、蓝(Blue)的原色光谱成分中。该模型基于笛卡儿坐标系。在RGB彩色模型中表示的图像由3个分量图像组成，每种原色一幅分量图像。当送入RGB监视器时，这3幅图像在屏幕上混合生成一幅合成的彩色图像。
        </p>
        <p>
          见下图，为方便起见，假定所有颜色值均已归一化，即R、G和B的所有值都在区间[0,1]中。0表示不发光，1表示完全发光。以(1,0,0)为例，R为1即完全发光，G与B为0即不发光，最终颜色为红色；以(1,1,0)为例，R与G为1即完全发光，B为0即不发光，即红色跟绿色完全发光，蓝色不发光，最终颜色为黄色。
        </p>
        <img src="@/assets/images/gray/color.png" alt="彩色模型" class="img-formula">
      </section>
      <section>
        <h2>二、RGB转灰度图像</h2>
        <p>
          没有颜色的光称为单色光或无色光。单色光的唯一属性是其强度或大小。因为感知单色光的强度从黑色到灰色变化，最后到白色，灰度级一次通常用来表示单色光的强度。从黑到白的单色光的度量值范围通常称为灰度级，而单色图像通常称为灰度图像。
        </p>
        <p>使用不同的算法，会得到不同的灰度图像，例如若要查看红色在图像的分布情况，可使用：</p>
        <p class="text-formula">Gray = 1 × R + 0 × G + 0 × B</p>
        <p>从上式可知，选择不同的系数，可得到不同的灰度图像，目前常使用下面的一个心理学公式：</p>
        <p class="text-formula">Gray = 0.299 × R + 0.587 × G + 0.114 × B</p>
      </section>
      <section>
        <h2>三、一些基本的灰度变换函数</h2>
        <h3>1、图像反转</h3>
        <p>使用下图所示的反转变换，可得到灰度级范围为 [0,L−1] 的一副图像的反转图像。</p>
        <img src="@/assets/images/gray/translate.png" alt="图像反转" class="img-formula">
        <h4>效果：</h4>
        <div class="example">
          <img src="@/assets/images/gray/translate_before.png" alt="图像反转前">
          <span>--- 变换 ---></span>
          <img src="@/assets/images/gray/translate_after.png" alt="图像反转后">
        </div>
        <h3>2、对数变换</h3>
        <p>对数变换的通用形式为</p>
        <p class="text-formula">s = c log(1+vr)</p>
        <p>
          式中 c 是常数，并假设 r≥0。图中对数曲线的形状表明，该变换将输入中范围较窄的低灰度值映射为输出中范围较宽的灰度值，或将输入中范围较宽的高灰度值映射为输出中范围较窄的灰度值。我们使用这种类型的变换来扩展图像中的暗像素值，同时压缩更高灰度级的值。反对数变换的作用与此相反。
        </p>
        <img src="@/assets/images/gray/log.png" alt="对数变换" class="img-formula">
        <h4>效果：</h4>
        <div class="example">
          <img src="@/assets/images/gray/log_before.png" alt="图像反转前">
          <span>--- 变换 ---></span>
          <img src="@/assets/images/gray/log_after.png" alt="图像反转后">
        </div>
        <h3>3、幂律（伽马）变换</h3>
        <p>幂律变换的基本形式为</p>
        <p class="text-formula">s = cr<sup>γ</sup></p>
        <p>式中 c 和 γ 为正常数。图像如下图所示。</p>
        <img src="@/assets/images/gray/gama.png" alt="幂律（伽马）变换" class="img-formula">
        <h4>效果：</h4>
        <div class="example">
          <img src="@/assets/images/gray/gama_before.png" alt="图像反转前">
          <span>--- 变换 ---></span>
          <img src="@/assets/images/gray/gama_after.png" alt="图像反转后">
        </div>
      </section>
    </article>
  </div>
</template>