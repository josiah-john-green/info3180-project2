<template>
<!-- Empty template as the logic is handled in the script setup -->
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router'; // Router for navigation

    // Reactive variable for storing the CSRF token
    const csrf_token = ref("");

    // Function to fetch the CSRF token
    function getCsrfToken() {
        return fetch('/api/v1/csrf-token') // Ensure correct endpoint
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to fetch CSRF token"); // Handle HTTP errors
            }
            return response.json();
        })
        .then((data) => {
            csrf_token.value = data.csrf_token; // Store the CSRF token
            return csrf_token.value; // Return the CSRF token for further use
        })
        .catch((error) => {
            console.error("Error fetching CSRF token:", error); // Handle fetch errors
        });
    }

    // Function to send the logout request
    function logout(csrfToken) {
        return fetch('/api/v1/auth/logout', {
            method: 'POST', // Ensure correct HTTP method
            headers: {
            'Content-Type': 'application/json', // Content type
            'X-CSRF-Token': csrfToken, // CSRF token
            },
        })
        .then((response) => {
        if (!response.ok) {
            throw new Error("Logout request failed"); // Handle HTTP errors
        }
        return response.json(); // Parse the response
        })
        .then((data) => {
            console.log("Logout successful:", data); // Confirm successful logout
        })
        .catch((error) => {
            console.error("Logout error:", error); // Handle logout errors
        });
    }

    // On mount, fetch the CSRF token and initiate logout
    const router = useRouter();

    onMounted(() => {
        getCsrfToken().then((csrfToken) => {
            const token = localStorage.getItem('jwt'); // Retrieve JWT from local storage

            if (token) {
                console.log('This is the logout before token:', token);
                localStorage.removeItem('jwt'); // Remove the JWT from local storage
                console.log('This is the logout after token:', token);
                console.log('This is the csrf before token:', csrfToken);
                logout(csrfToken); // Call the logout function with CSRF token
                console.log('This is the csrf after token:', csrfToken);
                router.push({ name: 'home' }); // Redirect after logout
            } else {
                router.push({ name: 'login' }); // Redirect to login if no JWT
            }
        });
    });
</script>

<style scoped>
/* Additional styles can go here if needed */
</style>
