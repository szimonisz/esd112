<template>
  <div>
    <transition name="modal-animation">
      <div class="modal">
        <transition name="modal-animation-inner">
          <div class="modal-inner">
            <div class="modal-content">
              <h1>{{ currentReport }}</h1>
              <h3 v-if="isNewRecord">Create a Record:</h3>
              <h3 v-else>Edit a Record:</h3>
              <DistrictForm
                @submitButtonClicked="submitRecordUpdate"
                v-show="currentReport == 'district'"
                :isNewRecord="isNewRecord"
                :currentReport="currentReport"
                :currentRecord="currentRecord"
                :fields="fields"
                :esds="esds"
              ></DistrictForm>
              <EsdForm
                @submitButtonClicked="submitRecordUpdate"
                v-show="currentReport == 'esd'"
                :isNewRecord="isNewRecord"
                :currentReport="currentReport"
                :currentRecord="currentRecord"
                :fields="fields"
              ></EsdForm>
              <SchoolForm
                @submitButtonClicked="submitRecordUpdate"
                v-show="currentReport == 'school'"
                :isNewRecord="isNewRecord"
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
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script>
import DistrictForm from "./DistrictForm.vue";
import EsdForm from "./EsdForm.vue";
import SchoolForm from "./SchoolForm.vue";
import axios from "axios";
export default {
  components: {
    DistrictForm,
    EsdForm,
    SchoolForm,
  },
  props: [
    "isNewRecord",
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
    newRecord(record) {
      const path = "http://localhost:80/" + this.currentReport;
      axios
        .post(path, record)
        .then(() => {
          this.closeModalAfterSubmit();
        })
        .catch((err) => {
          if (err.response) {
            if (err.response.status == "422") {
              alert(err.response.data);
            }
          }
          console.error(err);
        });
    },
    submitRecordUpdate(record) {
      if (this.isNewRecord) {
        this.newRecord(record);
      } else {
        const path =
          "http://localhost:80/" + this.currentReport + "/" + record.code;
        axios
          //.post(
          .patch(path, record)
          .then(() => {
            this.closeModalAfterSubmit();
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    closeModalAfterSubmit() {
      this.closeModal();
      this.$emit("submitButtonClicked");
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
  background-color: #009879;
  color: white;
  border: 1px solid;
  overflow: scroll;
}
.modal-content label {
  padding-bottom: 10px;
}
.modal-content h1 {
  text-transform: uppercase;
}
i {
  position: absolute;
  top: 15px;
  right: 15px;
  font-size: 20px;
  cursor: pointer;
}
i::hover sharp {
  color: grey;
}
.edit-record {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 2px;
}
.edit-record label {
  color: white;
  font-weight: bold;
  display: inline-block;
  width: 110px;
  white-space: nowrap;
}
.edit-record select,
.edit-record input {
  padding: 5px;
  border-radius: 0;
  border: 0px;
}
.col1,
.col2 {
  padding-bottom: 20px;
  margin-bottom: 10px;
}
.col1 {
  grid-column: 1 / 2;
  display: flex;
  flex-direction: column;
  padding-right: 5px;
}
.col2 {
  grid-column: 2 / 3;
  display: flex;
  flex-direction: column;
}

.submit-button {
  transition-duration: 0.4s;
  text-transform: capitalize;
  border: 2px solid #ffff;
  font-size: 15px;
  padding: 10px;
  margin: 10px;
  /*background-color:#1e6fc5;*/
  color: white;
  background-color: #009879;
  font-weight: bold;
}
.submit-button:hover {
  background-color: #ffff;
  color: #009879;
  font-size: 15px;
  font-weight: bold;
}
</style>
