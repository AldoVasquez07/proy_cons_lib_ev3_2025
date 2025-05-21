<template>
  <div class="crud-container">
    <div class="crud-header">
      <h2>Gestión de Libros</h2>
      <button @click="showAddModal = true" class="btn-add">
        <span class="btn-icon">+</span> Nuevo Libro
      </button>
    </div>

    <!-- Filtros de búsqueda -->
    <div class="filters-container">
      <div class="search-box">
        <input 
          v-model="filters.search" 
          type="text" 
          placeholder="Buscar por título o autor..." 
          class="search-input"
          @input="applyFilters"
        >
      </div>
      <div class="filter-selects">
        <div class="filter-group">
          <label for="genreFilter">Género:</label>
          <select v-model="filters.genre" id="genreFilter" class="filter-select" @change="applyFilters">
            <option value="">Todos los géneros</option>
            <option v-for="genre in genres" :key="genre.id" :value="genre.id">{{ genre.name }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label for="authorFilter">Autor:</label>
          <select v-model="filters.author" id="authorFilter" class="filter-select" @change="applyFilters">
            <option value="">Todos los autores</option>
            <option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Tabla de datos -->
    <div class="table-container">
      <table class="crud-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Autor</th>
            <th>Género</th>
            <th>Año</th>
            <th>ISBN</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredBooks.length === 0">
            <td colspan="7" class="empty-table">No hay libros que coincidan con la búsqueda</td>
          </tr>
          <tr v-for="book in filteredBooks" :key="book.id">
            <td>{{ book.id }}</td>
            <td>{{ book.title }}</td>
            <td>{{ getAuthorName(book.authorId) }}</td>
            <td>{{ getGenreName(book.genreId) }}</td>
            <td>{{ book.year }}</td>
            <td>{{ book.isbn }}</td>
            <td class="actions-cell">
              <button @click="editBook(book)" class="btn-edit">Editar</button>
              <button @click="confirmDelete(book)" class="btn-delete">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para agregar/editar libro -->
    <div v-if="showAddModal || showEditModal" class="modal-backdrop">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ showEditModal ? 'Editar Libro' : 'Nuevo Libro' }}</h3>
          <button @click="cancelModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="bookTitle">Título:</label>
            <input v-model="formData.title" id="bookTitle" type="text" class="form-control" required>
          </div>
          <div class="form-group">
            <label for="bookAuthor">Autor:</label>
            <select v-model="formData.authorId" id="bookAuthor" class="form-control" required>
              <option value="" disabled>Selecciona un autor</option>
              <option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option>
            </select>
            <div v-if="authors.length === 0" class="form-help-text">
              No hay autores disponibles. <a @click="goToAuthors" href="#" class="link">Agregar autor</a>
            </div>
          </div>
          <div class="form-group">
            <label for="bookGenre">Género:</label>
            <select v-model="formData.genreId" id="bookGenre" class="form-control" required>
              <option value="" disabled>Selecciona un género</option>
              <option v-for="genre in genres" :key="genre.id" :value="genre.id">{{ genre.name }}</option>
            </select>
            <div v-if="genres.length === 0" class="form-help-text">
              No hay géneros disponibles. <a @click="goToGenres" href="#" class="link">Agregar género</a>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group half-width">
              <label for="bookYear">Año de publicación:</label>
              <input v-model="formData.year" id="bookYear" type="number" min="1000" max="2099" class="form-control" required>
            </div>
            <div class="form-group half-width">
              <label for="bookISBN">ISBN:</label>
              <input v-model="formData.isbn" id="bookISBN" type="text" class="form-control">
            </div>
          </div>
          <div class="form-group">
            <label for="bookDescription">Descripción:</label>
            <textarea v-model="formData.description" id="bookDescription" class="form-control" rows="3"></textarea>
          </div>
          <div class="form-row">
            <div class="form-group half-width">
              <label for="bookPublisher">Editorial:</label>
              <input v-model="formData.publisher" id="bookPublisher" type="text" class="form-control">
            </div>
            <div class="form-group half-width">
              <label for="bookPages">Número de páginas:</label>
              <input v-model="formData.pages" id="bookPages" type="number" min="1" class="form-control">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="cancelModal" class="btn-cancel">Cancelar</button>
          <button @click="saveBook" class="btn-save">Guardar</button>
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
          <p>¿Estás seguro de que deseas eliminar el libro <strong>{{ bookToDelete?.title }}</strong>?</p>
          <p class="delete-warning">Esta acción no se puede deshacer.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn-cancel">Cancelar</button>
          <button @click="deleteBook" class="btn-confirm-delete">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookCrud',
  data() {
    return {
      books: [],
      filteredBooks: [],
      authors: [],
      genres: [],
      showAddModal: false,
      showEditModal: false,
      showDeleteModal: false,
      bookToDelete: null,
      formData: this.getEmptyFormData(),
      nextId: 1,
      filters: {
        search: '',
        author: '',
        genre: ''
      }
    };
  },
  mounted() {
    this.loadBooks();
    this.loadAuthors();
    this.loadGenres();
  },
  methods: {
    getEmptyFormData() {
      return {
        id: null,
        title: '',
        authorId: '',
        genreId: '',
        year: new Date().getFullYear(),
        isbn: '',
        description: '',
        publisher: '',
        pages: ''
      };
    },
    loadBooks() {
      // En una app real, aquí se haría una petición a la API
      try {
        const storedBooks = JSON.parse(localStorage.getItem('books')) || [];
        this.books = storedBooks;
        this.applyFilters();
        
        // Determinar el siguiente ID basado en los libros existentes
        if (this.books.length > 0) {
          this.nextId = Math.max(...this.books.map(b => b.id)) + 1;
        }
        
        this.$emit('update-stats');
      } catch (e) {
        console.error('Error al cargar libros:', e);
        this.books = [];
        this.filteredBooks = [];
      }
    },
    loadAuthors() {
      try {
        this.authors = JSON.parse(localStorage.getItem('authors')) || [];
      } catch (e) {
        console.error('Error al cargar autores:', e);
        this.authors = [];
      }
    },
    loadGenres() {
      try {
        this.genres = JSON.parse(localStorage.getItem('genres')) || [];
      } catch (e) {
        console.error('Error al cargar géneros:', e);
        this.genres = [];
      }
    },
    saveBooks() {
      // En una app real, aquí se haría una petición a la API
      localStorage.setItem('books', JSON.stringify(this.books));
      this.$emit('update-stats');
    },
    getAuthorName(authorId) {
      const author = this.authors.find(a => a.id === authorId);
      return author ? author.name : 'Desconocido';
    },
    getGenreName(genreId) {
      const genre = this.genres.find(g => g.id === genreId);
      return genre ? genre.name : 'Sin clasificar';
    },
    editBook(book) {
      this.formData = { ...book };
      this.showEditModal = true;
    },
    confirmDelete(book) {
      this.bookToDelete = book;
      this.showDeleteModal = true;
    },
    deleteBook() {
      if (!this.bookToDelete) return;
      
      this.books = this.books.filter(b => b.id !== this.bookToDelete.id);
      this.saveBooks();
      this.applyFilters();
      this.showDeleteModal = false;
      this.bookToDelete = null;
      
      // Mostrar notificación
      this.showNotification('Libro eliminado correctamente');
    },
    saveBook() {
      if (!this.formData.title || !this.formData.authorId || !this.formData.genreId || !this.formData.year) {
        alert('Por favor completa todos los campos requeridos');
        return;
      }
      
      if (this.showEditModal) {
        // Actualizar libro existente
        const index = this.books.findIndex(b => b.id === this.formData.id);
        if (index !== -1) {
          this.books[index] = { ...this.formData };
        }
      } else {
        // Crear nuevo libro
        const newBook = {
          ...this.formData,
          id: this.nextId++
        };
        this.books.push(newBook);
      }
      
      this.saveBooks();
      this.applyFilters();
      this.cancelModal();
      
      // Mostrar notificación
      this.showNotification(this.showEditModal ? 'Libro actualizado correctamente' : 'Libro agregado correctamente');
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
      let result = [...this.books];
      
      // Filtrar por texto de búsqueda (título o autor)
      if (this.filters.search) {
        const searchTerm = this.filters.search.toLowerCase();
        result = result.filter(book => {
          const authorName = this.getAuthorName(book.authorId).toLowerCase();
          return book.title.toLowerCase().includes(searchTerm) || 
                 authorName.includes(searchTerm);
        });
      }
      
      // Filtrar por autor
      if (this.filters.author) {
        result = result.filter(book => book.authorId === this.filters.author);
      }
      
      // Filtrar por género
      if (this.filters.genre) {
        result = result.filter(book => book.genreId === this.filters.genre);
      }
      
      this.filteredBooks = result;
    },
    goToAuthors() {
      // Emitir un evento para navegar a la sección de autores
      // En una app real, esto podría usar el router o notificar al componente padre
      this.$parent.navigateTo('authors');
      this.cancelModal();
    },
    goToGenres() {
      // Emitir un evento para navegar a la sección de géneros
      this.$parent.navigateTo('genres');
      this.cancelModal();
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

.form-row {
  display: flex;
  gap: 15px;
}

.half-width {
  flex: 1;
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

.form-help-text {
  margin-top: 5px;
  font-size: 0.85rem;
  color: #6b7280;
}

.link {
  color: #3b82f6;
  text-decoration: none;
  cursor: pointer;
}

.link:hover {
  text-decoration: underline;
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