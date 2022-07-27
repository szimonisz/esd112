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
        this.recordList = null;
      } else {
        this.recordList = null;
      }
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
</style>
