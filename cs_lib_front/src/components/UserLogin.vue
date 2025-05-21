<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="email">Correo electrónico:</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="ejemplo@correo.com"
          required
          autocomplete="username"
        />
      </div>
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="••••••••"
          required
          autocomplete="current-password"
        />
      </div>
      <button type="submit" class="btn-login">Entrar</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    <p v-if="loggedIn" class="success-message">¡Has iniciado sesión!</p>
  </div>
</template>

<script>
export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
      loggedIn: false,
      errorMessage: "",
    };
  },
  methods: {
  async handleLogin() {
    this.errorMessage = '';
    try {
      const response = await fetch('http://127.0.0.1:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: this.email,
          password: this.password,
        }),
      });

      if (!response.ok) {
        // Error de autenticación (status 400 o 401)
        this.errorMessage = 'Correo o contraseña incorrectos';
        this.loggedIn = false;
        return;
      }

      const data = await response.json();

      // Ejemplo: si recibes { access: "...", refresh: "..." }
      if (data.access) {
        this.loggedIn = true;
        this.errorMessage = '';
        // Guardar token en localStorage para usarlo después en peticiones protegidas
        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);
      } else {
        this.errorMessage = 'Error inesperado al iniciar sesión';
        this.loggedIn = false;
      }
    } catch (error) {
      this.errorMessage = 'Error de conexión con el servidor';
      this.loggedIn = false;
    }
  },
},
};
</script>

<style scoped>
.login-container {
  max-width: 350px;
  margin: 40px auto;
  padding: 25px 30px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  background-color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 6px;
  font-weight: 600;
  color: #555;
}

input[type="email"],
input[type="password"] {
  padding: 10px 12px;
  border: 1.8px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
  transition: border-color 0.3s ease;
}

input[type="email"]:focus,
input[type="password"]:focus {
  outline: none;
  border-color: #3b82f6; /* azul bonito */
  box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
}

.btn-login {
  padding: 12px 0;
  background-color: #3b82f6;
  color: white;
  font-size: 17px;
  font-weight: 700;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.25s ease;
}

.btn-login:hover {
  background-color: #2563eb;
}

.error-message {
  margin-top: 15px;
  color: #e03131;
  font-weight: 600;
  text-align: center;
}

.success-message {
  margin-top: 15px;
  color: #2f9e44;
  font-weight: 600;
  text-align: center;
}
</style>
