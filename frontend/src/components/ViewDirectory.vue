<template>
  <div>
    <Modal
      @closeButtonClicked="this.modalActive = false"
      :modalActive="modalActive"
    >
      <div class="modal-content">
        <h1>Modal Header</h1>
        <p>Modal Message</p>
        <form name="editRecord">
          <div v-for="field in this.fields" :key="field.fieldName">
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
        </form>
      </div>
    </Modal>
    <div class="radio-group">
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
      <table v-if="recordList">
        <thead>
          <tr>
            <th v-for="header in tableHeaders" :key="header.value">
              {{ header }}
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in recordList" :key="index">
            <td v-for="field in fieldNames" :key="field.value">
              {{ item[field] }}
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
      "ESDCode",
      "ESDName",
      "DistrictCode",
      "DistrictName",
      "AddressLine1",
      "AddressLine2",
      "City",
      "State",
      "Zipcode",
      "AdministratorName",
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
    let schoolTableHeaders = ['ESDCode', 'ESDName', 'LEACode', 'LEAName', 'SchoolCode', 'SchoolName', 'LowestGrade', 'HighestGrade', 'AddressLine1',
            'AddressLine2', 'City', 'State', 'ZipCode', 'PrincipalName', 'Email', 'Phone', 'OrgCategoryList', 'AYPCode', 'GradeCategory'];
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
      "grade_category"
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
      tableHeaders: null,
      esdList: null,
      modalActive: false,
      fieldNames: null,
      esdTableHeaders: esdTableHeaders,
      esdFieldNames: esdFieldNames,
      esdFields: esdFields,
      districtTableHeaders: districtTableHeaders,
      districtFieldNames: districtFieldNames,
      districtFields: districtFields,
      schoolTableHeaders: schoolTableHeaders,
      schoolFieldNames: schoolFieldNames,
      schoolFields: schoolFields
    };
  },
  methods: {
    updateReportType(reportType) {
      this.currentReport = reportType;

      if (reportType == "esd") {
        this.getAllESDs();
        this.fields = this.esdFields;
        this.tableHeaders = this.esdTableHeaders;
        this.fieldNames = this.esdFieldNames;
      } else if (reportType == "district") {
        this.getAllDistricts();
        this.fields = this.districtTableFields;
        this.tableHeaders = this.districtTableHeaders;
        this.fieldNames = this.districtFieldNames;
      } else {
        this.getAllSchools();
        this.fields = this.schoolTableFields;
        this.tableHeaders = this.schoolTableHeaders;
        this.fieldNames = this.schoolFieldNames;
      }
    },
    getAllSchools() {
      const path = "http://localhost:80/all_schools";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          if (res.data.length == 0) {
            this.schoolList = null;
            this.recordList = null;
          } else {
            this.schoolList = res.data;
            this.recordList = this.schoolList;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getAllESDs() {
      const path = "http://localhost:80/all_ESDs";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          if (res.data.length == 0) {
            this.esdList = null;
            this.recordList = null;
          } else {
            this.esdList = res.data;
            this.recordList = this.esdList;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getAllDistricts() {
      const path = "http://localhost:80/all_districts";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          if (res.data.length == 0) {
            this.districtList = null;
            this.recordList = null;
          } else {
            this.districtList = res.data;
            this.recordList = this.districtList;
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
          this.getAllESDs();
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
  mounted(){
    this.updateReportType('district');
  }
};
</script>

<style>
label {
  display: block;
  padding-bottom: 10px;
}
#file {
  display: block;
  padding-bottom: 10px;
}
#message {
  display: block;
  padding: 5px;
}
.modal-content {
  display: flex;
  flex-direction: column;
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
  display: flex;
}
table th td tbody{ 
  font-size: 10px; 
  
}

</style>
