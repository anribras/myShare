<template>
  <transition name="fade">
    <div v-show="show">User {{ this.$route.params.uid }}</div>
  </transition>
</template>

<script>
export default {
  name: 'User',
  data () {
    return {
      show: false
    }
  },
  beforeRouteEnter (to, from, next) {
    console.log('beforeRouteEnter')
    next(vm => {
      console.log('I got this')
      vm.show = true
      console.log(vm)
    })
  },
  beforeRouteUpdate (to, from, next) {
    console.log('beforeRouteUpdate')
    this.show = !this.show
    next()
  },
  beforeRouteLeave (to, from, next) {
    console.log('beforeRouteLeave')
    next()
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter {
  opacity: 0;
}

.fade-enter-to {
  opacity: 1;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
{
  transform: translateX(20px);
  opacity: 0;
}
</style>
