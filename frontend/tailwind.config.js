/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#204077', // CalHHS Blue
                secondary: '#FDB813', // California Gold
                alert: '#DC2626', // Red
                background: '#F8FAFC', // Slate
            },
        },
    },
    plugins: [],
}
