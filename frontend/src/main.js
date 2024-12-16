import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

createApp(App)
    .use(router)
    .mount('#app');

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then((registration) => {
                console.log('Service Worker зарегистрирован с объемом: ', registration.scope);
            })
            .catch((error) => {
                console.error('Ошибка регистрации Service Worker: ', error);
            });
    });
}

