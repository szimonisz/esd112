<template>
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
          @change="updateDistrictCode($event)"
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
              v-if="!(currentRecord['school_categories'] === undefined) &&
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
      @click="submitRecordUpdate(currentRecord.code)"
      id="submit-button"
    >
      Submit
    </button>
  </div>
</template>

<script>
import axios from "axios";
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
      newDistrictName: null,
      record: {},
      selectedSchoolCategories: [],
      isNewRecord: null,
    };
  },
  mounted() {
    this.record = this.currentRecord;
    this.isNewRecord = this.isEmpty(this.currentRecord);
  },

  methods: {
    newRecord() {
      console.log(this.record);
      const path = "http://localhost:80/" + this.currentReport;
      axios
        .post(path, this.record)
        .then((res) => {
          console.log(res.data);
            this.$emit("submitButtonClicked");
        })
        .catch((err) => {
          console.log("hi");
          if (err.response){
            console.log(err.response.status)
            if (err.response.status == '422'){
              alert(err.response.data);
            }
          }
          console.error(err);
        });
    },
    isEmpty(obj) {
      return Object.keys(obj).length == 0;
    },
    schoolCategoriesChecked() {
      console.log(this.$refs.schoolCategoriesRef);
      this.$refs.schoolCategoriesRef.forEach((schoolCategory) => {
        if (schoolCategory.children[0].checked) {
          this.selectedSchoolCategories.push(schoolCategory.children[0].id);
        }
      });
      console.log(this.selectedSchoolCategories);
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
  submitRecordUpdate(id) {
    if (this.isNewRecord) {
      this.schoolCategoriesChecked();
      this.record['school_category_ids'] = this.selectedSchoolCategories;
      this.newRecord();
    } else {
    this.schoolCategoriesChecked();
    this.record['school_category_ids'] = this.selectedSchoolCategories;
    const path = "http://localhost:80/" + this.currentReport + "/" + id;
    console.log(this.record);
    axios
      .patch(path, this.record)
      .then((res) => {
        console.log(res.data);
        this.$emit("submitButtonClicked");
      })
      .catch((err) => {
        console.error(err);
      });
    }
  },
},
};
</script>

<style></style>
