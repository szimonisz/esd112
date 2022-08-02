<template>
  <div id="container">
    <ModalMinimal
      @closeButtonClicked="modalActive = false"
      @submitButtonClicked="getAll(currentReport)"
      :modalActive="modalActive"
      :currentReport="currentReport"
      :currentRecord="currentRecord"
      :fields="fields"
      :esds="esds"
      :districts="districts"
      :schoolCategories="schoolCategories"
      :gradeCategories="gradeCategories"
    >
    </ModalMinimal>
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
    <div id="add-record-container">
      <button @click="addRecord()">Add Record</button>
      <ModalMinimal
        @closeButtonClicked="closeModal()"
        @submitButtonClicked="getAll(currentReport)"
        :modalActive="modalActive"
        :currentReport="currentReport"
        :currentRecord="currentRecord"
        :fields="fields"
        :esds="esds"
        :districts="districts"
        :schoolCategories="schoolCategories"
        :gradeCategories="gradeCategories"
      >
      </ModalMinimal>
    </div>
    <div>
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
                field.fieldName == "school_categories"
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
//import Modal from "../components/EditModal.vue";
import ModalMinimal from "../components/EditModalMinimal.vue";
import axios from "axios";
export default {
  name: "viewDirectory",
  components: {
    ModalMinimal,
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
      { tableHeader: "Address Line 1", fieldName: "line_one" },
      { tableHeader: "Address Line 2", fieldName: "line_two" },
      { tableHeader: "City", fieldName: "city" },
      { tableHeader: "State", fieldName: "state" },
      { tableHeader: "Zipcode", fieldName: "zip" },
      { tableHeader: "Principal Name", fieldName: "firstname" },
      { tableHeader: "Phone", fieldName: "phone_number" },
      { tableHeader: "Email", fieldName: "email" },
      { tableHeader: "School Categories", fieldName: "school_categories" },
      { tableHeader: "AYP Code", fieldName: "ayp_code" },
      { tableHeader: "Grade Category", fieldName: "grade_category" },
    ];

    return {
      currentReport: null,
      //currentRecord: null,
      currentRecord: {},
      recordList: null,
      fields: null,
      modalActive: false,
      esdFields: esdFields,
      districtFields: districtFields,
      schoolFields: schoolFields,
      esds: [],
      districts: [],
      schoolCategories: [],
      gradeCategories: [],
    };
  },
  methods: {
    closeModal() {
      this.modalActive = false;
      this.currentRecord = {};
    },
    updateReportType(reportType) {
      //this.currentRecord = null;
      this.currentRecord = {};
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
          }
          if (tableName == "district") {
            this.districts = res.data;
          }
          if (tableName == "school_category") {
            this.schoolCategories = res.data;
          }
          if (tableName == "grade_category") {
            this.gradeCategories = res.data;
          }
          if (tableName == this.currentReport) {
            if (res.data.length == 0) {
              this.recordList = null;
            } else {
              this.recordList = null;
              this.recordList = res.data;
            }
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
    addRecord() {
      this.modalActive= true;
    },
    getRecord(id) {
      const path = "http://localhost:80/" + this.currentReport + "/" + id;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
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
  border-top: 1px white solid;
  border-bottom: 1px white solid;
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
.modal-content h1 {
  text-transform: uppercase;
}
#edit-record {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 2px;
}
#edit-record label {
  display: inline-block;
  width: 110px;
  white-space: nowrap;
}
#edit-record input select {
  padding: 5px 10px;
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
.school-category-selection {
  padding: 0px;
}
#add-record-container {
  padding: 20px;
  background: #009879;
}
#add-record-container button {
  padding: 20px;
}
</style>
