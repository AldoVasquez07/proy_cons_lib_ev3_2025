<template>
  <div class="app-container">
    <!-- Menú lateral -->
    <div class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <h2 class="sidebar-title">Biblioteca</h2>
        <button class="toggle-btn" @click="toggleSidebar">
          <span v-if="sidebarCollapsed">›</span>
          <span v-else>‹</span>
        </button>
      </div>
      
      <div class="sidebar-content">
        <nav class="sidebar-menu">
          <div 
            v-for="(item, index) in menuItems" 
            :key="index" 
            class="menu-item" 
            :class="{ active: activeItem === item.route }"
            @click="navigateTo(item.route)"
          >
            <span class="menu-icon">{{ item.icon }}</span>
            <span class="menu-text" v-show="!sidebarCollapsed">{{ item.text }}</span>
          </div>
        </nav>
      </div>
    </div>
    
    <!-- Contenido principal -->
    <div class="main-content">
      <header class="top-header">
        <h1>{{ pageTitle }}</h1>
        <div class="user-controls">
          <span class="user-email">{{ userEmail }}</span>
          <button @click="logout" class="btn-logout">Cerrar sesión</button>
        </div>
      </header>
      
      <div class="content-area">
        <!-- Contenido para la ruta actual -->
        <div v-if="activeItem === 'dashboard'" class="dashboard-content">
          <h2>Panel Principal</h2>
          <p>Bienvenido al sistema de gestión de biblioteca</p>
          <div class="dashboard-stats">
            <div class="stat-card">
              <div class="stat-icon">📚</div>
              <div class="stat-count">{{ stats.books }}</div>
              <div class="stat-label">Libros</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">👤</div>
              <div class="stat-count">{{ stats.authors }}</div>
              <div class="stat-label">Autores</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">🏷️</div>
              <div class="stat-count">{{ stats.genres }}</div>
              <div class="stat-label">Géneros</div>
            </div>
          </div>
        </div>
        
        <!-- Componente de Autores -->
        <AuthorCrud v-else-if="activeItem === 'authors'" @update-stats="fetchStats" />
        
        <!-- Componente de Libros -->
        <BookCrud v-else-if="activeItem === 'books'" @update-stats="fetchStats" />
        
        <!-- Componente de Géneros -->
        <GenreCrud v-else-if="activeItem === 'genres'" @update-stats="fetchStats" />
      </div>
    </div>
  </div>
</template>

<script>
//import axios from 'axios';
import AuthorCrud from './AuthorCrud.vue';
import BookCrud from './BookCrud.vue';
import GenreCrud from './GenreCrud.vue';

export default {
  name: "MainPage",
  components: {
    AuthorCrud,
    BookCrud,
    GenreCrud
  },
  data() {
    return {
      userEmail: '',
      sidebarCollapsed: false,
      activeItem: 'dashboard',
      menuItems: [
        { icon: '📊', text: 'Dashboard', route: 'dashboard' },
        { icon: '👤', text: 'Autores', route: 'authors' },
        { icon: '📚', text: 'Libros', route: 'books' },
        { icon: '🏷️', text: 'Géneros', route: 'genres' }
      ],
      stats: {
        authors: 0,
        books: 0,
        genres: 0
      }
    };
  },
  computed: {
    pageTitle() {
      const titles = {
        'dashboard': 'Panel Principal',
        'authors': 'Autores',
        'books': 'Libros',
        'genres': 'Géneros'
      };
      return titles[this.activeItem] || 'Panel Principal';
    }
  },
  mounted() {
    // Obtener el email del usuario desde localStorage
    this.userEmail = localStorage.getItem('userEmail') || 'Usuario';
    
    // Si hay una ruta almacenada, restaurarla
    const savedRoute = localStorage.getItem('currentRoute');
    if (savedRoute && this.menuItems.some(item => item.route === savedRoute)) {
      this.activeItem = savedRoute;
    }
    
    // Cargar estadísticas iniciales
    this.fetchStats();
  },
  methods: {
  toggleSidebar() {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  },
  navigateTo(route) {
    this.activeItem = route;
    localStorage.setItem('currentRoute', route);
  },
  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('currentRoute');
    window.location.reload();
  },
  async fetchStats() {
    try {
      const [booksRes, authorsRes, genresRes] = await Promise.all([
        fetch('http://127.0.0.1:8001/lib/api/libros'),
        fetch('http://127.0.0.1:8001/lib/api/autores'),
        fetch('http://127.0.0.1:8001/lib/api/generos'),
      ]);


      if (!booksRes.ok || !authorsRes.ok || !genresRes.ok) {
        throw new Error('Error al obtener los datos');
      }

      const books = await booksRes.json();
      const authors = await authorsRes.json();
      const genres = await genresRes.json();

      this.stats.books = Array.isArray(books) ? books.length : 0;
      this.stats.authors = Array.isArray(authors) ? authors.length : 0;
      this.stats.genres = Array.isArray(genres) ? genres.length : 0;
    } catch (error) {
      console.error('Error al cargar estadísticas:', error);
      this.stats.books = 0;
      this.stats.authors = 0;
      this.stats.genres = 0;
    }
  }
},
};
</script>

<style scoped>
.app-container {
  display: flex;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Estilos del sidebar */
.sidebar {
  width: 250px;
  background-color: #1e40af;
  color: white;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar-collapsed {
  width: 60px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-title {
  margin: 0;
  font-size: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px;
}

.sidebar-content {
  flex-grow: 1;
  overflow-y: auto;
}

.sidebar-menu {
  padding: 15px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu-item.active {
  background-color: rgba(255, 255, 255, 0.2);
  border-left: 4px solid #60a5fa;
}

.menu-icon {
  font-size: 1.1rem;
  margin-right: 15px;
  width: 24px;
  text-align: center;
}

.menu-text {
  font-weight: 500;
}

/* Estilos del contenido principal */
.main-content {
  flex-grow: 1;
  background-color: #f3f4f6;
  display: flex;
  flex-direction: column;
}

.top-header {
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-header h1 {
  margin: 0;
  color: #1e40af;
  font-size: 1.5rem;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-email {
  color: #6b7280;
  font-weight: 500;
}

.btn-logout {
  padding: 8px 16px;
  background-color: #ef4444;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-logout:hover {
  background-color: #b91c1c;
}

.content-area {
  padding: 25px;
  flex-grow: 1;
}

.dashboard-content, .section-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #1e40af;
  margin-top: 0;
  margin-bottom: 15px;
}

/* Estilos para las tarjetas del dashboard */
.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 25px;
}

.stat-card {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.stat-count {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e40af;
  line-height: 1;
  margin-bottom: 5px;
}

.stat-label {
  color: #6b7280;
  font-weight: 500;
}
</style>