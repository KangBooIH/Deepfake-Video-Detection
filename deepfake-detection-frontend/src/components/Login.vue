<script setup>
    import GoogleSignIn from './GoogleSignIn.vue';
</script>

<template>
    <div id="allLogin">
        <div class="login">
            <h1>Login Page</h1>
            <div>
                <div>
                    <GoogleSignIn/>
                    <form id="loginForm">
                        <div class="credential">
                            <label for="Username">Username</label>
                            <br>
                            <input type="text" class="credentialInput" placeholder="Username">
                        </div>
                        <div class="credential">
                            <label for="Password">Password</label>
                            <br>
                            <input type="password" class="credentialInput" placeholder="Password">
                        </div>
                        <button type="submit">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
#allLogin {
    padding: 7rem 5rem 0 5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.login {
    border-style: outset;
    border-top: #d9d9d95b;
    border-left: #d9d9d95b;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-radius: 60px;
    width: 50%;
    padding: 2rem;
}

#loginForm {
    display: flex;
    flex-direction: column;
}

h1{
    font-weight: bold;
    font-size: 40px;
    /*position: absolute;*/
    /* top: -10px; */
    color: #EFDAFF;
    text-align: center;
}

.credential {
    margin-bottom: 1rem;
}

.credential label{
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
}

.credentialInput {
    width: 100%;
    border-radius: 50px;
    padding: 0.75rem;
}

</style>