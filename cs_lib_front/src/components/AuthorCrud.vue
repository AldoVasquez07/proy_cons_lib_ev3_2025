<template>
  <div class="crud-container">
    <div class="crud-header">
      <h2>Gestión de Autores</h2>
      <button @click="showAddModal = true" class="btn-add">
        <span class="btn-icon">+</span> Nuevo Autor
      </button>
    </div>

    <!-- Tabla de datos -->
    <div class="table-container">
      <table class="crud-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Nacionalidad</th>
            <th>Fecha de Nacimiento</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="authors.length === 0">
            <td colspan="5" class="empty-table">No hay autores registrados</td>
          </tr>
          <tr v-for="author in authors" :key="author.id">
            <td>{{ author.id }}</td>
            <td>{{ author.name }}</td>
            <td>{{ author.nationality }}</td>
            <td>{{ formatDate(author.birthDate) }}</td>
            <td class="actions-cell">
              <button @click="editAuthor(author)" class="btn-edit">Editar</button>
              <button @click="confirmDelete(author)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para agregar/editar autor -->
    <div v-if="showAddModal || showEditModal" class="modal-backdrop">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ showEditModal ? 'Editar Autor' : 'Nuevo Autor' }}</h3>
          <button @click="cancelModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="authorName">Nombre:</label>
            <input v-model="formData.name" id="authorName" type="text" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="authorNationality">Nacionalidad:</label>
            <input v-model="formData.nationality" id="authorNationality" type="text" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="authorBirthDate">Fecha de Nacimiento:</label>
            <input v-model="formData.birthDate" id="authorBirthDate" type="date" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="authorBio">Biografía:</label>
            <textarea v-model="formData.bio" id="authorBio" class="form-control" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="cancelModal" class="btn-cancel">Cancelar</button>
          <button @click="saveAuthor" class="btn-save">Guardar</button>
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
          <p>¿Estás seguro de que deseas eliminar al autor <strong>{{ authorToDelete?.name }}</strong>?</p>
          <p class="delete-warning">Esta acción no se puede deshacer.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn-cancel">Cancelar</button>
          <button @click="deleteAuthor" class="btn-confirm-delete">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthorCrud',
  data() {
    return {
      authors: [],
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      authorToDelete: null,
      formData: this.getEmptyFormData(),
      nextId: 1
    };
  },
  mounted() {
    this.loadAuthors();
  },
  methods: {
    getEmptyFormData() {
      return {
        id: null,
        name: '',
        nationality: '',
        birthDate: '',
        bio: ''
      };
    },
    loadAuthors() {
      // En una app real, aquí se haría una petición a la API
      try {
        const storedAuthors = JSON.parse(localStorage.getItem('authors')) || [];
        this.authors = storedAuthors;
        
        // Determinar el siguiente ID basado en los autores existentes
        if (this.authors.length > 0) {
          this.nextId = Math.max(...this.authors.map(a => a.id)) + 1;
        }
        
        this.$emit('update-stats');
      } catch (e) {
        console.error('Error al cargar autores:', e);
        this.authors = [];
      }
    },
    saveAuthors() {
      // En una app real, aquí se haría una petición a la API
      localStorage.setItem('authors', JSON.stringify(this.authors));
      this.$emit('update-stats');
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString;
      
      return date.toLocaleDateString();
    },
    editAuthor(author) {
      this.formData = { ...author };
      this.showEditModal = true;
    },
    confirmDelete(author) {
      this.authorToDelete = author;
      this.showDeleteModal = true;
    },
    deleteAuthor() {
      if (!this.authorToDelete) return;
      
      this.authors = this.authors.filter(a => a.id !== this.authorToDelete.id);
      this.saveAuthors();
      this.showDeleteModal = false;
      this.authorToDelete = null;
      
      // Mostrar notificación
      this.showNotification('Autor eliminado correctamente');
    },
    saveAuthor() {
      if (!this.formData.name || !this.formData.nationality || !this.formData.birthDate) {
        alert('Por favor completa todos los campos requeridos');
        return;
      }
      
      if (this.showEditModal) {
        // Actualizar autor existente
        const index = this.authors.findIndex(a => a.id === this.formData.id);
        if (index !== -1) {
          this.authors[index] = { ...this.formData };
        }
      } else {
        // Crear nuevo autor
        const newAuthor = {
          ...this.formData,
          id: this.nextId++
        };
        this.authors.push(newAuthor);
      }
      
      this.saveAuthors();
      this.cancelModal();
      
      // Mostrar notificación
      this.showNotification(this.showEditModal ? 'Autor actualizado correctamente' : 'Autor agregado correctamente');
    },
    cancelModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.formData = this.getEmptyFormData();
    },
    showNotification(message) {
      // En una app real, aquí se mostraría una notificación más elegante
      alert(message);
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