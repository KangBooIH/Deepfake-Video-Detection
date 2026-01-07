<script setup>
    import Toast from 'primevue/toast';
    import { useToast } from 'primevue/usetoast';

    const toast = useToast();

    const show = () => {
        toast.add({severity: 'success', summary: 'Success!', detail: 'Thank you! Your feedback has been submitted successfully.', life: 3000})
    };

    function sendFeedback() {
        
    }
</script>

<template>
    <div class="allFeedback">
        <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-t-20 animate-duration-1000' }" class="feedbackSection">
            <h1 id="Contact">Have feedback?</h1>
            <h2>Let us know!</h2>
    
            <form @submit.prevent="sendFeedback" id="formFeedback">
                <input type="text" placeholder="Your name" id="name" style="background-color: #ffffff; color: #4d4d4d;">
                <textarea name="" id="feedback" placeholder="Your feedback" style="background-color: #ffffff; color: #4d4d4d;"></textarea>
                <Toast />
                <button  type="submit" @click="show()">Submit</button>
            </form>
        </div>
        <div v-animateonscroll="{ enterClass: 'animate-enter fade-in-10 slide-in-from-b-20 animate-duration-1000' }" class="connectSection">
            <h2>Connect With Us</h2>
            <div>
                <p>For questions, support, or further information, please contact us through the details below.</p>
                <a href="">deepfakedetection.report@gmail.com</a>
            </div>
        </div>
    </div>
</template>

<style scoped>
.allFeedback {
    background-color: #ffffff;
    width: 100%;
    padding: 5rem 5rem 10rem 5rem;
    margin-top: 20rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    /* margin-top: 2rem; */
}

.feedbackSection {
    width: 45%;
}

h1 {
    font-weight: bold;
    font-size: 45px;
    color: #000000;
    /* text-align: center; */
}

h2 {
    font-weight: 700;
    font-size: 35px;
    color: #000000;    
}

#formFeedback {
    display: flex;
    flex-direction: column;
    gap: 1rem; /* Jarak antar elemen form */
    margin-top: 1rem; /* Menambahkan sedikit jarak antara judul dan form */
}

#formFeedback textarea {
    max-height: 100%;
    max-width: 80%;
    min-width: 80%;
}

#formFeedback input, #formFeedback textarea {
    width: 80%; /* Membuat input dan textarea memenuhi lebar kontainer */
    padding: 1rem; /* Memberi padding agar lebih besar dan mudah diisi */
    border-radius: 20px;
    border: 1px solid #ddd; /* Menambahkan border untuk elemen form */
    font-size: 1rem;
    font-family: Inter,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    'Fira Sans',
    'Droid Sans',
    'Helvetica Neue',
    sans-serif;
}


#formFeedback button {
    padding: 1rem 2rem;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 1rem;
    margin-top: 1rem;
    width: 80%;
    font-weight: 600;
    background-color: #933ace;
    transition: 0.7s;
}

#formFeedback button:hover {
    background-color: #5d0c76;
    color: rgb(255, 255, 255);
}

.connectSection {
    width: 48%;
     /* Menyediakan ruang untuk bagian Connect */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    text-align: left;
}

.connectSection p {
    margin-left: 0.2rem;
    color: #000000;
    /* margin-top: 1rem; */
    width: 70%;
}

.connectSection a {
    margin-left: 0.2rem;
    color: #0000EE; /* Warna link */
    text-decoration: none;
}

</style>