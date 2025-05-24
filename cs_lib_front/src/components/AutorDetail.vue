<template>
  <div class="detail-backdrop">
    <div class="detail-container">
      <!-- Header -->
      <div class="detail-header">
        <div class="header-content">
          <h2>Detalle del Autor</h2>
          <button @click="closeDetail" class="btn-close-detail">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Información del autor -->
      <div class="author-info-section">
        <div class="author-info-card">
          <h3>Información del Autor</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>ID:</label>
              <span>{{ autor.id }}</span>
            </div>
            <div class="info-item">
              <label>DNI:</label>
              <span>{{ autor.dni }}</span>
            </div>
            <div class="info-item">
              <label>Código:</label>
              <span>{{ autor.codigo }}</span>
            </div>
            <div class="info-item">
              <label>Nombre:</label>
              <span>{{ autor.nombre }}</span>
            </div>
            <div class="info-item">
              <label>Apellido Paterno:</label>
              <span>{{ autor.apellido_paterno }}</span>
            </div>
            <div class="info-item">
              <label>Apellido Materno:</label>
              <span>{{ autor.apellido_materno }}</span>
            </div>
            <div class="info-item">
              <label>Fecha de Creación:</label>
              <span>{{ formatDate(autor.fecha_creacion) }}</span>
            </div>
            <div class="info-item">
              <label>Estado:</label>
              <span :class="['status-badge', autor.flag ? 'status-active' : 'status-inactive']">
                {{ autor.flag ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección de libros -->
      <div class="books-section">
        <div class="books-header">
          <h3>Libros del Autor</h3>
          <button @click="showAddBookModal = true" class="btn-add-book">
            <span class="btn-icon">+</span> Agregar Libro
          </button>
        </div>

        <!-- Estado de carga de libros -->
        <div v-if="loadingBooks" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Cargando libros...</p>
        </div>

        <!-- Lista de libros del autor -->
        <div v-if="!loadingBooks" class="books-list">
          <div v-if="authorBooks.length === 0" class="empty-books">
            <p>Este autor no tiene libros asignados</p>
          </div>
          <div v-else class="books-grid">
            <div v-for="authorBook in authorBooks" :key="authorBook.id" class="book-card">
              <div class="book-info">
                <h4>{{ authorBook.libro_detalle.nombre || 'Libro sin nombre' }}</h4>
                <p class="book-details">
                  Código: {{ authorBook.libro_detalle.codigo || 'N/A' }}
                </p>
                <p class="book-details">
                  ID Libro: {{ authorBook.libro }}
                </p>
                <span :class="['status-badge-small', authorBook.flag ? 'status-active' : 'status-inactive']">
                  {{ authorBook.flag ? 'Activo' : 'Inactivo' }}
                </span>
              </div>
              <div class="book-actions">
                <button 
                  v-if="authorBook.flag"
                  @click="confirmRemoveBook(authorBook)" 
                  class="btn-remove-book"
                  title="Desactivar libro del autor"
                >
                  Desactivar
                </button>
                <button 
                  v-else
                  @click="confirmReactivateBook(authorBook)" 
                  class="btn-reactivate-book"
                  title="Reactivar libro del autor"
                >
                  Reactivar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal para agregar libro -->
      <div v-if="showAddBookModal" class="modal-backdrop">
        <div class="modal">
          <div class="modal-header">
            <h3>Agregar Libro al Autor</h3>
            <button @click="cancelAddBook" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="bookSelect">Seleccionar Libro:</label>
              <select v-model="selectedBookId" id="bookSelect" class="form-control">
                <option value="">-- Seleccione un libro --</option>
                <option 
                  v-for="book in availableBooks" 
                  :key="book.id" 
                  :value="book.id"
                >
                  {{ book.nombre }} - {{ book.codigo }} (ID: {{ book.id }})
                </option>
              </select>
            </div>
            <div v-if="loadingAvailableBooks" class="loading-container">
              <div class="loading-spinner-small"></div>
              <p>Cargando libros disponibles...</p>
            </div>
            <div v-if="availableBooks.length === 0 && !loadingAvailableBooks" class="no-books">
              <p>No hay libros disponibles para agregar</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="cancelAddBook" class="btn-cancel">Cancelar</button>
            <button 
              @click="addBookToAuthor" 
              class="btn-save" 
              :disabled="!selectedBookId || isAddingBook"
            >
              {{ isAddingBook ? 'Agregando...' : 'Agregar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación para desactivar libro -->
      <div v-if="showRemoveBookModal" class="modal-backdrop">
        <div class="modal delete-modal">
          <div class="modal-header">
            <h3>Confirmar Desactivación</h3>
            <button @click="showRemoveBookModal = false" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas desactivar el libro del autor?</p>
            <p class="delete-warning">La relación autor-libro será marcada como inactiva.</p>
          </div>
          <div class="modal-footer">
            <button @click="showRemoveBookModal = false" class="btn-cancel">Cancelar</button>
            <button @click="removeBookFromAuthor" class="btn-confirm-delete" :disabled="isRemovingBook">
              {{ isRemovingBook ? 'Desactivando...' : 'Desactivar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación para reactivar libro -->
      <div v-if="showReactivateBookModal" class="modal-backdrop">
        <div class="modal delete-modal">
          <div class="modal-header">
            <h3>Confirmar Reactivación</h3>
            <button @click="showReactivateBookModal = false" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas reactivar el libro del autor?</p>
          </div>
          <div class="modal-footer">
            <button @click="showReactivateBookModal = false" class="btn-cancel">Cancelar</button>
            <button @click="reactivateBookInAuthor" class="btn-confirm-reactivate" :disabled="isReactivatingBook">
              {{ isReactivatingBook ? 'Reactivando...' : 'Reactivar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Notificación -->
      <div v-if="notification.show" :class="['notification', `notification-${notification.type}`]">
        {{ notification.message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AutorDetail',
  props: {
    autor: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      authorBooks: [],
      availableBooks: [],
      selectedBookId: '',
      showAddBookModal: false,
      showRemoveBookModal: false,
      showReactivateBookModal: false,
      bookToRemove: null,
      bookToReactivate: null,
      loadingBooks: false,
      loadingAvailableBooks: false,
      isAddingBook: false,
      isRemovingBook: false,
      isReactivatingBook: false,
      notification: {
        show: false,
        message: '',
        type: 'success',
        timeout: null
      }
    };
  },
  mounted() {
    this.loadAuthorBooks();
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };
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

    async loadAuthorBooks() {
      this.loadingBooks = true;
      
      try {
        // Cargar libros del autor específico
        const response = await axios.get(
          `http://127.0.0.1:8001/lib/api/autor-libro/?autor=${this.autor.id}`, 
          { headers: this.getAuthHeaders() }
        );
        this.authorBooks = response.data;
      } catch (error) {
        console.error('Error al cargar libros del autor:', error);
        this.showNotification('Error al cargar los libros del autor', 'error');
      } finally {
        this.loadingBooks = false;
      }
    },

    async loadAvailableBooks() {
      this.loadingAvailableBooks = true;
      
      try {
        // Cargar todos los libros disponibles
        const response = await axios.get(
          'http://127.0.0.1:8001/lib/api/libros/', 
          { headers: this.getAuthHeaders() }
        );
        
        // Filtrar libros que ya están asignados al autor (activos)
        const assignedBookIds = this.authorBooks
          .filter(ab => ab.flag)
          .map(ab => ab.libro);
        
        this.availableBooks = response.data.filter(book => 
          book.flag && !assignedBookIds.includes(book.id)
        );
      } catch (error) {
        console.error('Error al cargar libros disponibles:', error);
        this.showNotification('Error al cargar los libros disponibles', 'error');
      } finally {
        this.loadingAvailableBooks = false;
      }
    },

    async addBookToAuthor() {
      if (!this.selectedBookId) return;
      
      this.isAddingBook = true;
      
      try {
        const authorBookData = {
          autor: this.autor.id,
          libro: parseInt(this.selectedBookId),
          flag: true
        };

        const response = await axios.post(
          'http://127.0.0.1:8001/lib/api/autor-libro/',
          authorBookData,
          { headers: this.getAuthHeaders() }
        );

        // Agregar el nuevo autor-libro a la lista
        this.authorBooks.push(response.data);
        
        this.showNotification('Libro agregado correctamente al autor', 'success');
        this.cancelAddBook();
        
      } catch (error) {
        console.error('Error al agregar libro al autor:', error);
        
        let errorMessage = 'Error al agregar el libro al autor';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isAddingBook = false;
      }
    },

    confirmRemoveBook(authorBook) {
      this.bookToRemove = authorBook;
      this.showRemoveBookModal = true;
    },

    confirmReactivateBook(authorBook) {
      this.bookToReactivate = authorBook;
      this.showReactivateBookModal = true;
    },

    async removeBookFromAuthor() {
      if (!this.bookToRemove) return;
      
      this.isRemovingBook = true;
      
      try {
        const updateData = {
          ...this.bookToRemove,
          flag: false
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/autor-libro/${this.bookToRemove.id}/`,
          updateData,
          { headers: this.getAuthHeaders() }
        );

        // Actualizar en la lista local
        const index = this.authorBooks.findIndex(ab => ab.id === this.bookToRemove.id);
        if (index !== -1) {
          this.authorBooks[index] = { ...this.authorBooks[index], flag: false };
        }

        this.showNotification('Libro desactivado del autor correctamente', 'success');
        
      } catch (error) {
        console.error('Error al desactivar libro del autor:', error);
        
        let errorMessage = 'Error al desactivar el libro del autor';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isRemovingBook = false;
        this.showRemoveBookModal = false;
        this.bookToRemove = null;
      }
    },

    async reactivateBookInAuthor() {
      if (!this.bookToReactivate) return;
      
      this.isReactivatingBook = true;
      
      try {
        const updateData = {
          ...this.bookToReactivate,
          flag: true
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/autor-libro/${this.bookToReactivate.id}/`,
          updateData,
          { headers: this.getAuthHeaders() }
        );

        // Actualizar en la lista local
        const index = this.authorBooks.findIndex(ab => ab.id === this.bookToReactivate.id);
        if (index !== -1) {
          this.authorBooks[index] = { ...this.authorBooks[index], flag: true };
        }

        this.showNotification('Libro reactivado en el autor correctamente', 'success');
        
      } catch (error) {
        console.error('Error al reactivar libro en el autor:', error);
        
        let errorMessage = 'Error al reactivar el libro en el autor';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isReactivatingBook = false;
        this.showReactivateBookModal = false;
        this.bookToReactivate = null;
      }
    },

    cancelAddBook() {
      this.showAddBookModal = false;
      this.selectedBookId = '';
      this.availableBooks = [];
    },

    async openAddBookModal() {
      this.showAddBookModal = true;
      await this.loadAvailableBooks();
    },

    closeDetail() {
      this.$emit('close');
    },

    showNotification(message, type = 'success') {
      if (this.notification.timeout) {
        clearTimeout(this.notification.timeout);
      }
      
      this.notification = {
        show: true,
        message,
        type,
        timeout: setTimeout(() => {
          this.notification.show = false;
        }, 3000)
      };
    }
  },

  watch: {
    showAddBookModal(newVal) {
      if (newVal) {
        this.loadAvailableBooks();
      }
    }
  }
};
</script>

<style scoped>
.detail-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  overflow-y: auto;
  padding: 20px;
}

.detail-container {
  background-color: white;
  border-radius: 8px;
  max-width: 1000px;
  margin: 0 auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.detail-header {
  background-color: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  border-radius: 8px 8px 0 0;
  padding: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
  color: #1e40af;
}

.btn-close-detail {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.btn-close-detail:hover {
  background-color: #e5e7eb;
}

.author-info-section {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.author-info-card {
  background-color: #f9fafb;
  border-radius: 6px;
  padding: 20px;
}

.author-info-card h3 {
  margin: 0 0 15px 0;
  color: #374151;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item label {
  font-weight: 600;
  color: #4b5563;
  font-size: 0.9rem;
}

.info-item span {
  color: #1f2937;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  width: fit-content;
}

.status-active {
  background-color: #d1fae5;
  color: #065f46;
}

.status-inactive {
  background-color: #fef2f2;
  color: #991b1b;
}

.books-section {
  padding: 20px;
}

.books-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.books-header h3 {
  margin: 0;
  color: #374151;
}

.btn-add-book {
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

.btn-add-book:hover {
  background-color: #059669;
}

.btn-icon {
  font-size: 1.1rem;
  margin-right: 6px;
}

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

.loading-spinner-small {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-books {
  text-align: center;
  padding: 40px 0;
  color: #6b7280;
  font-style: italic;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.book-card {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.book-info h4 {
  margin: 0 0 5px 0;
  color: #1f2937;
  font-size: 1rem;
}

.book-details {
  margin: 0 0 8px 0;
  color: #6b7280;
  font-size: 0.85rem;
}

.status-badge-small {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 500;
}

.book-actions {
  display: flex;
  gap: 8px;
}

.btn-remove-book, .btn-reactivate-book {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-remove-book {
  background-color: #ef4444;
  color: white;
}

.btn-remove-book:hover {
  background-color: #dc2626;
}

.btn-reactivate-book {
  background-color: #10b981;
  color: white;
}

.btn-reactivate-book:hover {
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
  z-index: 2000;
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

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.no-books {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-style: italic;
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
  z-index: 3000;
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