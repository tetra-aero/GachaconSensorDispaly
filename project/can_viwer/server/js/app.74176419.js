(function(){"use strict";var e={3731:function(e,r,t){var n=t(5130),o=t(6768);function a(e,r,t,n,a,u){const s=(0,o.g2)("simpleList");return(0,o.uX)(),(0,o.CE)("div",null,[(0,o.bF)(s)])}var u=t(4232);const s={class:"wrapper30"},i={key:0,class:"error"};function c(e,r,t,n,a,c){const l=(0,o.g2)("dispNumber");return(0,o.uX)(),(0,o.CE)("div",s,[n.errorMessage?((0,o.uX)(),(0,o.CE)("p",i,(0,u.v_)(n.errorMessage),1)):(0,o.Q3)("",!0),((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(n.dataFromServer,((e,r)=>((0,o.uX)(),(0,o.Wv)(l,{key:r,label:e.title||"none",number:e.data||"none",unit:e.unit||"mA"},null,8,["label","number","unit"])))),128))])}var l=t(782);const f={class:"number"},v={class:"data"};function d(e,r,t,n,a,s){return(0,o.uX)(),(0,o.CE)("div",f,[(0,o.Lk)("h1",null,(0,u.v_)(t.label),1),(0,o.Lk)("p",v,[(0,o.eW)((0,u.v_)(t.number),1),(0,o.Lk)("span",null,(0,u.v_)(t.unit),1)])])}var p={name:"dispNumber",props:{label:{type:String,required:!0},number:{type:String,required:!0},unit:{type:String,required:!1}}},m=t(1241);const b=(0,m.A)(p,[["render",d],["__scopeId","data-v-c3c7cfa8"]]);var g=b,y={name:"simpleList",components:{dispNumber:g},setup(){const e=(0,l.Pj)(),r=(0,o.EW)((()=>e.state.dataFromServer)),t=(0,o.EW)((()=>e.state.errorMessage)),n=()=>{e.dispatch("fetchData")};let a;return(0,o.sV)((()=>{n(),a=setInterval((()=>{n()}),1e3)})),(0,o.xo)((()=>{clearInterval(a)})),{dataFromServer:r,errorMessage:t}}};const h=(0,m.A)(y,[["render",c],["__scopeId","data-v-3e79ca4d"]]);var S=h,E={name:"App",components:{simpleList:S},setup(){return{}}};const C=(0,m.A)(E,[["render",a]]);var O=C,w=t(4373);const _=(0,l.y$)({state(){return{dataFromServer:null,errorMessege:null,retryCount:0}},mutations:{setData(e,r){e.dataFromServer=r,e.retryCount=0},setError(e,r){e.errorMessage=r},incrementRetryCount(e){e.retryCount+=1}},actions:{async fetchData({commit:e,state:r}){try{const r=await w.A.get("/json");e("setData",r.data),e("setError",null)}catch(t){e("setError","通信エラーが発生しました。"),console.error("Error fetching data:",t),r.retryCount<3?(e("incrementRetryCount"),setTimeout((()=>{this.dispatch("fetchData")}),1e3)):e("setError","通信エラーが発生しました。再試行に失敗しました。")}}},getters:{dataFromServer:e=>e.dataFromServer,errorMessage:e=>e.errorMessage}});var M=_;const j=(0,n.Ef)(O);j.use(M),j.mount("#app")}},r={};function t(n){var o=r[n];if(void 0!==o)return o.exports;var a=r[n]={exports:{}};return e[n].call(a.exports,a,a.exports,t),a.exports}t.m=e,function(){var e=[];t.O=function(r,n,o,a){if(!n){var u=1/0;for(l=0;l<e.length;l++){n=e[l][0],o=e[l][1],a=e[l][2];for(var s=!0,i=0;i<n.length;i++)(!1&a||u>=a)&&Object.keys(t.O).every((function(e){return t.O[e](n[i])}))?n.splice(i--,1):(s=!1,a<u&&(u=a));if(s){e.splice(l--,1);var c=o();void 0!==c&&(r=c)}}return r}a=a||0;for(var l=e.length;l>0&&e[l-1][2]>a;l--)e[l]=e[l-1];e[l]=[n,o,a]}}(),function(){t.n=function(e){var r=e&&e.__esModule?function(){return e["default"]}:function(){return e};return t.d(r,{a:r}),r}}(),function(){t.d=function(e,r){for(var n in r)t.o(r,n)&&!t.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:r[n]})}}(),function(){t.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){t.o=function(e,r){return Object.prototype.hasOwnProperty.call(e,r)}}(),function(){t.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={524:0};t.O.j=function(r){return 0===e[r]};var r=function(r,n){var o,a,u=n[0],s=n[1],i=n[2],c=0;if(u.some((function(r){return 0!==e[r]}))){for(o in s)t.o(s,o)&&(t.m[o]=s[o]);if(i)var l=i(t)}for(r&&r(n);c<u.length;c++)a=u[c],t.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return t.O(l)},n=self["webpackChunkviwer"]=self["webpackChunkviwer"]||[];n.forEach(r.bind(null,0)),n.push=r.bind(null,n.push.bind(n))}();var n=t.O(void 0,[504],(function(){return t(3731)}));n=t.O(n)})();
//# sourceMappingURL=app.74176419.js.map