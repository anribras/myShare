<template>
  <div class="container">
    <div id="app" style="height: 500px"></div>
    <van-button type="primary">nice</van-button>
    <van-button type="default">nice</van-button>
    <van-button type="warning">nice</van-button>
  </div>
</template>

<script>
import { sMap } from './TT/Tmap'

export default {
  data () {
    return {
      TTMap: null,
      mapInstance: null,
      fromLat: 40.094039,
      fromLng: 116.307630,
      toLat: 39.979466,
      toLng: 116.307888,
    }
  },
  mounted () {
    const key = 'GGABZ-G2MRF-WLWJQ-JE5WT-2PARO-USBN4'
    sMap(key).then(TMap => {
        console.log(TMap)
        this.mapInstance = new TMap.Map(document.getElementById('app'), {
          // 地图的中心地理坐标。
          center: new TMap.LatLng(this.fromLat, this.fromLng),
          // 缩放
          zoom: 16,
          // 俯仰角
          // pitch: 43.5,
          // rotation: 45,
          // viewMode: '3D'
        })

        // //WebServiceAPI请求URL（驾车路线规划默认会参考实时路况进行计算）
        var url = 'https://apis.map.qq.com/ws/direction/v1/driving/' //请求路径
        url += '?from=' + this.fromLat + ',' + this.fromLng  //起点坐标
        url += '&to=' + this.toLat + ',' + this.toLng//终点坐标
        // //发起JSONP请求，获取路线规划结果
        this.$jsonp(url, {
          key: key,
          output: 'jsonp'
        }).then(ret => {
          var coors = ret.result.routes[0].polyline, pl = []
          // 坐标解压（返回的点串坐标，通过前向差分进行压缩，因此需要解压）
          var kr = 1000000
          for (var i = 2; i < coors.length; i++) {
            coors[i] = Number(coors[i - 2]) + Number(coors[i]) / kr
          }
          // 将解压后的坐标生成LatLng数组
          for (var i = 0; i < coors.length; i += 2) {
            pl.push(new TMap.LatLng(coors[i], coors[i + 1]))
          }
          //创建 MultiPolyline显示折线
          var polylineLayer = new TMap.MultiPolyline({
            id: 'polyline-layer', //图层唯一标识
            map: this.mapInstance,//绘制到目标地图
            //折线样式定义
            styles: {
              'style_blue': new TMap.PolylineStyle({
                'color': '#3777FF', //线填充色
                'width': 6, //折线宽度
                'borderWidth': 5, //边线宽度
                'borderColor': '#FFF', //边线颜色
                'lineCap': 'round', //线端头方式
                'showArrow': true

              })
            },
            //折线数据定义
            geometries: [
              {
                'id': 'pl_1',//折线唯一标识，删除时使用
                'styleId': 'style_blue',//绑定样式名
                'paths': pl
              }
            ]
          })
          // 创建LatLngBounds实例
          var latlngBounds = new TMap.LatLngBounds()
          // 将坐标逐一做为参数传入extend方法，latlngBounds会根据传入坐标自动扩展生成
          console.log(pl.length)
          for (var i = 0; i < pl.length; i++) {
            latlngBounds.extend(pl[i])
          }
          // 调用fitBounds自动调整地图显示范围
          this.mapInstance.fitBounds(latlngBounds,{
            padding:50,
            ease: {
              duration: 1000
            }
          })
        })
        //创建并初始化MultiMarker
        var markerLayer = new TMap.MultiMarker({
          map: this.mapInstance,  //指定地图容器
          //样式定义
          styles: {
            //创建一个styleId为"myStyle"的样式（styles的子属性名即为styleId）
            'myStartStyle': new TMap.MarkerStyle({
              'width': 35,  // 点标记样式宽度（像素）
              'height': 35, // 点标记样式高度（像素）
              'src': './assets/start.png',  //图片路径
              //焦点在图片中的像素位置，一般大头针类似形式的图片以针尖位置做为焦点，圆形点以圆心位置为焦点
              'anchor': {
                x: 35,
                y: 35
              }
            }),
            'myEndStyle': new TMap.MarkerStyle({
              'width': 35,  // 点标记样式宽度（像素）
              'height': 35, // 点标记样式高度（像素）
              'src': './assets/end.png',  //图片路径
              //焦点在图片中的像素位置，一般大头针类似形式的图片以针尖位置做为焦点，圆形点以圆心位置为焦点
              'anchor': {
                x: 35,
                y: 35
              }
            }),
            'myCurrentStyle': new TMap.MarkerStyle({
              'width': 35,  // 点标记样式宽度（像素）
              'height': 35, // 点标记样式高度（像素）
              'src': './assets/current.png',  //图片路径
              //焦点在图片中的像素位置，一般大头针类似形式的图片以针尖位置做为焦点，圆形点以圆心位置为焦点
              'anchor': {
                x: 35,
                y: 35
              }
            })
          },
          //点标记数据数组
          geometries: [{
            'id': '1',   //点标记唯一标识，后续如果有删除、修改位置等操作，都需要此id
            'styleId': 'myStartStyle',  //指定样式id
            'position': new TMap.LatLng(this.fromLat, this.fromLng),  //点标记坐标位置
            'properties': {//自定义属性
              'title': 'marker1'
            }
          }, {//第二个点标记
            'id': '2',
            'styleId': 'myEndStyle',
            'position': new TMap.LatLng(this.toLat, this.toLng),
            'properties': {
              'title': 'marker2'
            }
          }
          ]
        })


        this.mapInstance.on('click', evt => {
          console.log('new click')
          markerLayer.updateGeometries({
            'id': '3',
            'styleId': 'myCurrentStyle',
            'position': new TMap.LatLng(evt.latLng.lat, evt.latLng.lng),
            'properties': {
              'title': 'marker3'
            }
          })
        })

      }
    )
  },
  methods: {},
  created: function () {
  }
}

</script>

<style lang="scss">

.container {
  margin-left: 20px;
  margin-right: 20px;
  position: absolute;
  height: 100%;
  width: 100%;
}

#app {
  position: relative;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
