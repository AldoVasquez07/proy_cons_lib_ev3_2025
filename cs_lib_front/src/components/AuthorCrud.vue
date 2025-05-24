<template>
  <div class="crud-container">
    <div class="crud-header">
      <h2>Gestión de Autores</h2>
      <button @click="showAddModal = true" class="btn-add">
        <span class="btn-icon">+</span> Nuevo Autor
      </button>
    </div>

    <!-- Filtros de búsqueda -->
    <div class="filters-container">
      <div class="search-box">
        <input 
          v-model="filters.search" 
          type="text"
          placeholder="Buscar por DNI, código, nombre o apellidos..." 
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
      <p>Cargando Autores...</p>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="loadAutores" class="btn-retry">Reintentar</button>
    </div>

    <!-- Tabla de datos -->
    <div v-if="!loading" class="table-container">
      <table class="crud-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>DNI</th>
            <th>Código</th>
            <th>Nombre</th>
            <th>Apellido Paterno</th>
            <th>Apellido Materno</th>
            <th>Fecha de Creación</th>
            <th>Estado</th>
            <th>Detalle</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredAutores.length === 0">
            <td colspan="10" class="empty-table">No hay Autores que coincidan con la búsqueda</td>
          </tr>
          <tr v-for="autor in filteredAutores" :key="autor.id">
            <td>{{ autor.id }}</td>
            <td>{{ autor.dni }}</td>
            <td>{{ autor.codigo }}</td>
            <td>{{ autor.nombre }}</td>
            <td>{{ autor.apellido_paterno }}</td>
            <td>{{ autor.apellido_materno }}</td>
            <td>{{ formatDate(autor.fecha_creacion) }}</td>
            <td>
              <span :class="['status-badge', autor.flag ? 'status-active' : 'status-inactive']">
                {{ autor.flag ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="detail-cell">
              <button @click="viewAutorDetail(autor)" class="btn-detail" title="Ver detalle">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </button>
            </td>
            <td class="actions-cell">
              <button @click="editAutor(autor)" class="btn-edit">Editar</button>
              <button 
                v-if="autor.flag" 
                @click="confirmDelete(autor)" 
                class="btn-delete"
              >
                Desactivar
              </button>
              <button 
                v-if="!autor.flag" 
                @click="confirmReactivate(autor)" 
                class="btn-reactivate"
              >
                Reactivar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para agregar/Editar Autor -->
    <div v-if="showAddModal || showEditModal" class="modal-backdrop">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ showEditModal ? 'Editar Autor' : 'Nuevo Autor' }}</h3>
          <button @click="cancelModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="autorDni">DNI: <span class="required">*</span></label>
            <input 
              v-model="formData.dni" 
              id="autorDni" 
              type="text" 
              class="form-control" 
              required
              maxlength="8"
              pattern="[0-9]{8}"
              placeholder="12345678"
            >
            <div class="form-help-text">Ingrese 8 dígitos</div>
          </div>
          <div class="form-group">
            <label for="autorCodigo">Código: <span class="required">*</span></label>
            <input 
              v-model="formData.codigo" 
              id="autorCodigo" 
              type="text" 
              class="form-control" 
              required
              maxlength="20"
              placeholder="Código único"
            >
          </div>
          <div class="form-group">
            <label for="autorNombre">Nombre: <span class="required">*</span></label>
            <input 
              v-model="formData.nombre" 
              id="autorNombre" 
              type="text" 
              class="form-control" 
              required
              maxlength="100"
            >
          </div>
          <div class="form-group">
            <label for="autorApellidoPaterno">Apellido Paterno: <span class="required">*</span></label>
            <input 
              v-model="formData.apellido_paterno" 
              id="autorApellidoPaterno" 
              type="text" 
              class="form-control" 
              required
              maxlength="100"
            >
          </div>
          <div class="form-group">
            <label for="autorApellidoMaterno">Apellido Materno: <span class="required">*</span></label>
            <input 
              v-model="formData.apellido_materno" 
              id="autorApellidoMaterno" 
              type="text" 
              class="form-control" 
              required
              maxlength="100"
            >
          </div>
          <div class="form-group">
            <label for="autorStatus">Estado:</label>
            <select v-model="formData.flag" id="autorStatus" class="form-control">
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
          <button @click="saveAutor" class="btn-save" :disabled="isSaving">
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
          <p>¿Estás seguro de que deseas desactivar a <strong>{{ getFullName(autorToDelete) }}</strong>?</p>
          <p class="delete-warning">El autor será marcado como inactivo pero no se eliminará permanentemente.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn-cancel">Cancelar</button>
          <button @click="deactivateautor" class="btn-confirm-delete" :disabled="isDeleting">
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
          <p>¿Estás seguro de que deseas reactivar a <strong>{{ getFullName(autorToReactivate) }}</strong>?</p>
        </div>
        <div class="modal-footer">
          <button @click="showReactivateModal = false" class="btn-cancel">Cancelar</button>
          <button @click="reactivateAutor" class="btn-confirm-reactivate" :disabled="isReactivating">
            {{ isReactivating ? 'Reactivando...' : 'Reactivar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Notificación -->
    <div v-if="notification.show" :class="['notification', `notification-${notification.type}`]">
      {{ notification.message }}
    </div>

    <!-- Componente de detalle del autor -->
    <AutorDetail 
      v-if="showAutorDetail"
      :autor="selectedAutor"
      @close="closeAutorDetail"
      @autor-updated="handleAutorUpdated"
    />
  </div>
</template>

<script>
import axios from 'axios';
import AutorDetail from './AutorDetail.vue';

export default {
  name: 'AutorCrud',
  components: {
    AutorDetail
  },
  data() {
    return {
      autors: [],
      filteredAutores: [],
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      showReactivateModal: false,
      showAutorDetail: false,
      selectedAutor: null,
      autorToDelete: null,
      autorToReactivate: null,
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
    this.loadAutores();
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
        dni: '',
        codigo: '',
        nombre: '',
        apellido_paterno: '',
        apellido_materno: '',
        flag: true
      };
    },

    getFullName(autor) {
      if (!autor) return '';
      return `${autor.nombre} ${autor.apellido_paterno} ${autor.apellido_materno}`.trim();
    },

    async loadAutores() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('http://127.0.0.1:8001/lib/api/autores', {
          headers: this.getAuthHeaders()
        });
        this.autors = response.data;
        this.applyFilters();
        this.$emit('update-stats');
      } catch (error) {
        console.error('Error al cargar autores:', error);
        if (error.response?.status === 401) {
          this.error = 'No tienes autorización para acceder a esta información. Por favor, inicia sesión nuevamente.';
        } else {
          this.error = 'No se pudieron cargar los autores. Por favor, intenta de nuevo.';
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

    viewAutorDetail(autor) {
      this.selectedAutor = autor;
      this.showAutorDetail = true;
    },

    closeAutorDetail() {
      this.showAutorDetail = false;
      this.selectedAutor = null;
    },

    handleAutorUpdated() {
      // Recargar la lista de autores cuando se actualice desde el detalle
      this.loadAutores();
    },

    editAutor(autor) {
      this.formData = { ...autor };
      this.showEditModal = true;
    },

    confirmDelete(autor) {
      this.autorToDelete = autor;
      this.showDeleteModal = true;
    },

    confirmReactivate(autor) {
      this.autorToReactivate = autor;
      this.showReactivateModal = true;
    },

    async deactivateautor() {
      if (!this.autorToDelete) return;
      
      this.isDeleting = true;
      
      try {
        // Crear datos para desactivación lógica
        const deactivateData = {
          ...this.autorToDelete,
          flag: false
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/autores/${this.autorToDelete.id}/`, 
          deactivateData,
          { headers: this.getAuthHeaders() }
        );
        
        // Actualizar lista local
        const index = this.autors.findIndex(p => p.id === this.autorToDelete.id);
        if (index !== -1) {
          this.autors[index] = { ...this.autors[index], flag: false };
        }
        
        this.applyFilters();
        this.showNotification('Autor desactivado correctamente', 'success');
      } catch (error) {
        console.error('Error al desactivar el autor:', error);
        if (error.response?.status === 401) {
          this.showNotification('No tienes autorización para realizar esta acción', 'error');
        } else {
          this.showNotification('Error al desactivar el autor', 'error');
        }
      } finally {
        this.isDeleting = false;
        this.showDeleteModal = false;
        this.autorToDelete = null;
      }
    },

    async reactivateAutor() {
      if (!this.autorToReactivate) return;
      
      this.isReactivating = true;
      
      try {
        // Crear datos para reactivación
        const reactivateData = {
          ...this.autorToReactivate,
          flag: true
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/autores/${this.autorToReactivate.id}/`, 
          reactivateData,
          { headers: this.getAuthHeaders() }
        );
        
        // Actualizar lista local
        const index = this.autors.findIndex(p => p.id === this.autorToReactivate.id);
        if (index !== -1) {
          this.autors[index] = { ...this.autors[index], flag: true };
        }
        
        this.applyFilters();
        this.showNotification('Autor reactivado correctamente', 'success');
      } catch (error) {
        console.error('Error al reactivar el autor:', error);
        if (error.response?.status === 401) {
          this.showNotification('No tienes autorización para realizar esta acción', 'error');
        } else {
          this.showNotification('Error al reactivar el autor', 'error');
        }
      } finally {
        this.isReactivating = false;
        this.showReactivateModal = false;
        this.autorToReactivate = null;
      }
    },

    async saveAutor() {
      // Validar campos requeridos
      if (!this.formData.dni || !this.formData.codigo || !this.formData.nombre || 
          !this.formData.apellido_paterno || !this.formData.apellido_materno) {
        this.showNotification('Por favor completa todos los campos requeridos', 'error');
        return;
      }

      // Validar formato del DNI
      if (!/^\d{8}$/.test(this.formData.dni)) {
        this.showNotification('El DNI debe tener exactamente 8 dígitos', 'error');
        return;
      }
      
      this.isSaving = true;
      
      try {
        if (this.showEditModal) {
          // Actualizar autor existente
          await axios.put(
            `http://127.0.0.1:8001/lib/api/autores/${this.formData.id}/`, 
            this.formData,
            { headers: this.getAuthHeaders() }
          );
          
          // Actualizar en la lista local
          const index = this.autors.findIndex(p => p.id === this.formData.id);
          if (index !== -1) {
            this.autors[index] = { ...this.formData };
          }
          
          this.showNotification('Autor actualizado correctamente', 'success');
        } else {
          // Crear Nuevo Autor
          const response = await axios.post(
            'http://127.0.0.1:8001/lib/api/autores/', 
            this.formData,
            { headers: this.getAuthHeaders() }
          );
          
          // Agregar a la lista local
          this.autors.push(response.data);
          
          this.showNotification('Autor agregado correctamente', 'success');
        }
        
        this.applyFilters();
        this.cancelModal();
      } catch (error) {
        console.error('Error al guardar el autor:', error);
        
        // Mostrar mensaje de error más específico
        let errorMessage = 'Ha ocurrido un error al guardar el autor';
        
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.status === 400 && error.response?.data) {
          // Manejar errores de validación del servidor
          const errors = error.response.data;
          const errorMessages = [];
          
          if (errors.dni) errorMessages.push(`DNI: ${errors.dni.join(', ')}`);
          if (errors.codigo) errorMessages.push(`Código: ${errors.codigo.join(', ')}`);
          if (errors.nombre) errorMessages.push(`Nombre: ${errors.nombre.join(', ')}`);
          if (errors.apellido_paterno) errorMessages.push(`Apellido Paterno: ${errors.apellido_paterno.join(', ')}`);
          if (errors.apellido_materno) errorMessages.push(`Apellido Materno: ${errors.apellido_materno.join(', ')}`);
          
          if (errorMessages.length > 0) {
            errorMessage = errorMessages.join(' | ');
          }
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
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
        }, 4000)
      };
    },

    applyFilters() {
      let result = [...this.autors];
      
      // Filtrar por texto de búsqueda
      if (this.filters.search) {
        const searchTerm = this.filters.search.toLowerCase();
        result = result.filter(autor => {
          return autor.dni.toLowerCase().includes(searchTerm) || 
                 autor.codigo.toLowerCase().includes(searchTerm) ||
                 autor.nombre.toLowerCase().includes(searchTerm) ||
                 autor.apellido_paterno.toLowerCase().includes(searchTerm) ||
                 autor.apellido_materno.toLowerCase().includes(searchTerm);
        });
      }
      
      // Filtrar por estado
      if (this.filters.status !== '') {
        const statusValue = this.filters.status === 'true';
        result = result.filter(autor => autor.flag === statusValue);
      }
      
      this.filteredAutores = result;
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

.detail-cell {
  text-align: center;
}

.btn-detail {
  background-color: #6b7280;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-detail:hover {
  background-color: #4b5563;
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

.required {
  color: #ef4444;
  font-weight: bold;
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
</style>