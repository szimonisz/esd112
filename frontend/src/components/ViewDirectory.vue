<template>
  <div id="container">
    <Modal
      @closeButtonClicked="this.modalActive = false"
      :modalActive="modalActive"
    >
      <div class="modal-content">
        <h1>Edit a Record:</h1>
        <form name="editRecord" id="edit-record">
          <div
            v-for="(field, index) in this.fields"
            :key="field.fieldName"
            :class="[index % 2 == 0 ? 'col1' : 'col2']"
          >
            <label :for="field.fieldName">
              {{ field.tableHeader }}
            </label>
            <select
              v-if="
                field.fieldName == 'esd_code' && currentReport == 'district'
              "
              :id="field.fieldName"
              :name="field.fieldName"
              @change="updateESDCode($event)"
            >
              <option
                v-for="esd in esds"
                :key="esd.code"
                :value="esd.code"
                :selected="currentRecord && esd.code == currentRecord.esd_code"
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
              v-for="school_category in school_categories"
              :key="school_category.id"
            >
              <input
                v-if="
                  currentRecord &&
                  currentRecord.school_categories.includes(
                    currentRecord.school_categories.find(
                      (el) => el.id === school_category.id
                    )
                  )
                "
                :key="school_category.id"
                :name="school_category.id"
                type="checkbox"
                checked
              />
              <input v-else :name="school_category.id" type="checkbox" />
              <label for="school_category.id">{{
                school_category.title
              }}</label>
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
                  currentRecord && district.code == currentRecord.district_code
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
                newESDName
                  ? newESDName
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
        <button type="submit">Submit</button>
      </div>
    </Modal>
    <div class="radio-group">
      <p>Report Type:</p>
      <label for="district">District</label>
      <input
        @click="updateReportType('district')"
        type="radio"
        id="district"
        name="report_type"
        value="District"
        checked
      />
      <label for="esd">ESD</label>
      <input
        @click="updateReportType('esd')"
        type="radio"
        id="esd"
        name="report_type"
        value="ESD"
      />
      <label for="school">School</label>
      <input
        @click="updateReportType('school')"
        type="radio"
        id="school"
        name="report_type"
        value="School"
      />
    </div>
    <div>
      <table id="record-table" v-if="fields">
        <thead>
          <tr>
            <th v-for="field in fields" :key="field.value">
              {{ field.tableHeader }}
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in recordList" :key="index">
            <td v-for="field in fields" :key="field.value">
              {{ item[field.fieldName] }}
            </td>
            <td>
              <button @click="editRecord(item.code)">Edit</button>
              <button class="delete-record" @click="deleteRecord(item.code)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Modal from "../components/EditModal.vue";
import axios from "axios";
export default {
  name: "viewDirectory",
  components: {
    Modal,
  },
  data() {
    let esdFields = [
      { tableHeader: "ESD Code", fieldName: "code" },
      { tableHeader: "ESD Name", fieldName: "name" },
      { tableHeader: "Address Line 1", fieldName: "line_one" },
      { tableHeader: "Address Line 2", fieldName: "line_two" },
      { tableHeader: "State", fieldName: "state" },
      { tableHeader: "Zipcode", fieldName: "zip" },
      { tableHeader: "Administrator Name", fieldName: "firstname" },
      { tableHeader: "Phone", fieldName: "phone_number" },
      { tableHeader: "Email", fieldName: "email" },
    ];
    let esdTableHeaders = [
      "ESD Code",
      "ESD Name",
      "Address Line 1",
      "Address Line 2",
      "State",
      "Zipcode",
      "Administrator Name",
      "Phone",
      "Email",
    ];
    let esdFieldNames = [
      "code",
      "name",
      "line_one",
      "line_two",
      "state",
      "zip",
      "firstname",
      "phone_number",
      "email",
    ];
    let esdFields2 = esdTableHeaders.map((tableHeader, i) => ({
      tableHeader,
      fieldName: esdFieldNames[i],
    }));
    let districtTableHeaders = [
      "ESD Code",
      "ESD Name",
      "District Code",
      "District Name",
      "Address Line 1",
      "Address Line 2",
      "City",
      "State",
      "Zipcode",
      "Administrator Name",
      "Phone",
      "Email",
    ];
    let districtFieldNames = [
      "esd_code",
      "esd_name",
      "code",
      "name",
      "line_one",
      "line_two",
      "city",
      "state",
      "zip",
      "firstname",
      "phone_number",
      "email",
    ];
    let districtFields = districtTableHeaders.map((tableHeader, i) => ({
      tableHeader,
      fieldName: districtFieldNames[i],
    }));
    let schoolTableHeaders = [
      "ESD Code",
      "ESD Name",
      "District Code",
      "District Name",
      "School Code",
      "School Name",
      "Lowest Grade",
      "Highest Grade",
      "Address Line 1",
      "Address Line 2",
      "City",
      "State",
      "Zipcode",
      "Principal Name",
      "Phone",
      "Email",
      "School Categories",
      "AYP Code",
      "Grade Category",
    ];
    let schoolFieldNames = [
      "esd_code",
      "esd_name",
      "district_code",
      "district_name",
      "code",
      "name",
      "lowest_grade",
      "highest_grade",
      "line_one",
      "line_two",
      "city",
      "state",
      "zip",
      "firstname",
      "phone_number",
      "email",
      "school_categories",
      "ayp_code",
      "grade_category",
    ];

    let schoolFields = schoolTableHeaders.map((tableHeader, i) => ({
      tableHeader,
      fieldName: schoolFieldNames[i],
    }));

    return {
      currentReport: "district",
      currentRecord: null,
      recordList: null,
      fields: null,
      modalActive: false,
      //modalActive: true,
      esdFields: esdFields,
      districtFields: districtFields,
      schoolFields: schoolFields,
      esds: [],
      districts: [],
      school_categories: [],
      gradeCategories: [],
      newESDName: null,
      newDistrictName: null,
      esdFields2: esdFields2
    };
  },
  methods: {
    updateDistrictCode(event) {
      let code = event.target.value;
      for (let district of this.districts) {
        if (district.code == code) {
          this.newDistrictName = district.name;
        }
      }
    },
    updateESDCode(event) {
      let code = event.target.value;
      for (let esd of this.esds) {
        if (esd.code == code) {
          this.newESDName = esd.name;
        }
      }
    },
    updateReportType(reportType) {
      this.currentRecord = null;
      this.currentReport = reportType;

      if (reportType == "esd") {
        this.fields = this.esdFields;
      } else if (reportType == "district") {
        this.fields = this.districtFields;
      } else {
        this.fields = this.schoolFields;
      }
      this.getAll(reportType);
      console.log(this.fields);
    },
    getAll(tableName) {
      const path = "http://localhost:80/all_" + tableName + "s";
      this.recordList = null;
      axios
        .get(path)
        .then((res) => {
          if (tableName == "esd") {
            this.esds = res.data;
            console.log(this.esds);
          }
          if (tableName == "district") {
            this.districts = res.data;
          }
          if (tableName == "school_category") {
            this.school_categories = res.data;
            console.log(res.data);
            return;
          }
          if (tableName == "grade_category") {
            this.gradeCategories = res.data;
            console.log(res.data);
            return;
          }
          if (res.data.length == 0) {
            this.recordList = null;
          } else {
            this.recordList = null;
            this.recordList = res.data;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    deleteRecord(id) {
      const path = "http://localhost:80/" + this.currentReport + "/" + id;
      axios
        .delete(path)
        .then((res) => {
          console.log(res.data);
          this.getAll(this.currentReport);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    editRecord(id) {
      this.getRecord(id);
    },
    getRecord(id) {
      const path = "http://localhost:80/" + this.currentReport + "/" + id;
      this.modalActive = true;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.currentRecord = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  computed: {
    checkedSchoolCategories() {
      let checkedCategories = [];
      for (let current_category of this.currentRecord.school_categories) {
        for (let category of this.school_categories)
          if (current_category.id == category.id) {
            checkedCategories.append(current_category);
          }
      }
      return checkedCategories;
    },
  },
  mounted() {
    this.updateReportType("district");
    // is mounted the right place for this?
    //this.getAllCodes("esd");
    this.getAll("esd");
    this.getAll("district");
    this.getAll("school_category");
    this.getAll("grade_category");
  },
};
</script>

<style>
.radio-group {
  border-top: 1px black solid;
  border-bottom: 1px black solid;
  background-color: #009879;
  display: flex;
  font-weight: bold;
  color: white;
}
table {
  border-collapse: collapse;
  min-width: 100%;
}
table,
th,
td {
  font-size: 10px;
}
th {
  background-color: #009879;
  color: #ffff;
  position: sticky;
  top: 0;
  text-align: left;
  font-weight: bold;
}
th,
td {
  padding: 12px 15px;
}
tbody tr {
  border-bottom: 1px solid #dddddd;
}
tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}
tbody tr:nth-of-type(odd) {
  background-color: #ffff;
}
.radio-group input[type="radio"],
.radio-group label,
.radio-group p {
  vertical-align: baseline;
  padding: 10px;
  margin: 10px;
}
#container {
  display: inline-block;
  min-width: 100%;
}
.modal-content label {
  padding-bottom: 10px;
}
.modal-content {
}
#edit-record {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
#edit-record label {
  display: inline-block;
  width: 110px;
}
#edit-record input {
  padding: 5px 10px;
}
#edit-record div {
  padding-bottom: 20px;
  margin-bottom: 10px;
}
.col1 {
  grid-column: 1 / 2;
}
.col2 {
  grid-column: 2 / 3;
}
</style>
