<template>
  <div class="wrapper100">
    <template v-for="(item,index) in items" :key="index">
      <dispNumber :label="item.title ||'none'" :number="item.data || 'none'" :unit="item.unit || 'mA'"></dispNumber>
    </template>
  </div>
</template>

<script>
import dispNumber  from "@/components/number.vue";
export default{
  name:"simpleList",
  components:{
    dispNumber,
  },
  setup() {
    const items= [
    {
        "title": "LABEL",
        "data": "5017",
        "unit":"mV"
    },
    {
        "title": "Label_2",
        "data": "4922",
        "unit":"m"
    },
    {
        "title": "Label_3",
        "data": "7137",
        "unit":"m"
    },
    {
        "title": "Label_4",
        "data": "4510",
        "unit":"m"
    },
    {
        "title": "Label_5",
        "data": "9243",
        "unit":"m"
    },
    {
        "title": "Label_6",
        "data": "2721",
        "unit":"m"
    },
    {
        "title": "Label_7",
        "data": "5060",
        "unit":"m"
    },
    {
        "title": "Label_8",
        "data": "1124",
        "unit":"m"
    },
    {
        "title": "Label_9",
        "data": "7481",
        "unit":"m"
    },
    {
        "title": "Label_10",
        "data": "8778",
        "unit":"m"
    },
    {
        "title": "Label_11",
        "data": "6286"
    },
    {
        "title": "Label_12",
        "data": "6242"
    },
    {
        "title": "Label_13",
        "data": "3850"
    },
    {
        "title": "Label_14",
        "data": "8547"
    },
    {
        "title": "Label_15",
        "data": "2718"
    },
    {
        "title": "Label_16",
        "data": "6315"
    },
    {
        "title": "Label_17",
        "data": "3993"
    },
    {
        "title": "Label_18",
        "data": "1070"
    },
    {
        "title": "Label_19",
        "data": "5174"
    },
    {
        "title": "Label_20",
        "data": "4678"
    },
    {
        "title": "Label_21",
        "data": "4977"
    },
    {
        "title": "Label_22",
        "data": "9701"
    },
    {
        "title": "Label_23",
        "data": "3387"
    },
    {
        "title": "Label_24",
        "data": "5873"
    },
    {
        "title": "Label_25",
        "data": "4601"
    },
    {
        "title": "Label_26",
        "data": "3311"
    },
    {
        "title": "Label_27",
        "data": "4006"
    },
    {
        "title": "Label_28",
        "data": "7793"
    },
    {
        "title": "Label_29",
        "data": "3950"
    },
    {
        "title": "Label_30",
        "data": "9564"
    },{
        "title": "Label_31",
        "data": "5123"
    },
    {
        "title": "Label_32",
        "data": "6734"
    },
    {
        "title": "Label_33",
        "data": "2134"
    },
    {
        "title": "Label_34",
        "data": "8765"
    },
    {
        "title": "Label_35",
        "data": "3456"
    },
    {
        "title": "Label_36",
        "data": "9876"
    },
    {
        "title": "Label_37",
        "data": "2345"
    },
    {
        "title": "Label_38",
        "data": "6543"
    },
    {
        "title": "Label_39",
        "data": "4321"
    },
    {
        "title": "Label_40",
        "data": "6789"
    },
    {
        "title": "Label_41",
        "data": "8762"
    },
    {
        "title": "Label_42",
        "data": "9861"
    },
    {
        "title": "Label_43",
        "data": "7214"
    },
    {
        "title": "Label_44",
        "data": "2356"
    },
    {
        "title": "Label_45",
        "data": "5678"
    },
    {
        "title": "Label_46",
        "data": "3457"
    },
    {
        "title": "Label_47",
        "data": "6542"
    },
    {
        "title": "Label_48",
        "data": "2876"
    },
    {
        "title": "Label_49",
        "data": "9834"
    },
    {
        "title": "Label_50",
        "data": "7153"
    },
    {
        "title": "Label_51",
        "data": "5432"
    },
    {
        "title": "Label_52",
        "data": "2879"
    },
    {
        "title": "Label_53",
        "data": "8752"
    },
    {
        "title": "Label_54",
        "data": "2378"
    },
    {
        "title": "Label_55",
        "data": "5231"
    },
    {
        "title": "Label_56",
        "data": "7623"
    },
    {
        "title": "Label_57",
        "data": "4921"
    },
    {
        "title": "Label_58",
        "data": "5123"
    },
    {
        "title": "Label_59",
        "data": "8934"
    },
    {
        "title": "Label_60",
        "data": "2394"
    },
    {
        "title": "Label_61",
        "data": "5124"
    },
    {
        "title": "Label_62",
        "data": "5126"
    },
    {
        "title": "Label_63",
        "data": "7823"
    },
    {
        "title": "Label_64",
        "data": "2837"
    },
    {
        "title": "Label_65",
        "data": "6452"
    },
    {
        "title": "Label_66",
        "data": "2786"
    },
    {
        "title": "Label_67",
        "data": "1294"
    },
    {
        "title": "Label_68",
        "data": "2348"
    },
    {
        "title": "Label_69",
        "data": "3789"
    },
    {
        "title": "Label_70",
        "data": "5731"
    },
    {
        "title": "Label_71",
        "data": "9873"
    },
    {
        "title": "Label_72",
        "data": "2789"
    },
    {
        "title": "Label_73",
        "data": "8234"
    },
    {
        "title": "Label_74",
        "data": "5642"
    },
    {
        "title": "Label_75",
        "data": "2834"
    },
    {
        "title": "Label_76",
        "data": "1234"
    },
    {
        "title": "Label_77",
        "data": "8237"
    },
    {
        "title": "Label_78",
        "data": "6532"
    },
    {
        "title": "Label_79",
        "data": "2761"
    },
    {
        "title": "Label_80",
        "data": "3847"
    },
    {
        "title": "Label_81",
        "data": "1938"
    },
    {
        "title": "Label_82",
        "data": "6457"
    },
    {
        "title": "Label_83",
        "data": "8934"
    },
    {
        "title": "Label_84",
        "data": "3847"
    },
    {
        "title": "Label_85",
        "data": "2743"
    },
    {
        "title": "Label_86",
        "data": "6543"
    },
    {
        "title": "Label_87",
        "data": "2834"
    },
    {
        "title": "Label_88",
        "data": "1238"
    },
    {
        "title": "Label_89",
        "data": "5342"
    },
    {
        "title": "Label_90",
        "data": "2874"
    },
    {
        "title": "Label_91",
        "data": "5938"
    },
    {
        "title": "Label_92",
        "data": "9823"
    },
    {
        "title": "Label_93",
        "data": "5678"
    },
    {
        "title": "Label_94",
        "data": "4729"
    },
    {
        "title": "Label_95",
        "data": "8924"
    },
    {
        "title": "Label_96",
        "data": "6294"
    },
    {
        "title": "Label_97",
        "data": "2374"
    },
    {
        "title": "Label_98",
        "data": "5837"
    },
    {
        "title": "Label_99",
        "data": "1239"
    },
    {
        "title": "Label_100",
        "data": "8732"
    }
];
return{
  items
};
  }
}
</script>
<style scoped>
.wrapper100{
    border: 10px ridge rgb(0, 175, 122);
    padding:5px;
    width: 100%;
    height: 100vh;
    gap: 5px;
    margin: 0;
    display: grid;
    box-sizing:border-box;
    /* 列設定 余白（gap:5px*9)を引いて等分する*/
    grid-template-columns: repeat(10, calc(calc(100% - 45px) / 10));
    /* 行設定 余白（border:10px*2 gap:5px*9 padding:5px*2を引いて等分する*/
    grid-template-rows: repeat(10, calc(calc(100vh - 75px) / 10));
}
</style>