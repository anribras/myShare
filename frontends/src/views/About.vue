<template>
  <div class="about">
    <h1>This is an about page</h1>
    <router-link to="/about/u/1/p/2">u1p2</router-link>
    <div></div>
    <router-link to="/about/u/3/p/4">u3p4</router-link>
    <router-view name="userView"></router-view>
    <router-view name="profileView"></router-view>
  </div>
</template>
