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
          placeholder="Buscar por código o nombre..." 
          class="search-input"
          @input="applyFilters"
        >
      </div>
      <div class="filter-selects">
        <div class="filter-group">
          <label for="statusFilter">Estado:</label>
          <select v-model="filters.status" id="statusFilter" class="filter-select" @change="applyFilters">
            <option value="">Todos</option>
            <option value="true">Activos</option>
            <option value="false">Inactivos</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Estado de carga y errores -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Cargando géneros...</p>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="loadGenres" class="btn-retry">Reintentar</button>
    </div>

    <!-- Tabla de datos -->
    <div v-if="!loading" class="table-container">
      <table class="crud-table">
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Fecha de Creación</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredGenres.length === 0">
            <td colspan="6" class="empty-table">No hay géneros que coincidan con la búsqueda</td>
          </tr>
          <tr v-for="genre in filteredGenres" :key="genre.codigo">
            <td>{{ genre.codigo }}</td>
            <td>{{ genre.nombre }}</td>
            <td>{{ genre.descripcion || 'Sin descripción' }}</td>
            <td>{{ formatDate(genre.fecha_creacion) }}</td>
            <td>
              <span :class="['status-badge', genre.flag ? 'status-active' : 'status-inactive']">
                {{ genre.flag ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="actions-cell">
              <button @click="editGenre(genre)" class="btn-edit">Editar</button>
              <button 
                v-if="genre.flag" 
                @click="confirmDelete(genre)" 
                class="btn-delete"
              >
                Desactivar
              </button>
              <button 
                v-if="!genre.flag" 
                @click="confirmReactivate(genre)" 
                class="btn-reactivate"
              >
                Reactivar
              </button>
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
            <label for="genreCode">Código:</label>
            <input 
              v-model="formData.codigo" 
              id="genreCode" 
              type="text" 
              class="form-control" 
              required
              :disabled="showEditModal"
              maxlength="150"
            >
            <small v-if="showEditModal" class="form-help-text">El código no puede ser modificado</small>
          </div>
          <div class="form-group">
            <label for="genreName">Nombre:</label>
            <input 
              v-model="formData.nombre" 
              id="genreName" 
              type="text" 
              class="form-control" 
              required
              maxlength="150"
            >
          </div>
          <div class="form-group">
            <label for="genreDescription">Descripción:</label>
            <textarea 
              v-model="formData.descripcion" 
              id="genreDescription" 
              class="form-control" 
              rows="3"
              maxlength="500"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="genreStatus">Estado:</label>
            <select v-model="formData.flag" id="genreStatus" class="form-control">
              <option :value="true">Activo</option>
              <option :value="false">Inactivo</option>
            </select>
          </div>
          <div v-if="showEditModal" class="form-group">
            <label>Fecha de Creación:</label>
            <div class="form-static-value">{{ formatDate(formData.fecha_creacion) }}</div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="cancelModal" class="btn-cancel">Cancelar</button>
          <button @click="saveGenre" class="btn-save" :disabled="isSaving">
            {{ isSaving ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de desactivación -->
    <div v-if="showDeleteModal" class="modal-backdrop">
      <div class="modal delete-modal">
        <div class="modal-header">
          <h3>Confirmar Desactivación</h3>
          <button @click="showDeleteModal = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <p>¿Estás seguro de que deseas desactivar el género <strong>{{ genreToDelete?.nombre }}</strong>?</p>
          <p class="delete-warning">El género será marcado como inactivo pero no se eliminará permanentemente.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn-cancel">Cancelar</button>
          <button @click="deactivateGenre" class="btn-confirm-delete" :disabled="isDeleting">
            {{ isDeleting ? 'Desactivando...' : 'Desactivar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de reactivación -->
    <div v-if="showReactivateModal" class="modal-backdrop">
      <div class="modal delete-modal">
        <div class="modal-header">
          <h3>Confirmar Reactivación</h3>
          <button @click="showReactivateModal = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <p>¿Estás seguro de que deseas reactivar el género <strong>{{ genreToReactivate?.nombre }}</strong>?</p>
        </div>
        <div class="modal-footer">
          <button @click="showReactivateModal = false" class="btn-cancel">Cancelar</button>
          <button @click="reactivateGenre" class="btn-confirm-reactivate" :disabled="isReactivating">
            {{ isReactivating ? 'Reactivando...' : 'Reactivar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Notificación -->
    <div v-if="notification.show" :class="['notification', `notification-${notification.type}`]">
      {{ notification.message }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GeneroCrud',
  data() {
    return {
      genres: [],
      filteredGenres: [],
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      showReactivateModal: false,
      genreToDelete: null,
      genreToReactivate: null,
      formData: this.getEmptyFormData(),
      filters: {
        search: '',
        status: ''
      },
      loading: false,
      error: null,
      isSaving: false,
      isDeleting: false,
      isReactivating: false,
      notification: {
        show: false,
        message: '',
        type: 'success',
        timeout: null
      }
    };
  },
  mounted() {
    this.loadGenres();
  },
  methods: {
    // Configurar headers con token de autenticación
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
    },

    getEmptyFormData() {
      return {
        codigo: '',
        nombre: '',
        descripcion: '',
        flag: true
      };
    },

    async loadGenres() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('http://127.0.0.1:8001/lib/api/generos', {
          headers: this.getAuthHeaders()
        });
        this.genres = response.data;
        this.applyFilters();
        this.$emit('update-stats');
      } catch (error) {
        console.error('Error al cargar géneros:', error);
        if (error.response?.status === 401) {
          this.error = 'No tienes autorización para acceder a esta información. Por favor, inicia sesión nuevamente.';
        } else {
          this.error = 'No se pudieron cargar los géneros. Por favor, intenta de nuevo.';
        }
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      
      try {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('es-ES', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }).format(date);
      } catch (e) {
        return dateString;
      }
    },

    editGenre(genre) {
      this.formData = { ...genre };
      this.showEditModal = true;
    },

    confirmDelete(genre) {
      this.genreToDelete = genre;
      this.showDeleteModal = true;
    },

    confirmReactivate(genre) {
      this.genreToReactivate = genre;
      this.showReactivateModal = true;
    },

    async deactivateGenre() {
      if (!this.genreToDelete) return;
      
      this.isDeleting = true;
      
      try {
        // Crear datos para desactivación lógica
        const deactivateData = {
          ...this.genreToDelete,
          flag: false
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/generos/${this.genreToDelete.id}/`, 
          deactivateData,
          { headers: this.getAuthHeaders() }
        );
        
        // Actualizar lista local
        const index = this.genres.findIndex(g => g.codigo === this.genreToDelete.codigo);
        if (index !== -1) {
          this.genres[index] = { ...this.genres[index], flag: false };
        }
        
        this.applyFilters();
        this.showNotification('Género desactivado correctamente', 'success');
      } catch (error) {
        console.error('Error al desactivar el género:', error);
        if (error.response?.status === 401) {
          this.showNotification('No tienes autorización para realizar esta acción', 'error');
        } else {
          this.showNotification('Error al desactivar el género', 'error');
        }
      } finally {
        this.isDeleting = false;
        this.showDeleteModal = false;
        this.genreToDelete = null;
      }
    },

    async reactivateGenre() {
      if (!this.genreToReactivate) return;
      
      this.isReactivating = true;
      
      try {
        // Crear datos para reactivación
        const reactivateData = {
          ...this.genreToReactivate,
          flag: true
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/generos/${this.genreToReactivate.id}/`, 
          reactivateData,
          { headers: this.getAuthHeaders() }
        );
        
        // Actualizar lista local
        const index = this.genres.findIndex(g => g.codigo === this.genreToReactivate.codigo);
        if (index !== -1) {
          this.genres[index] = { ...this.genres[index], flag: true };
        }
        
        this.applyFilters();
        this.showNotification('Género reactivado correctamente', 'success');
      } catch (error) {
        console.error('Error al reactivar el género:', error);
        if (error.response?.status === 401) {
          this.showNotification('No tienes autorización para realizar esta acción', 'error');
        } else {
          this.showNotification('Error al reactivar el género', 'error');
        }
      } finally {
        this.isReactivating = false;
        this.showReactivateModal = false;
        this.genreToReactivate = null;
      }
    },

    async saveGenre() {
      if (!this.formData.codigo || !this.formData.nombre) {
        this.showNotification('Por favor completa todos los campos requeridos', 'error');
        return;
      }
      
      this.isSaving = true;
      
      try {
        if (this.showEditModal) {
          // Actualizar género existente
          await axios.put(
            `http://127.0.0.1:8001/lib/api/generos/${this.formData.id}/`, 
            this.formData,
            { headers: this.getAuthHeaders() }
          );
          
          // Actualizar en la lista local
          const index = this.genres.findIndex(g => g.codigo === this.formData.codigo);
          if (index !== -1) {
            this.genres[index] = { ...this.formData };
          }
          
          this.showNotification('Género actualizado correctamente', 'success');
        } else {
          // Crear nuevo género
          const response = await axios.post(
            'http://127.0.0.1:8001/lib/api/generos/', 
            this.formData,
            { headers: this.getAuthHeaders() }
          );
          
          // Agregar a la lista local (con la fecha de creación que viene del servidor)
          this.genres.push(response.data);
          
          this.showNotification('Género agregado correctamente', 'success');
        }
        
        this.applyFilters();
        this.cancelModal();
      } catch (error) {
        console.error('Error al guardar el género:', error);
        
        // Mostrar mensaje de error más específico si está disponible
        let errorMessage = 'Ha ocurrido un error al guardar el género';
        
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        } else if (error.response?.data) {
          // Manejar errores de validación específicos
          const errors = error.response.data;
          if (errors.codigo || errors.nombre) {
            errorMessage = 'Campos requeridos: ';
            const missingFields = [];
            if (errors.codigo) missingFields.push('Código');
            if (errors.nombre) missingFields.push('Nombre');
            errorMessage += missingFields.join(', ');
          }
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isSaving = false;
      }
    },

    cancelModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.formData = this.getEmptyFormData();
    },

    showNotification(message, type = 'success') {
      // Limpiar notificación anterior si existe
      if (this.notification.timeout) {
        clearTimeout(this.notification.timeout);
      }
      
      // Mostrar nueva notificación
      this.notification = {
        show: true,
        message,
        type,
        timeout: setTimeout(() => {
          this.notification.show = false;
        }, 3000)
      };
    },

    applyFilters() {
      let result = [...this.genres];
      
      // Filtrar por texto de búsqueda (nombre o código)
      if (this.filters.search) {
        const searchTerm = this.filters.search.toLowerCase();
        result = result.filter(genre => {
          return genre.nombre.toLowerCase().includes(searchTerm) || 
                 (genre.codigo && genre.codigo.toLowerCase().includes(searchTerm)) ||
                 (genre.descripcion && genre.descripcion.toLowerCase().includes(searchTerm));
        });
      }
      
      // Filtrar por estado
      if (this.filters.status !== '') {
        const statusValue = this.filters.status === 'true';
        result = result.filter(genre => genre.flag === statusValue);
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
  position: relative;
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

.filter-selects {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-group {
  min-width: 150px;
}

.filter-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #4b5563;
}

.filter-select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
  min-width: 150px;
}

/* Estado de carga y errores */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #6b7280;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  border-radius: 6px;
  padding: 15px;
  color: #ef4444;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-retry {
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}

.btn-retry:hover {
  background-color: #dc2626;
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

.status-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-active {
  background-color: #d1fae5;
  color: #065f46;
}

.status-inactive {
  background-color: #fef2f2;
  color: #991b1b;
}

.actions-cell {
  white-space: nowrap;
}

.btn-edit, .btn-delete, .btn-reactivate {
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

.btn-reactivate {
  background-color: #10b981;
  color: white;
}

.btn-reactivate:hover {
  background-color: #059669;
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
  width: 600px;
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

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.form-control:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
}

.form-help-text {
  margin-top: 5px;
  font-size: 0.85rem;
  color: #6b7280;
}

.form-static-value {
  padding: 8px 12px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 1rem;
  color: #4b5563;
}

.btn-save, .btn-cancel, .btn-confirm-delete, .btn-confirm-reactivate {
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

.btn-save:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-save:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
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

.btn-confirm-delete:hover:not(:disabled) {
  background-color: #dc2626;
}

.btn-confirm-delete:disabled {
  background-color: #fca5a5;
  cursor: not-allowed;
}

.btn-confirm-reactivate {
  background-color: #10b981;
  color: white;
}

.btn-confirm-reactivate:hover:not(:disabled) {
  background-color: #059669;
}

.btn-confirm-reactivate:disabled {
  background-color: #86efac;
  cursor: not-allowed;
}

.delete-warning {
  color: #ef4444;
  font-weight: 500;
}

/* Notificaciones */
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 300px;
  z-index: 200;
  animation: fadeIn 0.3s, fadeOut 0.5s 2.5s forwards;
}

.notification-success {
  background-color: #10b981;
  color: white;
}

.notification-error {
  background-color: #ef4444;
  color: white;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-20px); }
}
</style>