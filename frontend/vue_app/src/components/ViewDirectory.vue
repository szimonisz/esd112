<template>
  <div id="container">
    <Modal
      v-if="modalActive"
      @closeButtonClicked="closeModal()"
      @submitButtonClicked="getAll(currentReport)"
      :isNewRecord="isNewRecord"
      :currentReport="currentReport"
      :currentRecord="currentRecord"
      :fields="fields"
      :esds="esds"
      :districts="districts"
      :schoolCategories="schoolCategories"
      :gradeCategories="gradeCategories"
    >
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
      <div id="add-record-container">
        <button @click="addRecord()">New {{ currentReportCapitalized }}</button>
      </div>
    </div>
    <div>
      <div class="loader-container" v-if="loading">
        <div class="loader"></div>
      </div>
      <table id="record-table" v-if="fields && recordList">
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
              {{
                field.fieldName == "school_categories" &&
                !(item.school_categories === undefined)
                  ? item.school_categories
                      .map((value) => value.title)
                      .join(",\n")
                  : item[field.fieldName]
              }}
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
import Modal from "./MyModal.vue";
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
    let districtFields = [
      { tableHeader: "ESD Code", fieldName: "esd_code" },
      { tableHeader: "ESD Name", fieldName: "esd_name" },
      { tableHeader: "District Code", fieldName: "code" },
      { tableHeader: "District Name", fieldName: "name" },
      { tableHeader: "Address Line 1", fieldName: "line_one" },
      { tableHeader: "Address Line 2", fieldName: "line_two" },
      { tableHeader: "City", fieldName: "city" },
      { tableHeader: "State", fieldName: "state" },
      { tableHeader: "Zipcode", fieldName: "zip" },
      { tableHeader: "Administrator Name", fieldName: "firstname" },
      { tableHeader: "Phone", fieldName: "phone_number" },
      { tableHeader: "Email", fieldName: "email" },
    ];
    let schoolFields = [
      { tableHeader: "ESD Code", fieldName: "esd_code" },
      { tableHeader: "ESD Name", fieldName: "esd_name" },
      { tableHeader: "District Code", fieldName: "district_code" },
      { tableHeader: "District Name", fieldName: "district_name" },
      { tableHeader: "School Code", fieldName: "code" },
      { tableHeader: "School Name", fieldName: "name" },
      { tableHeader: "Lowest Grade", fieldName: "lowest_grade" },
      { tableHeader: "Highest Grade", fieldName: "highest_grade" },
      { tableHeader: "School Categories", fieldName: "school_categories" },
      { tableHeader: "AYP Code", fieldName: "ayp_code" },
      { tableHeader: "Grade Category", fieldName: "grade_category" },
      { tableHeader: "Address Line 1", fieldName: "line_one" },
      { tableHeader: "Address Line 2", fieldName: "line_two" },
      { tableHeader: "City", fieldName: "city" },
      { tableHeader: "State", fieldName: "state" },
      { tableHeader: "Zipcode", fieldName: "zip" },
      { tableHeader: "Principal Name", fieldName: "firstname" },
      { tableHeader: "Phone", fieldName: "phone_number" },
      { tableHeader: "Email", fieldName: "email" },
    ];
    return {
      // 'esd', 'district', or 'school'
      currentReport: null,
      // populates modal form
      currentRecord: {},
      // populates table
      recordList: null,
      // populates table headers, gives access access to record attributes
      fields: null,
      // determines if modal is open or not
      modalActive: false,
      esdFields: esdFields,
      districtFields: districtFields,
      schoolFields: schoolFields,
      // used to populate ESD code options in District Form
      esds: [],
      // used to populate District code options in School Form
      districts: [],
      // used to populate SchoolCategory checkboxes in School Form
      schoolCategories: [],
      // used to populate GradeCategory options in School Form
      gradeCategories: [],
      // determines if 'add new record' or 'edit existing record' form modal is opened
      isNewRecord: null,
      currentReportCapitalized: null,
      loading: false,
    };
  },
  methods: {
    closeModal() {
      this.modalActive = false;
      this.currentRecord = {};
    },
    updateReportType(reportType) {
      this.currentRecord = {};
      this.currentReport = reportType;

      if (reportType == "esd") {
        this.fields = this.esdFields;
        this.currentReportCapitalized = "ESD";
      } else if (reportType == "district") {
        this.fields = this.districtFields;
        this.currentReportCapitalized = "District";
      } else {
        this.fields = this.schoolFields;
        this.currentReportCapitalized = "School";
      }
      this.getAll(reportType);
    },
    getAll(tableName) {
      const path = "http://localhost:80/api/" + tableName + "/all";
      this.loading = true;
      this.recordList = null;
      axios
        .get(path)
        .then((res) => {
          // Save the ESDs so they can be referenced in District Form's 'ESD Code, ESD Name' drop-down selector
          if (tableName == "esd") {
            this.esds = res.data;
          }
          // Save the Districts so they can be referenced in School Form's 'District Code, District Name' drop-down selector
          if (tableName == "district") {
            this.districts = res.data;
          }
          // Save the School Categories so they can be referenced in School Form's 'School Categories' checkbox selector
          if (tableName == "school_category") {
            this.schoolCategories = res.data;
          }
          // Save the GradeCategories so they can be referenced in School Form's 'Grade Category' drop-down selector
          if (tableName == "grade_category") {
            this.gradeCategories = res.data;
          }
          if (tableName == this.currentReport) {
            if (res.data.length > 0) {
              this.recordList = res.data;
            }
          }
          this.loading = false;
        })
        .catch((err) => {
          console.error(err);
          this.loading = false;
        });
    },
    deleteRecord(id) {
      const path = "http://localhost:80/api/" + this.currentReport + "/" + id;
      axios
        .delete(path)
        .then(() => {
          this.getAll(this.currentReport);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    editRecord(id) {
      this.isNewRecord = false;
      this.getRecord(id);
    },
    addRecord() {
      this.modalActive = true;
      this.isNewRecord = true;
    },
    getRecord(id) {
      const path = "http://localhost:80/api/" + this.currentReport + "/" + id;
      axios
        .get(path)
        .then((res) => {
          this.currentRecord = res.data;
          this.modalActive = true;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  mounted() {
    this.updateReportType("district");
    this.getAll("esd");
    this.getAll("district");
    this.getAll("school_category");
    this.getAll("grade_category");
  },
};
</script>

<style>
.radio-group {
  border-top: 4px white solid;
  /*border-bottom: 1px white solid;*/
  background-color: #009879;
  display: flex;
  font-weight: bold;
  color: white;
  padding-top: 5px;
}
.radio-group input[type="radio"],
.radio-group label,
.radio-group p,
.radio-group button {
  vertical-align: baseline;
  padding: 10px;
  margin: 10px;
}
table {
  border-collapse: collapse;
  min-width: 100%;
}
table,
th,
td,
button {
  font-size: 11px;
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
  padding: 10px 10px;
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
#container {
  display: inline-block;
  min-width: 100%;
}
#add-record-container button {
  transition-duration: 0.4s;
  text-transform: capitalize;
  border: 2px solid #ffff;
  font-size: 12px;
  padding: 10px;
  margin: 10px;
  /*background-color:#1e6fc5;*/
  color: white;
  background-color: #009879;
  font-weight: bold;
}
#add-record-container button:hover {
  background-color: #ffff;
  color: #009879;
  font-size: 12px;
  font-weight: bold;
}
.loader-container {
  display: flex;
  justify-content: center;
  height: 100%;
  width: 100%;
  padding-top: 200px;
}
/* Spinner animation borrowed from: https://www.w3schools.com/howto/howto_css_loader.asp */
.loader {
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
  text-align: center;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
