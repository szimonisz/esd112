<template>
  <div>
    <transition name="modal-animation">
      <!-- Only show this if modalActive is true-->
      <div v-show="modalActive" class="modal">
        <transition name="modal-animation-inner">
          <div class="modal-inner" v-show="modalActive">
            <div class="modal-content">
              <h1>{{ currentReport }}</h1>
              <h3>Edit a Record:</h3>
              <form name="editRecord" id="edit-record">
                <div
                  v-for="(field, index) in this.fields"
                  :key="index"
                  :class="[index % 2 == 0 ? 'col1' : 'col2']"
                >
                  <label :for="field.fieldName">
                    {{ field.tableHeader }}
                  </label>
                  <select
                    v-if="
                      field.fieldName == 'esd_code' &&
                      currentReport == 'district'
                    "
                    :id="field.fieldName"
                    :name="field.fieldName"
                    @change="updateESDCode($event)"
                  >
                    <option
                      v-for="esd in esds"
                      :key="esd.code"
                      :value="esd.code"
                      :selected="
                        currentRecord && esd.code == currentRecord.esd_code
                      "
                    >
                      {{ esd.code }}
                    </option>
                  </select>
                  <input
                    v-else-if="
                      field.fieldName == 'esd_code' &&
                      esds.length > 0 &&
                      currentReport == 'school'
                    "
                    type="text"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    :value="
                      newESDName
                        ? newESDName
                        : currentRecord
                        ? currentRecord.esd_code
                        : ''
                    "
                    disabled
                  />
                  <div
                    v-else-if="
                      field.fieldName == 'school_categories' && currentRecord
                    "
                    class="school-category-selection"
                  >
                    <div
                      v-for="schoolCategory in schoolCategories"
                      :key="schoolCategory.id"
                    >
                      <input
                        v-if="
                          currentRecord &&
                          currentRecord.school_categories.includes(
                            currentRecord.school_categories.find(
                              (el) => el.id === schoolCategory.id
                            )
                          )
                        "
                        :key="schoolCategory.id"
                        :id="schoolCategory.id"
                        type="checkbox"
                        checked
                      />
                      <input
                        v-else
                        :name="schoolCategory.id"
                        type="checkbox"
                        :id="schoolCategory.id"
                      />
                      <label :for="schoolCategory.id">{{
                        schoolCategory.title
                      }}</label>
                    </div>
                  </div>

                  <input
                    v-else-if="field.fieldName == 'esd_name' && esds.length > 0"
                    type="text"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    :value="
                      newESDName
                        ? newESDName
                        : currentRecord
                        ? currentRecord.esd_name
                        : ''
                    "
                    disabled
                  />
                  <select
                    v-else-if="field.fieldName == 'district_code'"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    @change="updateDistrictCode($event)"
                  >
                    <option
                      v-for="district in districts"
                      :key="district.code"
                      :value="district.code"
                      :selected="
                        currentRecord &&
                        district.code == currentRecord.district_code
                      "
                    >
                      {{ district.code }}
                    </option>
                  </select>
                  <input
                    v-else-if="
                      field.fieldName == 'district_name' && districts.length > 0
                    "
                    type="text"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    :value="
                      newDistrictName
                        ? newDistrictName
                        : currentRecord
                        ? currentRecord.district_name
                        : ''
                    "
                    disabled
                  />
                  <input
                    v-else-if="field.fieldName == 'code'"
                    type="text"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    :value="
                      newDistrictName
                        ? newDistrictName
                        : currentRecord
                        ? currentRecord.code
                        : ''
                    "
                    disabled
                  />
                  <select
                    v-else-if="field.fieldName == 'grade_category'"
                    :id="field.fieldName"
                    :name="field.fieldName"
                  >
                    <option
                      v-for="gradeCategory in gradeCategories"
                      :key="gradeCategory.id"
                      :value="gradeCategory.id"
                      :selected="
                        currentRecord &&
                        gradeCategory.id == currentRecord.grade_category_id
                      "
                    >
                      {{ gradeCategory.title }}
                    </option>
                  </select>

                  <input
                    v-else
                    type="text"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    :value="currentRecord ? currentRecord[field.fieldName] : ''"
                  />
                </div>
              </form>
              <button
                type="submit"
                @click="submitRecordUpdate(currentRecord.code)"
                id="submit-button"
              >
                Submit
              </button>
            </div>
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
export default {
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
