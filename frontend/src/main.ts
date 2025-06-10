import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// Import Bootstrap JS (required for components that require JavaScript)
import 'bootstrap';

// Import main SCSS file
import '@/assets/styles/main.scss';

// Create app
const app = createApp(App);

// Create Pinia store
const pinia = createPinia();

// Use plugins
app.use(pinia);
app.use(router);

// Mount the app
app.mount('#app');

// Log app initialization
console.log('Application initialized');
