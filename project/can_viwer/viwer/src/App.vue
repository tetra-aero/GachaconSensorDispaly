<template>
<div>
<simpleList></simpleList>
</div>
</template>

<script>
import simpleList from './components/simplelist30.vue'
export default {
  name: 'App',
  components: {
  simpleList,
  },
  setup(){
    return {

    }
  }
}
</script>

<style>
html,body{
margin:0;
height: 100%;
width: 100%;
overflow-x: hidden;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgb(255,75,0);
  margin-top: 0px;
  background: black;
  margin: 0;
  padding: 0;
}
</style>
