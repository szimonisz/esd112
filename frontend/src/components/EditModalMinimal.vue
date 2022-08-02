<template>
  <div>
    <transition name="modal-animation">
      <!-- Only show this if modalActive is true-->
      <div v-if="modalActive && currentRecord" class="modal">
        <transition name="modal-animation-inner">
          <div class="modal-inner">
            <DistrictForm
              @submitButtonClicked="closeModalAfterSubmit()"
              v-show="currentReport == 'district'"
              :currentReport="currentReport"
              :currentRecord="currentRecord"
              :fields="fields"
              :esds="esds"
            ></DistrictForm>
            <EsdForm
              @submitButtonClicked="closeModalAfterSubmit()"
              v-show="currentReport == 'esd'"
              :currentReport="currentReport"
              :currentRecord="currentRecord"
              :fields="fields"
            ></EsdForm>
            <SchoolForm
              @submitButtonClicked="closeModalAfterSubmit()"
              v-show="currentReport == 'school'"
              :currentReport="currentReport"
              :currentRecord="currentRecord"
              :fields="fields"
              :esds="esds"
              :districts="districts"
              :schoolCategories="schoolCategories"
              :gradeCategories="gradeCategories"
            ></SchoolForm>
            <i
              @mouseover="isHovering = true"
              @mouseout="isHovering = false"
              class="fa-circle-xmark"
              :class="[isHovering ? 'fa-solid' : 'fa-regular']"
              @click="closeModal()"
            ></i>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script>
import DistrictForm from "../components/DistrictForm.vue";
import EsdForm from "../components/EsdForm.vue";
import SchoolForm from "../components/SchoolForm.vue";
export default {
  components: {
    DistrictForm,
    EsdForm,
    SchoolForm,
  },
  props: [
    "modalActive",
    "currentReport",
    "currentRecord",
    "fields",
    "esds",
    "districts",
    "schoolCategories",
    "gradeCategories",
  ],
  data() {
    return {
      newESDName: null,
      isHovering: false,
      newDistrictName: null,
    };
  },

  methods: {
    closeModalAfterSubmit(){
      this.closeModal();
      this.$emit("submitButtonClicked");
    },
    updateDistrictCode(event) {
      let code = event.target.value;
      for (let district of this.districts) {
        if (district.code == code) {
          console.log(district.name);
          this.newDistrictName = district.name;
        }
      }
    },
    updateESDCode(event) {
      let code = event.target.value;
      for (let esd of this.esds) {
        if (esd.code == code) {
          console.log("hi");
          this.newESDName = esd.name;
        }
      }
    },
    closeModal() {
      this.$emit("closeButtonClicked");
    },
  },
};
</script>

<style>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(255, 255, 255, 0.7);
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
