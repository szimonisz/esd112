<template>
  <div>
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
          <select
            v-if="field.fieldName == 'esd_code'"
            @change="updateESDName($event)"
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
            v-else-if="field.fieldName == 'esd_name'"
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
          <input
            v-else
            type="text"
            v-model="record[field.fieldName]"
          />
        </div>
      </form>
      <button
        type="submit"
        @click="$emit('submitButtonClicked',record)"
        id="submit-button"
      >
        Submit
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    "currentReport",
    "currentRecord",
    "isNewRecord",
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
    updateESDName(event) {
      let code = event.target.value;
      for (let esd of this.esds) {
        if (esd.code == code) {
          this.newESDName = esd.name;
        }
      }
    },
  }
};
</script>

<style>
</style>
