<template>
  <div class="detail-backdrop">
    <div class="detail-container">
      <!-- Header -->
      <div class="detail-header">
        <div class="header-content">
          <h2>Detalle del Libro</h2>
          <button @click="closeDetail" class="btn-close-detail">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Información del libro -->
      <div class="book-info-section">
        <div class="book-info-card">
          <h3>Información del Libro</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Código:</label>
              <span>{{ book.codigo }}</span>
            </div>
            <div class="info-item">
              <label>Nombre:</label>
              <span>{{ book.nombre }}</span>
            </div>
            <div class="info-item">
              <label>Fecha de Creación:</label>
              <span>{{ formatDate(book.fecha_creacion) }}</span>
            </div>
            <div class="info-item">
              <label>Estado:</label>
              <span :class="['status-badge', book.flag ? 'status-active' : 'status-inactive']">
                {{ book.flag ? 'Activo' : 'Inactivo' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección de autores -->
      <div class="authors-section">
        <div class="authors-header">
          <h3>Autores del Libro</h3>
          <button @click="showAddAuthorModal = true" class="btn-add-author">
            <span class="btn-icon">+</span> Agregar Autor
          </button>
        </div>

        <!-- Estado de carga de autores -->
        <div v-if="loadingAuthors" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Cargando autores...</p>
        </div>

        <!-- Lista de autores del libro -->
        <div v-if="!loadingAuthors" class="authors-list">
          <div v-if="bookAuthors.length === 0" class="empty-authors">
            <p>Este libro no tiene autores asignados</p>
          </div>
          <div v-else class="authors-grid">
            <div v-for="authorBook in bookAuthors" :key="authorBook.id" class="author-card">
              <div class="author-info">
                <h4>{{ authorBook.autor_nombre || 'Autor sin nombre' }}</h4>
                <p class="author-details">ID: {{ authorBook.autor }}</p>
                <span :class="['status-badge-small', authorBook.flag ? 'status-active' : 'status-inactive']">
                  {{ authorBook.flag ? 'Activo' : 'Inactivo' }}
                </span>
              </div>
              <div class="author-actions">
                <button 
                  v-if="authorBook.flag"
                  @click="confirmRemoveAuthor(authorBook)" 
                  class="btn-remove-author"
                  title="Desactivar autor del libro"
                >
                  Desactivar
                </button>
                <button 
                  v-else
                  @click="confirmReactivateAuthor(authorBook)" 
                  class="btn-reactivate-author"
                  title="Reactivar autor del libro"
                >
                  Reactivar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección de categorías -->
      <div class="categories-section">
        <div class="categories-header">
          <h3>Categorías del Libro</h3>
          <button @click="showAddCategoryModal = true" class="btn-add-category">
            <span class="btn-icon">+</span> Agregar Categoría
          </button>
        </div>

        <!-- Estado de carga de categorías -->
        <div v-if="loadingCategories" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Cargando categorías...</p>
        </div>

        <!-- Lista de categorías del libro -->
        <div v-if="!loadingCategories" class="categories-list">
          <div v-if="bookCategories.length === 0" class="empty-categories">
            <p>Este libro no tiene categorías asignadas</p>
          </div>
          <div v-else class="categories-grid">
            <div v-for="categoryBook in bookCategories" :key="categoryBook.id" class="category-card">
              <div class="category-info">
                <h4>{{ categoryBook.categoria_nombre || 'Categoría sin nombre' }}</h4>
                <p class="category-details">ID: {{ categoryBook.categoria }}</p>
                <span :class="['status-badge-small', categoryBook.flag ? 'status-active' : 'status-inactive']">
                  {{ categoryBook.flag ? 'Activo' : 'Inactivo' }}
                </span>
              </div>
              <div class="category-actions">
                <button 
                  v-if="categoryBook.flag"
                  @click="confirmRemoveCategory(categoryBook)" 
                  class="btn-remove-category"
                  title="Desactivar categoría del libro"
                >
                  Desactivar
                </button>
                <button 
                  v-else
                  @click="confirmReactivateCategory(categoryBook)" 
                  class="btn-reactivate-category"
                  title="Reactivar categoría del libro"
                >
                  Reactivar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal para agregar autor -->
      <div v-if="showAddAuthorModal" class="modal-backdrop">
        <div class="modal">
          <div class="modal-header">
            <h3>Agregar Autor al Libro</h3>
            <button @click="cancelAddAuthor" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="authorSelect">Seleccionar Autor:</label>
              <select v-model="selectedAuthorId" id="authorSelect" class="form-control">
                <option value="">-- Seleccione un autor --</option>
                <option 
                  v-for="author in availableAuthors" 
                  :key="author.id" 
                  :value="author.id"
                >
                  {{ author.nombre }} (ID: {{ author.id }})
                </option>
              </select>
            </div>
            <div v-if="loadingAvailableAuthors" class="loading-container">
              <div class="loading-spinner-small"></div>
              <p>Cargando autores disponibles...</p>
            </div>
            <div v-if="availableAuthors.length === 0 && !loadingAvailableAuthors" class="no-authors">
              <p>No hay autores disponibles para agregar</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="cancelAddAuthor" class="btn-cancel">Cancelar</button>
            <button 
              @click="addAuthorToBook" 
              class="btn-save" 
              :disabled="!selectedAuthorId || isAddingAuthor"
            >
              {{ isAddingAuthor ? 'Agregando...' : 'Agregar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal para agregar categoría -->
      <div v-if="showAddCategoryModal" class="modal-backdrop">
        <div class="modal">
          <div class="modal-header">
            <h3>Agregar Categoría al Libro</h3>
            <button @click="cancelAddCategory" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="categorySelect">Seleccionar Categoría:</label>
              <select v-model="selectedCategoryId" id="categorySelect" class="form-control">
                <option value="">-- Seleccione una categoría --</option>
                <option 
                  v-for="category in availableCategories" 
                  :key="category.id" 
                  :value="category.id"
                >
                  {{ category.nombre }} (ID: {{ category.id }})
                </option>
              </select>
            </div>
            <div v-if="loadingAvailableCategories" class="loading-container">
              <div class="loading-spinner-small"></div>
              <p>Cargando categorías disponibles...</p>
            </div>
            <div v-if="availableCategories.length === 0 && !loadingAvailableCategories" class="no-categories">
              <p>No hay categorías disponibles para agregar</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="cancelAddCategory" class="btn-cancel">Cancelar</button>
            <button 
              @click="addCategoryToBook" 
              class="btn-save" 
              :disabled="!selectedCategoryId || isAddingCategory"
            >
              {{ isAddingCategory ? 'Agregando...' : 'Agregar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación para desactivar autor -->
      <div v-if="showRemoveAuthorModal" class="modal-backdrop">
        <div class="modal delete-modal">
          <div class="modal-header">
            <h3>Confirmar Desactivación</h3>
            <button @click="showRemoveAuthorModal = false" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas desactivar el autor del libro?</p>
            <p class="delete-warning">La relación autor-libro será marcada como inactiva.</p>
          </div>
          <div class="modal-footer">
            <button @click="showRemoveAuthorModal = false" class="btn-cancel">Cancelar</button>
            <button @click="removeAuthorFromBook" class="btn-confirm-delete" :disabled="isRemovingAuthor">
              {{ isRemovingAuthor ? 'Desactivando...' : 'Desactivar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación para reactivar autor -->
      <div v-if="showReactivateAuthorModal" class="modal-backdrop">
        <div class="modal delete-modal">
          <div class="modal-header">
            <h3>Confirmar Reactivación</h3>
            <button @click="showReactivateAuthorModal = false" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas reactivar el autor del libro?</p>
          </div>
          <div class="modal-footer">
            <button @click="showReactivateAuthorModal = false" class="btn-cancel">Cancelar</button>
            <button @click="reactivateAuthorInBook" class="btn-confirm-reactivate" :disabled="isReactivatingAuthor">
              {{ isReactivatingAuthor ? 'Reactivando...' : 'Reactivar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación para desactivar categoría -->
      <div v-if="showRemoveCategoryModal" class="modal-backdrop">
        <div class="modal delete-modal">
          <div class="modal-header">
            <h3>Confirmar Desactivación</h3>
            <button @click="showRemoveCategoryModal = false" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas desactivar la categoría del libro?</p>
            <p class="delete-warning">La relación categoría-libro será marcada como inactiva.</p>
          </div>
          <div class="modal-footer">
            <button @click="showRemoveCategoryModal = false" class="btn-cancel">Cancelar</button>
            <button @click="removeCategoryFromBook" class="btn-confirm-delete" :disabled="isRemovingCategory">
              {{ isRemovingCategory ? 'Desactivando...' : 'Desactivar' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Modal de confirmación para reactivar categoría -->
      <div v-if="showReactivateCategoryModal" class="modal-backdrop">
        <div class="modal delete-modal">
          <div class="modal-header">
            <h3>Confirmar Reactivación</h3>
            <button @click="showReactivateCategoryModal = false" class="btn-close">×</button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas reactivar la categoría del libro?</p>
          </div>
          <div class="modal-footer">
            <button @click="showReactivateCategoryModal = false" class="btn-cancel">Cancelar</button>
            <button @click="reactivateCategoryInBook" class="btn-confirm-reactivate" :disabled="isReactivatingCategory">
              {{ isReactivatingCategory ? 'Reactivando...' : 'Reactivar' }}
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
  name: 'LibroDetail',
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      bookAuthors: [],
      bookCategories: [],
      availableAuthors: [],
      availableCategories: [],
      selectedAuthorId: '',
      selectedCategoryId: '',
      showAddAuthorModal: false,
      showAddCategoryModal: false,
      showRemoveAuthorModal: false,
      showReactivateAuthorModal: false,
      showRemoveCategoryModal: false,
      showReactivateCategoryModal: false,
      authorToRemove: null,
      authorToReactivate: null,
      categoryToRemove: null,
      categoryToReactivate: null,
      loadingAuthors: false,
      loadingCategories: false,
      loadingAvailableAuthors: false,
      loadingAvailableCategories: false,
      isAddingAuthor: false,
      isAddingCategory: false,
      isRemovingAuthor: false,
      isReactivatingAuthor: false,
      isRemovingCategory: false,
      isReactivatingCategory: false,
      notification: {
        show: false,
        message: '',
        type: 'success',
        timeout: null
      }
    };
  },
  mounted() {
    this.loadBookAuthors();
    this.loadBookCategories();
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

    // Métodos para autores
    async loadBookAuthors() {
      this.loadingAuthors = true;
      
      try {
        const response = await axios.get(
          `http://127.0.0.1:8001/lib/api/autor-libro/?libro=${this.book.id}`, 
          { headers: this.getAuthHeaders() }
        );
        this.bookAuthors = response.data;
      } catch (error) {
        console.error('Error al cargar autores del libro:', error);
        this.showNotification('Error al cargar los autores del libro', 'error');
      } finally {
        this.loadingAuthors = false;
      }
    },

    async loadAvailableAuthors() {
      this.loadingAvailableAuthors = true;
      
      try {
        const response = await axios.get(
          'http://127.0.0.1:8001/lib/api/autores/', 
          { headers: this.getAuthHeaders() }
        );
        
        const assignedAuthorIds = this.bookAuthors
          .filter(ab => ab.flag)
          .map(ab => ab.autor);
        
        this.availableAuthors = response.data.filter(author => 
          author.flag && !assignedAuthorIds.includes(author.id)
        );
      } catch (error) {
        console.error('Error al cargar autores disponibles:', error);
        this.showNotification('Error al cargar los autores disponibles', 'error');
      } finally {
        this.loadingAvailableAuthors = false;
      }
    },

    async addAuthorToBook() {
      if (!this.selectedAuthorId) return;
      
      this.isAddingAuthor = true;
      
      try {
        const authorBookData = {
          autor: parseInt(this.selectedAuthorId),
          libro: this.book.id,
          flag: true
        };

        const response = await axios.post(
          'http://127.0.0.1:8001/lib/api/autor-libro/',
          authorBookData,
          { headers: this.getAuthHeaders() }
        );

        this.bookAuthors.push(response.data);
        this.showNotification('Autor agregado correctamente al libro', 'success');
        this.cancelAddAuthor();
        
      } catch (error) {
        console.error('Error al agregar autor al libro:', error);
        
        let errorMessage = 'Error al agregar el autor al libro';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isAddingAuthor = false;
      }
    },

    confirmRemoveAuthor(authorBook) {
      this.authorToRemove = authorBook;
      this.showRemoveAuthorModal = true;
    },

    confirmReactivateAuthor(authorBook) {
      this.authorToReactivate = authorBook;
      this.showReactivateAuthorModal = true;
    },

    async removeAuthorFromBook() {
      if (!this.authorToRemove) return;
      
      this.isRemovingAuthor = true;
      
      try {
        const updateData = {
          ...this.authorToRemove,
          flag: false
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/autor-libro/${this.authorToRemove.id}/`,
          updateData,
          { headers: this.getAuthHeaders() }
        );

        const index = this.bookAuthors.findIndex(ab => ab.id === this.authorToRemove.id);
        if (index !== -1) {
          this.bookAuthors[index] = { ...this.bookAuthors[index], flag: false };
        }

        this.showNotification('Autor desactivado del libro correctamente', 'success');
        
      } catch (error) {
        console.error('Error al desactivar autor del libro:', error);
        
        let errorMessage = 'Error al desactivar el autor del libro';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isRemovingAuthor = false;
        this.showRemoveAuthorModal = false;
        this.authorToRemove = null;
      }
    },

    async reactivateAuthorInBook() {
      if (!this.authorToReactivate) return;
      
      this.isReactivatingAuthor = true;
      
      try {
        const updateData = {
          ...this.authorToReactivate,
          flag: true
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/autor-libro/${this.authorToReactivate.id}/`,
          updateData,
          { headers: this.getAuthHeaders() }
        );

        const index = this.bookAuthors.findIndex(ab => ab.id === this.authorToReactivate.id);
        if (index !== -1) {
          this.bookAuthors[index] = { ...this.bookAuthors[index], flag: true };
        }

        this.showNotification('Autor reactivado en el libro correctamente', 'success');
        
      } catch (error) {
        console.error('Error al reactivar autor en el libro:', error);
        
        let errorMessage = 'Error al reactivar el autor en el libro';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isReactivatingAuthor = false;
        this.showReactivateAuthorModal = false;
        this.authorToReactivate = null;
      }
    },

    cancelAddAuthor() {
      this.showAddAuthorModal = false;
      this.selectedAuthorId = '';
      this.availableAuthors = [];
    },

    // Métodos para categorías

    // Métodos para categorías (sección corregida)
    async loadBookCategories() {
      this.loadingCategories = true;
      
      try {
        const response = await axios.get(
          `http://127.0.0.1:8001/lib/api/libro-genero/?libro=${this.book.id}`, 
          { headers: this.getAuthHeaders() }
        );
        this.bookCategories = response.data;
      } catch (error) {
        console.error('Error al cargar categorías del libro:', error);
        this.showNotification('Error al cargar las categorías del libro', 'error');
      } finally {
        this.loadingCategories = false;
      }
    },

    async loadAvailableCategories() {
      this.loadingAvailableCategories = true;
      
      try {
        const response = await axios.get(
          'http://127.0.0.1:8001/lib/api/generos/', 
          { headers: this.getAuthHeaders() }
        );
        
        // Obtener IDs de categorías ya asignadas y activas
        const assignedCategoryIds = this.bookCategories
          .filter(cb => cb.flag)
          .map(cb => cb.genero || cb.categoria); // Compatibilidad con ambos nombres
        
        this.availableCategories = response.data.filter(category => 
          category.flag && !assignedCategoryIds.includes(category.id)
        );
      } catch (error) {
        console.error('Error al cargar categorías disponibles:', error);
        this.showNotification('Error al cargar las categorías disponibles', 'error');
      } finally {
        this.loadingAvailableCategories = false;
      }
    },

    async addCategoryToBook() {
      if (!this.selectedCategoryId) {
        this.showNotification('Por favor selecciona una categoría', 'error');
        return;
      }
      
      this.isAddingCategory = true;
      
      try {
        // Usar 'genero' en lugar de 'categoria' según la API
        const categoryBookData = {
          genero: parseInt(this.selectedCategoryId),
          libro: this.book.id,
          flag: true
        };

        console.log('Enviando datos:', categoryBookData); // Debug

        const response = await axios.post(
          'http://127.0.0.1:8001/lib/api/libro-genero/',
          categoryBookData,
          { headers: this.getAuthHeaders() }
        );

        this.bookCategories.push(response.data);
        this.showNotification('Categoría agregada correctamente al libro', 'success');
        this.cancelAddCategory();
        
      } catch (error) {
        console.error('Error al agregar categoría al libro:', error);
        
        let errorMessage = 'Error al agregar la categoría al libro';
        
        if (error.response?.status === 400) {
          // Error 400 - Bad Request
          if (error.response.data?.genero) {
            errorMessage = `Error en el campo género: ${error.response.data.genero.join(', ')}`;
          } else if (error.response.data?.libro) {
            errorMessage = `Error en el campo libro: ${error.response.data.libro.join(', ')}`;
          } else if (error.response.data?.non_field_errors) {
            errorMessage = error.response.data.non_field_errors.join(', ');
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          } else {
            errorMessage = 'Datos inválidos para crear la relación libro-género';
          }
        } else if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isAddingCategory = false;
      }
    },

    confirmRemoveCategory(categoryBook) {
      this.categoryToRemove = categoryBook;
      this.showRemoveCategoryModal = true;
    },

    confirmReactivateCategory(categoryBook) {
      this.categoryToReactivate = categoryBook;
      this.showReactivateCategoryModal = true;
    },

    async removeCategoryFromBook() {
      if (!this.categoryToRemove) return;
      
      this.isRemovingCategory = true;
      
      try {
        const updateData = {
          ...this.categoryToRemove,
          flag: false
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/libro-genero/${this.categoryToRemove.id}/`,
          updateData,
          { headers: this.getAuthHeaders() }
        );

        const index = this.bookCategories.findIndex(cb => cb.id === this.categoryToRemove.id);
        if (index !== -1) {
          this.bookCategories[index] = { ...this.bookCategories[index], flag: false };
        }

        this.showNotification('Categoría desactivada del libro correctamente', 'success');
        
      } catch (error) {
        console.error('Error al desactivar categoría del libro:', error);
        
        let errorMessage = 'Error al desactivar la categoría del libro';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isRemovingCategory = false;
        this.showRemoveCategoryModal = false;
        this.categoryToRemove = null;
      }
    },

    async reactivateCategoryInBook() {
      if (!this.categoryToReactivate) return;
      
      this.isReactivatingCategory = true;
      
      try {
        const updateData = {
          ...this.categoryToReactivate,
          flag: true
        };

        await axios.put(
          `http://127.0.0.1:8001/lib/api/libro-genero/${this.categoryToReactivate.id}/`,
          updateData,
          { headers: this.getAuthHeaders() }
        );

        const index = this.bookCategories.findIndex(cb => cb.id === this.categoryToReactivate.id);
        if (index !== -1) {
          this.bookCategories[index] = { ...this.bookCategories[index], flag: true };
        }

        this.showNotification('Categoría reactivada en el libro correctamente', 'success');
        
      } catch (error) {
        console.error('Error al reactivar categoría en el libro:', error);
        
        let errorMessage = 'Error al reactivar la categoría en el libro';
        if (error.response?.status === 401) {
          errorMessage = 'No tienes autorización para realizar esta acción';
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }
        
        this.showNotification(errorMessage, 'error');
      } finally {
        this.isReactivatingCategory = false;
        this.showReactivateCategoryModal = false;
        this.categoryToReactivate = null;
      }
    },

    cancelAddCategory() {
      this.showAddCategoryModal = false;
      this.selectedCategoryId = '';
      this.availableCategories = [];
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
    showAddAuthorModal(newVal) {
      if (newVal) {
        this.loadAvailableAuthors();
      }
    },
    showAddCategoryModal(newVal) {
      if (newVal) {
        this.loadAvailableCategories();
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

.book-info-section {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.book-info-card {
  background-color: #f9fafb;
  border-radius: 6px;
  padding: 20px;
}

.book-info-card h3 {
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

.authors-section {
  padding: 20px;
}

.authors-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.authors-header h3 {
  margin: 0;
  color: #374151;
}

.btn-add-author {
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

.btn-add-author:hover {
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

.empty-authors {
  text-align: center;
  padding: 40px 0;
  color: #6b7280;
  font-style: italic;
}

.authors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.author-card {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.author-info h4 {
  margin: 0 0 5px 0;
  color: #1f2937;
  font-size: 1rem;
}

.author-details {
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

.author-actions {
  display: flex;
  gap: 8px;
}

.btn-remove-author, .btn-reactivate-author {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-remove-author {
  background-color: #ef4444;
  color: white;
}

.btn-remove-author:hover {
  background-color: #dc2626;
}

.btn-reactivate-author {
  background-color: #10b981;
  color: white;
}

.btn-reactivate-author:hover {
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

.no-authors {
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

/* Estilos faltantes para la sección de categorías */

.categories-section {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.categories-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.categories-header h3 {
  margin: 0;
  color: #374151;
}

.btn-add-category {
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

.btn-add-category:hover {
  background-color: #059669;
}

.empty-categories {
  text-align: center;
  padding: 40px 0;
  color: #6b7280;
  font-style: italic;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.category-card {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.category-info h4 {
  margin: 0 0 5px 0;
  color: #1f2937;
  font-size: 1rem;
}

.category-details {
  margin: 0 0 8px 0;
  color: #6b7280;
  font-size: 0.85rem;
}

.category-actions {
  display: flex;
  gap: 8px;
}

.btn-remove-category, .btn-reactivate-category {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-remove-category {
  background-color: #ef4444;
  color: white;
}

.btn-remove-category:hover {
  background-color: #dc2626;
}

.btn-reactivate-category {
  background-color: #10b981;
  color: white;
}

.btn-reactivate-category:hover {
  background-color: #059669;
}

.no-categories {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-style: italic;
}
</style>