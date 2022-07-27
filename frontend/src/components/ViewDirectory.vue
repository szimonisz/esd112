<template>
  <div>
    <div>
      <table v-if="esdList">
        <thead>
          <tr>
            <th>ESD Code</th>
            <th>ESD Name</th>
            <th>Address Line 1</th>
            <th>Address Line 2</th>
            <th>State</th>
            <th>Zipcode</th>
            <th>Administator Name</th>
            <th>Phone</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in esdList" :key="item.code">
            <td>{{ item.code }}</td>
            <td>{{ item.name}}</td>
            <td>{{ item.line_one}}</td>
            <td>{{ item.line_two}}</td>
            <td>{{ item.state}}</td>
            <td>{{ item.zip}}</td>
            <td>{{ item.firstname}}</td>
            <td>{{ item.phone_number}}</td>
            <td>{{ item.email}}</td>
            <td>
                <button class="delete-record" @click="deleteESD(item.code)">Delete</button>
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
  name: "viewDirectory",
  data() {
    return {
      msg: "Upload a CSV file: ",
      esdList: null,
    };
  },
  methods: {
    getAllESDs() {
      const path = "http://localhost:80/all_ESDs";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          if (res.data.length == 0) {
            this.esdList = null;
          } else {
            this.esdList= res.data;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    deleteESD(id) {
      const path = "http://localhost:80/delete_esd/"+id;
      axios.delete(path)
        .then((res) => {
            console.log(res.data)
            this.getAllESDs();
        })
        .catch((err) => {
            console.error(err);
        });
    }
  },
  created() {
    this.getAllESDs();
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
