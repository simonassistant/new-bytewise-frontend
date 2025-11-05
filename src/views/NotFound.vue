<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Oops! The page you were looking for doesn’t exist.</p>
    <router-link to="/">Go back home</router-link>
  </div>
</template>

<script>
export default {
  name: "NotFoundPage",
};
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
  padding: 2rem;
}

.not-found h1 {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.not-found p {
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
}

.not-found a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}
</style>