<template>
  <div>
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
            v-if="field.fieldName == 'esd_code'"
            @change="updateESDCode($event)"
            v-model="record.esd_code"
          >
            <option
              v-for="esd in esds"
              :key="esd.code"
              :value="esd.code"
            >
              {{ esd.code }}
            </option>
          </select>
          <input
            v-else-if="field.fieldName == 'esd_name' && esds.length > 0"
            type="text"
            :value="
              newESDName
                ? newESDName
                : currentRecord
                ? currentRecord.esd_name
                : ''
            "
            disabled
          />
          <input
            v-else-if="currentRecord && field.fieldName == 'code'"
            type="text"
            :value="record.code"
            disabled
          />
          <input
            v-else
            type="text"
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
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: [
    "currentReport",
    "currentRecord",
    "fields",
    "esds",
  ],
  data() {
    return {
      record: {},
      newESDName: null,
    };
  },
  mounted() {
    this.record = this.currentRecord;
  },

  methods: {
    updateESDCode(event) {
      let code = event.target.value;
      for (let esd of this.esds) {
        if (esd.code == code) {
          this.newESDName = esd.name;
        }
      }
    },
    submitRecordUpdate(id) {
      const path = "http://localhost:80/" + this.currentReport + "/" + id;
      console.log(this.record);
      axios
        .post(
          path,
          this.record
        )
        .then((res) => {
          console.log(res.data);
          this.$emit("submitButtonClicked");
        })
        .catch((err) => {
          console.error(err);
        });
    }
  },
};
</script>

<style>
</style>
