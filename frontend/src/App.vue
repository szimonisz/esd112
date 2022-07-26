<template>
  <MyHeader/>
  <router-view />
</template>

<script>
import MyHeader from "./components/MyHeader";
export default {
  components: {
    MyHeader,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
