<template>
  <div id="app">
    <nav>
      <!-- These should now render as clickable links -->
      <router-link to="/">Monitor</router-link> |
      <router-link to="/faq">FAQ</router-link>
    </nav>

    <!-- Route content goes here -->
    <router-view />
  </div>
</template>

<style>
nav {
  background: #eee;
  padding: 10px;
}
nav a {
  margin: 0 10px;
  text-decoration: none;
}
nav a.router-link-exact-active {
  font-weight: bold;
}
</style>
