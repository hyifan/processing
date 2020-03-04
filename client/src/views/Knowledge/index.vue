<template>
  <div class="clearfix">
    <aside class="m-side-nav">
      <ul>
        <li><router-link to="/knowledge/gray">灰度图像</router-link></li>
        <li><router-link to="/knowledge/histogram">直方图均衡</router-link></li>
        <li><router-link to="/knowledge/space">简单空间域滤波器</router-link></li>
      </ul>
    </aside>
    <router-view></router-view>
  </div>
</template>