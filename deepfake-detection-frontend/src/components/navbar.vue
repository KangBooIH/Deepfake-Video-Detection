<script setup lang="ts">
    import { RouterLink } from 'vue-router';
</script>

<template>
    <div id="allnavbar">
        <div class="logoPosition">
            <img class="logo" src="../assets/logo1.png" alt="">
        </div>
        <div id="blockNavbar">
            <nav id="navigationBar">
                <div class="navigationPosition">
                    <RouterLink v-if="$route.fullPath !== '/'" to="/" class="navLink">Home</RouterLink>
                    <a class="navLink" v-else href="#home">Home</a>
                    <RouterLink :to="{ path: '/upload', query: { reset: Date.now() } }" class="navLink">Upload</RouterLink>
                    <RouterLink v-if="$route.fullPath !== '/'" to="/#allStudies" class="navLink">About</RouterLink>
                    <a class="navLink" v-else href="#allStudies">About</a>
                    <RouterLink v-if="$route.fullPath !== '/'" to="/#Contact" class="navLink">Contact Us</RouterLink>
                    <a class="navLink" v-else href="#Contact">Contact Us</a>    
                </div>
            </nav>
            <!-- <div class="border
            ">
                <nav>
                    <RouterLink to="/Login" class="navLink rainbow" style="color: #ffffff;">Login</RouterLink>
                </nav>
            </div> -->
        </div>
    </div>
</template>

<style scoped>
#allnavbar {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 1.5rem 2rem;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    /* background-color: #2f3556; */
    z-index: 100;
}

.logo {
    width: 5vw;
    position: absolute;
    left: 3rem;
    top: 2rem;
}

#navigationBar{
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

.navigationPosition {
    max-width: 100%;
    background-color: #202020;
    padding: 0.8rem 3.5rem 0.8rem 3.5rem;
    border-radius: 60px;
    display: flex;
    justify-content: center;
    gap: 38px;
    box-shadow: 0em 0em 4em rgba(226, 153, 255, 0.822);
}

.navLink {
    text-decoration: none;
    color: #EFDAFF;
    font-weight: 600;
    gap: 10px;
    font-size: 15px;
}

/* #blockNavbar {
    width: 30%;
    background-color: #6c427a;
    padding: 0.8rem 0 0.8rem 2rem;
    border-radius: 60px;
    display: flex;
    justify-content: center;
} */

/* .signin {
    width: 5%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: 3rem;
    top: 1.5rem;
    padding: 0.5rem;
    color: #ffffff;
    background-color: #202020;
    border-radius: 40px;
    padding: 0.8rem 3.5rem 0.8rem 3.5rem;
    border: 1px solid #933ace;
    border-top: #933ace;
    border-left: #933ace;
    transition: border 1s ease;
} */

/* .signin:hover {
  background-color: #000000;
  color: rgb(255, 255, 255);
  border: 1px solid #933ace;
  border-bottom: #933ace;
  border-right: #933ace;
  transition: border 1s ease;
  /* animation: Rotate 2s infinite linear;
} */

/* @keyframes Rotate {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
} */

/* :root {
  --angle: 45deg;
  --opacity: 0.5;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

.rainbow {
    width: 5%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: 3rem;
    top: 1.5rem;
    color: #ffffff;
    background-color: #202020;
    border-radius: 40px;
    padding: 0.6rem 2.8rem 0.6rem 2.8rem;
    border: 1px solid #933ace;
    border-top: #933ace;
    border-left: #933ace;
    transition: border 1s ease;

    --border-size: 0.1rem;
    border: var(--border-size) dotted transparent;
    background-image: linear-gradient(
        to right,
        #202020,
        #202020                                                       
    ),
    conic-gradient(
        from var(--angle),
        transparent 0deg 54deg,
        #933ace 70deg 180deg,
        #933ace 180deg 216deg,
        transparent 235deg 360deg
    );
    background-origin: border-box;
    background-clip: padding-box, border-box;
}

@property --opacity {
  syntax: "<number>";
  initial-value: 0.5;
  inherits: false;
}

@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

@keyframes rotate {
  to {
    --angle: 360deg;
  }
}

.rainbow:hover {
  animation: rotate 2s linear infinite;
   background-image: linear-gradient(
        to right,
        #000000,
        #000000 
   ),
    conic-gradient(
        from var(--angle),
        transparent 0deg 54deg,
        #933ace 70deg 180deg,
        #933ace 180deg 216deg,
        transparent 235deg 360deg
    );
    background-origin: border-box;
    background-clip: padding-box, border-box;

    transition: background-image 1s;
} */

</style>