import { createRouter, createWebHistory } from 'vue-router';
import AuthForm from '@/layout/auth_page.vue';
import Login from "@/components/login.vue";
import Registration from "@/components/registration.vue";
import main_page from "@/layout/main_page.vue";
import stationSearch from "@/layout/stationSearch_page.vue";
import trainSearch from "@/layout/trainSearch_page.vue";
import trainRoute from "@/layout/trainRoute_page.vue";
import Profile from "@/layout/profile_page.vue";
import CashierPage from "@/layout/cashier_page.vue"
import Stations from "@/components/admin/stations.vue";

function isAuthenticated() {
    return !!localStorage.getItem('token');
}

const routes = [
    {
        path: '/auth',
        name: 'AuthForm',
        component: AuthForm
    },
    {
        path: '/login',
        name: 'UserLogin',
        component: Login
    },
    {
        path: '/register',
        name: 'UserRegister',
        component: Registration
    },
    {
        path: '/',
        name: 'Home',
        component: main_page
    },
    {
        path: '/station-search',
        name: 'StationSearch',
        component: stationSearch
    },
    {
        path:'/train-search',
        name: 'TrainSearch',
        component: ()=> import("@/layout/trainSearch_page.vue"),
        props: (route) => ({
            departureStationId: route.query.departure_station_id,
            arrivalStationId: route.query.arrival_station_id,
            date: route.query.date,
        }),
    },
    {
        path: "/seats",
        name: "SeatsPage",
        component: () => import("@/layout/seats_page.vue"),
        props: (route) => ({
            trainId: Number(route.query.train_id),
            departureStationId: Number(route.query.departure_station_id),
            arrivalStationId: Number(route.query.arrival_station_id),
            date: route.query.date,
        }),
    },
    {
        path: "/train-route",
        name: "TrainRoute",
        component: trainRoute,
        props: (route) => ({
            trainId: Number(route.query.train_id),
            date:route.query.date,
        })
    },
    {
        path: "/profile",
        name: "ProfilePage",
        component: Profile
    },
    {
        path: '/cashier',
        name: "CashierPage",
        component: CashierPage
    },
    {
        path: '/admin/stations',
        name: 'Stations',
        component: Stations
    }


];

const router = createRouter({
    history: createWebHistory(import.meta.env.VITE_BASE_URL),
    routes
});

router.beforeEach((to, from, next) => {
    if (to.meta.requiresUnauth && isAuthenticated()) {
        next({ name: 'Home' });
    } else {
        next();
    }
});

export default router;
