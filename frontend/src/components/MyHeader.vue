<template>
  <div id="header">
      <h1 class="logo">Education Directory</h1>
      <nav>
        <ul>
          <li><a href="/upload">Upload Report</a></li>
          <li><a href="/view">View Directory</a></li>
        </ul>
      </nav>
  </div>
</template>
<script>
export default {
  name: 'MyHeader',
}
</script>
<style>

body {
  margin: 0;
  font-weight: 30;
}
.logo {
  color: white;
  padding: 10px 0;
  text-transform: uppercase;
  grid-column: 2 / 3;
}
nav {
  grid-column: 3 / 4;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
nav ul {
  display: flex;
  padding: 10px;
  list-style: none;
}
nav li {
  margin-left: 3em;
  margin-bottom: 0;
  color: white;
}
nav a {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  text-transform: uppercase;
}
nav a:hover {
  color: black;
}
#header {
  /*background: rgb(82, 121, 111); */
  background: #009879;
  display: grid;
  grid-template-columns: 1fr auto minmax(600px, 3fr) 1fr;
  width: 100%;
  /* border: 3px solid grey; */
}
</style>
