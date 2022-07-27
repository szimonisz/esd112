<template>
  <div>
    <transition name="modal-animation">
      <!-- Only show this if modalActive is true-->
      <div v-show="modalActive" class="modal">
        <transition name="modal-animation-inner">
          <div class="modal-inner" v-show="modalActive">
            <slot />
            <button @click="closeModal()">Close</button>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  props: ["modalActive"],

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
    background-color:rgba(255,255,255,0.7)
}
.modal-inner {
    position: relative;
    max-width: 640px;
    width: 80%;
    padding: 64px 16px;
    box-shadow: 5px 10px #888888;
    background-color: #fff;
    border: 1px solid;
}

</style>
