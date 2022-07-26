<template>
    <div id='message'>
        <img src="https://smb.ibsrv.net/imageresizer/image/blog_images/1200x1200/10087/91160/0447463001544828845.jpg">
        <p>{{ msg }}</p>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name:'MyHelen',
    data() {
        return {
            msg: "Hello this is Shark"
        }
    },
    methods: {
        getResponse(){
            const path = 'http://10.0.0.106:80/helen';
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
        this.getResponse();

    }
}
</script>
<style>
#message {
    display: flex;
    padding: 30px;
}
p {
    padding: 30px;
}
img {
    padding: 30px;
    max-width: 50%;
    height: auto;
}

</style>