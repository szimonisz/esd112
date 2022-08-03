<template>
  <div class="modal-content">
    <form name="editRecord" class="edit-record">
      <div
        v-for="(field, index) in this.fields"
        :key="index"
        :class="[index % 2 == 0 ? 'col1' : 'col2']"
      >
        <label :for="field.fieldName">
          {{ field.tableHeader }}
        </label>
        <input
          v-if="field.fieldName == 'esd_code'"
          type="text"
          v-model="record.esd_code"
          disabled
        />
        <input
          v-else-if="field.fieldName == 'esd_name'"
          type="text"
          v-model="record.esd_name"
          disabled
        />
        <select
          v-else-if="field.fieldName == 'district_code'"
          @change="updateDistrictName($event)"
          v-model="record.district_code"
        >
          <option
            v-for="district in districts"
            :key="district.code"
            :value="district.code"
          >
            {{ district.code }}
          </option>
        </select>
        <input
          v-else-if="field.fieldName == 'district_name'"
          type="text"
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
          v-else-if="currentRecord && field.fieldName == 'code' && isNewRecord"
          type="text"
          v-model="record.code"
        />
        <input
          v-else-if="currentRecord && field.fieldName == 'code' && !isNewRecord"
          type="text"
          v-model="record.code"
          disabled
        />
        <div
          v-else-if="field.fieldName == 'school_categories'"
          class="school-category-selection"
        >
          <div
            v-for="schoolCategory in schoolCategories"
            :key="schoolCategory.id"
            ref="schoolCategoriesRef"
          >
            <input
              v-if="
                !(currentRecord['school_categories'] === undefined) &&
                currentRecord.school_categories.includes(
                  currentRecord.school_categories.find(
                    (el) => el.id === schoolCategory.id
                  )
                )
              "
              type="checkbox"
              :key="schoolCategory.id"
              :id="schoolCategory.id"
              checked
            />
            <input v-else type="checkbox" :id="schoolCategory.id" />
            <label :for="schoolCategory.id">{{ schoolCategory.title }}</label>
          </div>
        </div>
        <select
          v-else-if="field.fieldName == 'grade_category'"
          v-model="record.grade_category_id"
        >
          <option
            v-for="gradeCategory in gradeCategories"
            :key="gradeCategory.id"
            :value="gradeCategory.id"
          >
            {{ gradeCategory.title }}
          </option>
        </select>
        <input
          v-else
          type="text"
          :id="field.fieldName"
          :name="field.fieldName"
          v-model="record[field.fieldName]"
        />
      </div>
    </form>
    <button
      type="submit"
      @click="saveSchoolCategoriesAndSubmit()"
      class="submit-button"
    >
      Submit
    </button>
  </div>
</template>

<script>
export default {
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
      newDistrictName: null,
      record: {},
      selectedSchoolCategories: [],
    };
  },
  mounted() {
    this.record = this.currentRecord;
  },
  methods: {
    // Generate a list of all selected School Categories
    schoolCategoriesSelected() {
      this.$refs.schoolCategoriesRef.forEach((schoolCategory) => {
        if (schoolCategory.children[0].checked) {
          this.selectedSchoolCategories.push(schoolCategory.children[0].id);
        }
      });
    },
    saveSchoolCategoriesAndSubmit(){
      this.schoolCategoriesSelected();
      this.record["school_category_ids"] = this.selectedSchoolCategories;
      this.$emit("submitButtonClicked",this.record);
    },
    // Changes the disabled 'District Name' input text when a new 'District Code' options is selected
    updateDistrictName(event) {
      let code = event.target.value;
      for (let district of this.districts) {
        if (district.code == code) {
          this.newDistrictName = district.name;
        }
      }
    },
  },
};
</script>

<style>
.school-category-selection {
  padding: 0px;
}
</style>
