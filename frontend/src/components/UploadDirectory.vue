<template>
  <div>
    <form @submit.prevent="uploadFile()" id="message">
      <label for="file">Upload a CSV file:</label>
      <input type="file" id="file" name="file" ref="file" />
      <input type="submit" value="Upload" />
    </form>
    <div>
      <table v-if="uploadList">
        <thead>
          <tr>
            <th>Id</th>
            <th>File Name</th>
            <th>Date Added</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in uploadList" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.filename }}</td>
            <td>{{ item.date_added }}</td>
            <td>
                <button class="delete-record" @click="deleteUpload(item.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UploadDirectory",
  data() {
    return {
      msg: "Upload a CSV file: ",
      uploadList: null,
    };
  },
  methods: {
    uploadFile() {
      const fileInput = this.$refs.file.files[0];
      const path = "http://localhost:80/upload";
      axios
        .post(
          path,
          {
            file: fileInput,
          },
          {
            headers: {
              "Content-Type": "multipart/form-data",
              "Access-Control-Allow-Origin": "*",
            },
          }
        )
        .then((res) => {
          console.log("File Upload: Success");
          this.uploadList = res.data;
          console.log(res.data);
          console.log(fileInput);
        })
        .catch((err) => {
          console.log("File Upload: Failed");
          console.error(err);
        });
    },
    getUploadHistory() {
      const path = "http://localhost:80/uploadHistory";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          if (res.data.length == 0) {
            this.uploadList = null;
          } else {
            this.uploadList = res.data;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    deleteUpload(id) {
      const path = "http://localhost:80/delete_upload/"+id;
      axios.delete(path)
        .then((res) => {
            console.log(res.data)
            this.getUploadHistory();
        })
        .catch((err) => {
            console.error(err);
        });
    }
  },
  created() {
    //this.getResponse();
    this.getUploadHistory();
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
</style>
