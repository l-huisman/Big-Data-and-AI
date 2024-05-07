// app.js
const Vue = require('vue');
const App = require('./app.vue');

new Vue({
  render: h => h(App)
}).$mount('#app');
