/* eslint-disable */ 
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.LspUUID=t():e.LspUUID=t()}(self,(function(){return e={45:function(e,t,r){const{int2Hex:n,hex2Int:o,leftZero:s}=r(712);let u=0,f=0;e.exports={uuid:function(e){let t=void 0!==e?e:Date.now();if("number"!=typeof t)throw new Error("St must be a Number!");let r=n(t);r.length<11&&(r=s(r,11));let o=n(u);if(o.length<4&&(o=s(o,4-o.length)),u++,t===f&&u>65535)throw new Error("Overstep the limits");return(t-f>=1e3||u>=65535)&&(f=t,u=0),r+o},parse:function(e){const t=e.substr(0,11).split("").reverse().join(""),r=e.substr(11,4);return{flg:0,timestamp:o(t),count:o(r)}}}},712:function(e){e.exports={int2Hex:function(e){let t=e,r="";for(;t>0;){let e=t%16;switch(t=(t-e)/16,e){case 10:r+="a";break;case 11:r+="b";break;case 12:r+="c";break;case 13:r+="d";break;case 14:r+="e";break;case 15:r+="f";break;default:r+=e+""}}return r},hex2Int:function(e){let t=e.length,r=new Array(t),n="";for(let o=0;o<t;o++)n=e.charCodeAt(o),48<=n&&n<58?n-=48:n=(223&n)-65+10,r[o]=n;return r.reduce((function(e,t){return 16*e+t}),0)},leftZero:function(e,t){let r="";for(let e=0;e<t;e++)r+="0";return r+e}}}},t={},function r(n){var o=t[n];if(void 0!==o)return o.exports;var s=t[n]={exports:{}};return e[n](s,s.exports,r),s.exports}(45);var e,t}));