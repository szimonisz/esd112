<template>
  <div>
    <div class="modal-content">
      <h1>{{ currentReport }}</h1>
      <h3>Edit a Record:</h3>
      <form name="editRecord" id="edit-record">
        <div
          v-for="(field, index) in fields"
          :key="index"
          :class="[index % 2 == 0 ? 'col1' : 'col2']"
        >
          <label :for="field.fieldName">
            {{ field.tableHeader }}
          </label>
          <input
            v-if="field.fieldName == 'code'"
            type="text"
            v-model="record.code"
            :id="field.fieldName"
            :name="field.fieldName"
            disabled
          />
          <input
            v-else
            type="text"
            v-model="record[field.fieldName]"
            :id="field.fieldName"
            :name="field.fieldName"
          />
        </div>
      </form>
      <button
        type="submit"
        @click="submitRecordUpdate(record.code)"
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
  ],
  data() {
    return {
      record: {}
    };
  },
  created() {
    this.record = this.currentRecord;
  },

  methods: {
    submitRecordUpdate(id) {
      const path = "http://localhost:80/" + this.currentReport + "/" + id;
      console.log(this.currentRecord);
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
