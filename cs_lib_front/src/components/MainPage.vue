<template>
  <div class="main-container">
    <h1>¡Bienvenido, {{ userEmail }}!</h1>
    <p>Esta es la pantalla principal de la aplicación.</p>
    <button @click="logout" class="btn-logout">Cerrar sesión</button>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  data() {
    return {
      userEmail: '',
    };
  },
  mounted() {
    // Puedes obtener el email guardado (o cualquier dato) de localStorage u otra fuente
    // Aquí supongo que guardaste el email al iniciar sesión
    this.userEmail = localStorage.getItem('userEmail') || 'Usuario';
  },
  methods: {
    logout() {
      // Eliminar tokens y cualquier dato de sesión
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('userEmail');
      // Recargar la página o redirigir al login
      window.location.reload();
    },
  },
};
</script>

<style scoped>
.main-container {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  background-color: #f5f8ff;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(59, 130, 246, 0.3);
}

h1 {
  color: #2563eb;
  margin-bottom: 20px;
}

.btn-logout {
  padding: 12px 25px;
  background-color: #ef4444;
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-logout:hover {
  background-color: #b91c1c;
}
</style>
