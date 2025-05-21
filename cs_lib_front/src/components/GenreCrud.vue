<template>
  <div class="crud-container">
    <div class="crud-header">
      <h2>Gestión de Géneros</h2>
      <button @click="showAddModal = true" class="btn-add">
        <span class="btn-icon">+</span> Nuevo Género
      </button>
    </div>

    <!-- Filtros de búsqueda -->
    <div class="filters-container">
      <div class="search-box">
        <input 
          v-model="filters.search" 
          type="text" 
          placeholder="Buscar por nombre..." 
          class="search-input"
          @input="applyFilters"
        >
      </div>
    </div>

    <!-- Tabla de datos -->
    <div class="table-container">
      <table class="crud-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Libros</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredGenres.length === 0">
            <td colspan="5" class="empty-table">No hay géneros que coincidan con la búsqueda</td>
          </tr>
          <tr v-for="genre in filteredGenres" :key="genre.id">
            <td>{{ genre.id }}</td>
            <td>{{ genre.name }}</td>
            <td>{{ genre.description || 'Sin descripción' }}</td>
            <td>{{ getGenreBookCount(genre.id) }}</td>
            <td class="actions-cell">
              <button @click="editGenre(genre)" class="btn-edit">Editar</button>
              <button @click="confirmDelete(genre)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para agregar/editar género -->
    <div v-if="showAddModal || showEditModal" class="modal-backdrop">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ showEditModal ? 'Editar Género' : 'Nuevo Género' }}</h3>
          <button @click="cancelModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="genreName">Nombre:</label>
            <input v-model="formData.name" id="genreName" type="text" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="genreDescription">Descripción:</label>
            <textarea v-model="formData.description" id="genreDescription" class="form-control" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label for="genreColor">Color (opcional):</label>
            <input v-model="formData.color" id="genreColor" type="color" class="form-control color-input">
            <div class="form-help-text">Selecciona un color para identificar visualmente el género</div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="cancelModal" class="btn-cancel">Cancelar</button>
          <button @click="saveGenre" class="btn-save">Guardar</button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de eliminación -->
    <div v-if="showDeleteModal" class="modal-backdrop">
      <div class="modal delete-modal">
        <div class="modal-header">
          <h3>Confirmar Eliminación</h3>
          <button @click="showDeleteModal = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <p>¿Estás seguro de que deseas eliminar el género <strong>{{ genreToDelete?.name }}</strong>?</p>
          <p v-if="getGenreBookCount(genreToDelete?.id) > 0" class="delete-warning">
            Este género está siendo utilizado por {{ getGenreBookCount(genreToDelete?.id) }} libros.
            Al eliminarlo, esos libros quedarán sin clasificar.
          </p>
          <p class="delete-warning">Esta acción no se puede deshacer.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn-cancel">Cancelar</button>
          <button @click="deleteGenre" class="btn-confirm-delete">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GenreCrud',
  data() {
    return {
      genres: [],
      filteredGenres: [],
      books: [],
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      genreToDelete: null,
      formData: this.getEmptyFormData(),
      nextId: 1,
      filters: {
        search: ''
      }
    };
  },
  mounted() {
    this.loadGenres();
    this.loadBooks();
  },
  methods: {
    getEmptyFormData() {
      return {
        id: null,
        name: '',
        description: '',
        color: '#3b82f6' // Color azul por defecto
      };
    },
    loadGenres() {
      // En una app real, aquí se haría una petición a la API
      try {
        const storedGenres = JSON.parse(localStorage.getItem('genres')) || [];
        this.genres = storedGenres;
        this.applyFilters();
        
        // Determinar el siguiente ID basado en los géneros existentes
        if (this.genres.length > 0) {
          this.nextId = Math.max(...this.genres.map(g => g.id)) + 1;
        }
        
        this.$emit('update-stats');
      } catch (e) {
        console.error('Error al cargar géneros:', e);
        this.genres = [];
        this.filteredGenres = [];
      }
    },
    loadBooks() {
      // Cargamos los libros para saber cuántos usan cada género
      try {
        this.books = JSON.parse(localStorage.getItem('books')) || [];
      } catch (e) {
        console.error('Error al cargar libros:', e);
        this.books = [];
      }
    },
    saveGenres() {
      // En una app real, aquí se haría una petición a la API
      localStorage.setItem('genres', JSON.stringify(this.genres));
      this.$emit('update-stats');
    },
    getGenreBookCount(genreId) {
      if (!genreId) return 0;
      return this.books.filter(book => book.genreId === genreId).length;
    },
    editGenre(genre) {
      this.formData = { ...genre };
      this.showEditModal = true;
    },
    confirmDelete(genre) {
      this.genreToDelete = genre;
      this.showDeleteModal = true;
    },
    deleteGenre() {
      if (!this.genreToDelete) return;
      
      this.genres = this.genres.filter(g => g.id !== this.genreToDelete.id);
      this.saveGenres();
      this.applyFilters();
      this.showDeleteModal = false;
      this.genreToDelete = null;
      
      // Mostrar notificación
      this.showNotification('Género eliminado correctamente');
    },
    saveGenre() {
      if (!this.formData.name) {
        alert('Por favor completa al menos el nombre del género');
        return;
      }
      
      if (this.showEditModal) {
        // Actualizar género existente
        const index = this.genres.findIndex(g => g.id === this.formData.id);
        if (index !== -1) {
          this.genres[index] = { ...this.formData };
        }
      } else {
        // Crear nuevo género
        const newGenre = {
          ...this.formData,
          id: this.nextId++
        };
        this.genres.push(newGenre);
      }
      
      this.saveGenres();
      this.applyFilters();
      this.cancelModal();
      
      // Mostrar notificación
      this.showNotification(this.showEditModal ? 'Género actualizado correctamente' : 'Género agregado correctamente');
    },
    cancelModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.formData = this.getEmptyFormData();
    },
    showNotification(message) {
      // En una app real, aquí se mostraría una notificación más elegante
      alert(message);
    },
    applyFilters() {
      let result = [...this.genres];
      
      // Filtrar por texto de búsqueda
      if (this.filters.search) {
        const searchTerm = this.filters.search.toLowerCase();
        result = result.filter(genre => 
          genre.name.toLowerCase().includes(searchTerm) || 
          (genre.description && genre.description.toLowerCase().includes(searchTerm))
        );
      }
      
      this.filteredGenres = result;
    }
  }
};
</script>

<style scoped>
.crud-container {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.crud-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.crud-header h2 {
  margin: 0;
  color: #1e40af;
}

.btn-add {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #059669;
}

.btn-icon {
  font-size: 1.2rem;
  margin-right: 8px;
}

/* Estilos para filtros */
.filters-container {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}

.search-box {
  flex: 1 1 300px;
}

.search-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
}

/* Estilos para la tabla */
.table-container {
  overflow-x: auto;
}

.crud-table {
  width: 100%;
  border-collapse: collapse;
}

.crud-table th, .crud-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.crud-table th {
  background-color: #f9fafb;
  color: #4b5563;
  font-weight: 600;
}

.crud-table tr:hover {
  background-color: #f9fafb;
}

.empty-table {
  text-align: center;
  padding: 30px !important;
  color: #6b7280;
  font-style: italic;
}

.actions-cell {
  white-space: nowrap;
}

.btn-edit, .btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-edit {
  background-color: #3b82f6;
  color: white;
  margin-right: 8px;
}

.btn-edit:hover {
  background-color: #2563eb;
}

.btn-delete {
  background-color: #ef4444;
  color: white;
}

.btn-delete:hover {
  background-color: #dc2626;
}

/* Estilos para modales */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal {
  background-color: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.delete-modal {
  width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1e40af;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 20px;
  flex-grow: 1;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 15px 20px;
  border-top: 1px solid #e5e7eb;
  gap: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #4b5563;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 1rem;
}

.color-input {
  height: 40px;
  padding: 2px;
  cursor: pointer;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.form-help-text {
  margin-top: 5px;
  font-size: 0.85rem;
  color: #6b7280;
}

.btn-save, .btn-cancel, .btn-confirm-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-save {
  background-color: #3b82f6;
  color: white;
}

.btn-save:hover {
  background-color: #2563eb;
}

.btn-cancel {
  background-color: #e5e7eb;
  color: #4b5563;
}

.btn-cancel:hover {
  background-color: #d1d5db;
}

.btn-confirm-delete {
  background-color: #ef4444;
  color: white;
}

.btn-confirm-delete:hover {
  background-color: #dc2626;
}

.delete-warning {
  color: #ef4444;
  font-weight: 500;
}
</style>