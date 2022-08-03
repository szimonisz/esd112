<template>
  <div class="container">
    <form @submit.prevent="uploadFile()" id="message">
      <div class="upload-container">
        <label for="file">Upload a CSV file:</label>
        <input type="file" id="file" name="file" ref="file" />
        <div id="upload-button-container">
          <input type="submit" value="Upload" id="submit-button" />
        </div>
      </div>
    </form>

    <div>
      <div class="loader-container" v-if="loading">
        <div class="loader"></div>
      </div>
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
              <button class="delete-record" @click="deleteUpload(item.id)">
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
import axios from "axios";
export default {
  name: "UploadDirectory",
  data() {
    return {
      uploadList: null,
      loading: false,
    };
  },
  methods: {
    uploadFile() {
      this.loading = true;
      this.uploadList = null;
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
        .then(() => {
          this.loading = false;
          console.log("File Upload: Success");
          this.getUploadHistory();
        })
        .catch((err) => {
          this.loading = false;
          console.log("File Upload: Failed");
          console.error(err);
        });
    },
    getUploadHistory() {
      const path = "http://localhost:80/upload/all";
      this.loading = true;
      axios
        .get(path)
        .then((res) => {
          if (res.data.length == 0) {
            this.uploadList = null;
            this.loading = false;
          } else {
            this.uploadList = res.data;
            this.loading = false;
          }
        })
        .catch((err) => {
          console.error(err);
          this.loading = false;
        });
    },
    deleteUpload(id) {
      const path = "http://localhost:80/upload/" + id;
      axios
        .delete(path)
        .then(() => {
          this.getUploadHistory();
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getUploadHistory();
  },
};
</script>

<style>
#upload-button-container {
  padding-top: 2px;
}
#upload-button-container input {
  transition-duration: 0.4s;
  text-transform: capitalize;
  border: 2px solid #ffff;
  font-size: 12px;
  padding: 10px;
  margin: 10px;
  color: white;
  background-color: #009879;
  font-weight: bold;
}
#upload-button-container input:hover {
  background-color: #ffff;
  color: #009879;
  font-size: 12px;
  font-weight: bold;
}
.upload-container {
  border-top: 4px white solid;
  background-color: #009879;
  display: flex;
  font-weight: bold;
  color: white;
  padding-top: 5px;
}
.upload-container input,
.upload-container label,
.upload-container button
{
  vertical-align: baseline;
  padding: 10px;
  margin: 10px;
}
.upload-container input {
  border: 1px solid white;
}
button {
  font-size: 10px;
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
