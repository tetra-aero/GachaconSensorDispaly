<template>
  <div class="number">
    <h1>{{label}}</h1>
    <p class="data">{{ number }}<span>{{ unit }}</span></p>
  </div>
</template>

<script>
export default{
  name:"dispNumber",
  props:{
    label: {
      type: String,
      required:true,
    },
    number:{
      type: String,
      required:true,
    },
    unit:{
      type:String,
      required:false
    }
  }
}
</script>
<style scoped>
.number{
  display: block;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  background-color:rgb(200,200,203);
  border: 8px outset rgb(132,145,158);
  container-type: size;
  padding: 0.5em;
  margin: 0;
  position: relative;
}
h1{
  /* ラベル */
  padding:0;
  margin: 0;
  font-size: 1rem;
  text-align: left;
  position: absolute;
  top: 1px;
  left: 1px;
  @container (width > 300px){
    font-size: 1.6rem;
    font-weight: normal;
  }
}
p.data{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateY(-50%) translateX(-50%);
  font-size: 2rem;
  margin: 0;
  @container (width > 300px){
    font-size: 5rem;
    font-weight: bold;
  }
}
.data>span{
  position: absolute;
  bottom: 0;
  font-size: 1rem;
  @container (width > 300px){
    font-size: 2rem;
    font-weight: bold;
    text-indent: 1rem;
  }
}

</style>