<template>
  <div>
    <transition name="modal-animation">
      <!-- Only show this if modalActive is true-->
      <div v-show="modalActive" class="modal">
        <transition name="modal-animation-inner">
          <div class="modal-inner" v-show="modalActive">
            <slot />
            <!--button @click="closeModal()">Close</button-->
            <!--i class="fa-solid fa-circle-xmark" @click="closeModal()"></i-->
            <i @mouseover="isHovering=true" @mouseout="isHovering=false" class="fa-circle-xmark" :class="[isHovering ? 'fa-solid' : 'fa-regular']" @click="closeModal()"></i>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: ["modalActive"],
  data() {
    return {
    isHovering: false,
    };
  },

  methods: {
    closeModal(){
        this.$emit('closeButtonClicked')
    }
  },
};
</script>

<style>
.modal {
    display: flex;
    justify-content:center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 0;
    left: 0;
    background-color:rgba(255,255,255,0.7);
    z-index: 999;
}
.modal-inner {
    position: relative;
    max-width: 640px;
    width: 80%;
    height: 80%;
    padding: 64px 16px;
    box-shadow: 5px 10px #888888;
    background-color: #fff;
    border: 1px solid;
    overflow: scroll;
}
i {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 20px;
  cursor: pointer;
}
i::hover {
  color: grey;
}

</style>
