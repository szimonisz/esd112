<template>
  <div id="header">
      <h1 class="logo">Education Directory</h1>
      <nav>
        <ul>
          <li><a href="/upload">Upload</a></li>
          <li><a href="/view">Edit/View/Search</a></li>
          <li><a href="/helen">Helen</a></li>
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

:root {
  /*--background: rgba(0, 214, 170, .85);*/
  --background: rgba(82, 121, 111,.85);
  
}
body {
  margin: 0;
  font-weight: 30;
}
.logo {
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
  padding: 0;
  list-style: none;
}
nav li {
  margin-left: 3em;
  margin-bottom: 0;
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
  background: var(--background);
  display: grid;
  grid-template-columns: 1fr auto minmax(600px, 3fr) 1fr;
  width: 100%;
  /* border: 3px solid grey; */
}
</style>
