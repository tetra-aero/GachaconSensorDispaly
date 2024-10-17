<template>
  <div class="wrapper30">
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <template v-for="(item,index) in dataFromServer" :key="index">
       
        <dispNumber :label="item.title ||'none'" :number="item.data || 'none'" :unit="item.unit || 'mA'"></dispNumber>
    </template>
  </div>
</template>

<script>
import { computed ,onMounted , onBeforeUnmount } from "vue";
import { useStore } from 'vuex';
import dispNumber  from "@/components/number.vue";
export default{
  name:"simpleList",
  components:{
    dispNumber,
  },
  setup() {
    const store = useStore();
//         {
//             "title": "LABEL",
//             "data": "5017",
//         "unit":"V"
//     },
//         {
//             "title": "Title_2",
//             "data": "4922",
//         "unit":"m"
//     },
//         {
//             "title": "Title_3",
//             "data": "7137",
//         "unit":"mA"
//     },
//         {
//             "title": "Title_4",
//             "data": "4510"
//     },
//     {
//         "title": "Title_5",
//         "data": "9243"
//     },
//     {
//         "title": "Title_6",
//         "data": "2721"
//     },
//     {
//         "title": "Title_7",
//         "data": "5060"
//     },
//     {
//         "title": "Title_8",
//         "data": "1124"
//     },
//     {
//         "title": "Title_9",
//         "data": "7481"
//     },
//     {
//         "title": "Title_10",
//         "data": "8778"
//     },
//     {
//         "title": "Title_11",
//         "data": "6286"
//     },
//     {
//         "title": "Title_12",
//         "data": "6242"
//     },
//     {
//         "title": "Title_13",
//         "data": "3850"
//     },
//     {
//         "title": "Title_14",
//         "data": "8547"
//     },
//     {
//         "title": "Title_15",
//         "data": "2718"
//     },
//     {
//         "title": "Title_16",
//         "data": "6315"
//     },
//     {
//         "title": "Title_17",
//         "data": "3993"
//     },
//     {
//         "title": "Title_18",
//         "data": "1070"
//     },
//     {
//         "title": "Title_19",
//         "data": "5174"
//     },
//     {
//         "title": "Title_20",
//         "data": "4678"
//     },
//     {
//         "title": "Title_21",
//         "data": "4977"
//     },
//     {
//         "title": "Title_22",
//         "data": "9701"
//     },
//     {
//         "title": "Title_23",
//         "data": "3387"
//     },
//     {
//         "title": "Title_24",
//         "data": "5873"
//     },
//     {
//         "title": "Title_25",
//         "data": "4601"
//     },
//     {
//         "title": "Title_26",
//         "data": "3311"
//     },
//     {
//         "title": "Title_27",
//         "data": "4006"
//     },

// ];
const dataFromServer = computed(() => store.state.dataFromServer);
const errorMessage = computed(() => store.state.errorMessage);
const fetchData = () => {
        store.dispatch('fetchData');
    };

let interval
//ライフサイクルフック
    onMounted(() => {
        fetchData();
        interval = setInterval(() => {
            fetchData();
        }, 1000);  // 1秒ごとにデータを取得
    });
    onBeforeUnmount(() => {
        clearInterval(interval);  // コンポーネントが破棄される前に interval をクリア
      });
return{
  dataFromServer,
  errorMessage
};
  }
}
</script>
<style scoped>
.wrapper30{
    border: 20px ridge rgb(0, 175, 122);
    padding:10px;
    width: 100%;
    height: 100vh;
    gap: 10px;
    margin: 0;
    display: grid;
    box-sizing:border-box;
    /* 列設定 余白（gap:10px*6)を引いて等分する*/
    grid-template-columns: repeat(7, calc(calc(100% - 60px) /7));
    /* 行設定 余白（border:20px*2 gap:10px*5 padding:10px*2)を引いて等分する*/
    grid-template-rows: repeat(7, calc(calc(100vh - 110px) / 7));
}
</style>