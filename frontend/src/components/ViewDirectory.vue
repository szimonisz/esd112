<template>
  <div id="container">
    <Modal
      @closeButtonClicked="this.modalActive = false"
      :modalActive="modalActive"
    >
      <div class="modal-content">
        <div id="edit-header">
          <h1>Edit a Record: {{ currentReport }}</h1>
        </div>
        <div id="form-container">
          <form id="edit-record" name="editRecord">
            <ul>
              <li v-for="field in this.fields" :key="field.fieldName">
                <div id="input-container">
                  <label :for="field.fieldname">
                    {{ field.tableHeader }}
                  </label>
                  <input
                    type="text"
                    :id="field.fieldName"
                    :name="field.fieldName"
                    :value="currentRecord ? currentRecord[field.fieldName] : ''"
                  />
                </div>
              </li>
            </ul>
          </form>
        </div>
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
              <button class="edit-record" @click="editRecord(item.code)">
                Edit
              </button>
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
    let esdFields = esdTableHeaders.map((tableHeader, i) => ({
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
      //modalActive: false,
      modalActive: true,
      esdFields: esdFields,
      districtFields: districtFields,
      schoolFields: schoolFields,
    };
  },
  methods: {
    updateReportType(reportType) {
      this.currentReport = reportType;

      if (reportType == "esd") {
        this.fields = this.esdFields;
      } else if (reportType == "district") {
        this.fields = this.districtFields;
      } else {
        this.fields = this.schoolFields;
      }
      this.getAll(reportType);
    },
    getAll(tableName) {
      const path = "http://localhost:80/all_" + tableName + "s";
      this.recordList = null;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
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
  mounted() {
    this.updateReportType("district");
  },
};
</script>

<style>
#input-container{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
#edit-header {
  text-align: center;
}
ul {
  width: 100%;
}
li {
  width: 49%;
  display: inline-block;
}
#input-container label {
  width: 110px;
  font-size: 12px;
}
input[type="text"],
select {
  border: 1px solid #ccc;
  padding: 5px 10px;
  border-radius: 4px;
  box-sizing: border-box;
}
.modal-content {
  display: flex;
  flex-direction: column;
  align-content: center;
}
.modal-content > h1,
p {
  margin-bottom: 16px;
}
.modal-content > h1 {
  font-size: 32px;
}
.modal-content > p {
  font-size: 18px;
}
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
  /*font-size: 0.7vw;*/
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
input[type="radio"],
label,
p {
  vertical-align: baseline;
  padding: 10px;
  margin: 10px;
}
#container {
  display: inline-block;
  min-width: 100%;
}
</style>
