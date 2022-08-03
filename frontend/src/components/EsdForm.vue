<template>
  <div>
    <div class="modal-content">
      <form name="editRecord" class="edit-record">
        <div
          v-for="(field, index) in fields"
          :key="index"
          :class="[index % 2 == 0 ? 'col1' : 'col2']"
        >
          <label :for="field.fieldName">
            {{ field.tableHeader }}
          </label>
          <input
            v-if="field.fieldName == 'code' && isNewRecord"
            type="text"
            v-model="record.code"
            :id="field.fieldName"
            :name="field.fieldName"
          />
          <input
            v-else-if="field.fieldName == 'code' && !isNewRecord"
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
        @click="$emit('submitButtonClicked', record)"
        id="submit-button"
      >
        Submit
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["currentReport", "currentRecord", "fields", "isNewRecord"],
  data() {
    return {
      record: {},
    };
  },
  mounted() {
    this.record = this.currentRecord;
  },
};
</script>

<style></style>
