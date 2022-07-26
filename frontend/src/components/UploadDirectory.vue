<template>
    <form @submit.prevent="uploadFile()" id="message">
        <label for="file">{{ msg }}</label>
        <input type="file" id="file" name="file" ref="file">
        <input type="submit" value="Upload">
    </form>
</template>

<script>
import axios from 'axios';
export default {
    name:'UploadDirectory',
    data() {
        return {
            msg: "Upload a CSV file: "
        }
    },
    methods: {
        uploadFile() {
            console.log("ahh!!");
            //const fileInput = document.getElementById('file');
            const fileInput = this.$refs.file.files[0];
            const path = 'http://localhost:80/upload';
            console.log(fileInput);
            axios.post(path, { 
                file: fileInput
            }, { headers: {
                'Content-Type': 'multipart/form-data',
                'Access-Control-Allow-Origin': '*'
            }})
            .then ((res) => {
                console.log(res.data);
                console.log(fileInput);
            })
            .catch ((err) => {
                console.log("hi");
                console.error(err);
            });
        },
        getResponse(){
            const path = 'http://localhost:80/upload';
            axios.get(path)
            .then ((res) => {
                console.log(res.data);
                this.msg = res.data;
            })
            .catch ((err) => {
                console.error(err);
            });
        },
    },
    created(){
        //this.getResponse();
    }
}
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