
const {createApp} = Vue

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            baseUrl: 'http://127.0.0.1:8000/',
            notes: [],
            notesForm: {
                note: '',
                errors: {},
            }
        }
    },
    methods: {
        getNotes() {
            const taskContainer = document.getElementById('task_container');
            let task_id = taskContainer.dataset.taskId;
            axios.get(`${this.baseUrl}/api/rest/tasks/${task_id}/notes`)
            .then(response => {
                this.notes = response.data.notes;
            })
        },

        toggleLike(event) {
            let task_id = document.getElementById('task_container').dataset.taskId;
            let note_id = event.currentTarget.dataset.noteId;

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            axios.post(`${this.baseUrl}/api/rest/tasks/${task_id}/notes/${note_id}/like`)
            .then(response => {
                this.getNotes();
            })
        },

        addNote() {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            const payload = this.notesForm;
            let task_id = document.getElementById('task_container').dataset.taskId;

            axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
            axios.post(`${this.baseUrl}/api/rest/tasks/${task_id}/notes/add`, payload)
            .then(response => {
                this.getNotes();
                this.notesForm.note = '';
                this.notesForm.errors = {};
            })
            .catch(error => {
                this.notesForm.errors = error.response.data
                console.log(this.notesForm.errors)
            })
        }
    },
    mounted() {
        this.getNotes();
    }
}).mount('#task')