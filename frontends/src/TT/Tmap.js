export function sMap(key) {
  return new Promise(function (resolve, reject) {
    window.init = function () {
      resolve(TMap)//注意这里
    }
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "http://map.qq.com/api/gljs?v=1.exp&callback=init&key="+key;
    script.onerror = reject;
    document.head.appendChild(script);
  })
}
