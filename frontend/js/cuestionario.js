/**
 * Módulo de Cuestionario de Conocimiento Ciudadano
 *
 * RESTRICCIONES ÉTICAS:
 * - Completamente independiente del sistema de votación
 * - No almacena DNI, id_voto, IP ni datos identificables
 * - No muestra feedback sobre respuestas correctas
 * - Es completamente opcional para el elector
 */

const Cuestionario = {
    // Estado del cuestionario
    estado: {
        preguntas: [],
        respuestas: {},  // { id_pregunta: id_opcion }
        activo: false,
        enviado: false
    },

    /**
     * Inicializa el módulo de cuestionario
     */
    init() {
        this.setupEventListeners();
    },

    /**
     * Configura los event listeners
     */
    setupEventListeners() {
        // Botón para aceptar el cuestionario
        const btnAceptar = document.getElementById('btnAceptarCuestionario');
        if (btnAceptar) {
            btnAceptar.addEventListener('click', () => this.aceptarCuestionario());
        }

        // Botón para omitir el cuestionario
        const btnOmitir = document.getElementById('btnOmitirCuestionario');
        if (btnOmitir) {
            btnOmitir.addEventListener('click', () => this.omitirCuestionario());
        }

        // Botón para enviar respuestas
        const btnEnviar = document.getElementById('btnEnviarCuestionario');
        if (btnEnviar) {
            btnEnviar.addEventListener('click', () => this.enviarCuestionario());
        }

        // Botón para cerrar mensaje final
        const btnCerrarFinal = document.getElementById('btnCerrarCuestionarioFinal');
        if (btnCerrarFinal) {
            btnCerrarFinal.addEventListener('click', () => this.cerrarCuestionario());
        }
    },

    /**
     * Muestra la invitación al cuestionario después de votar exitosamente
     * Se llama desde main.js después de registrar el voto
     */
    mostrarInvitacion() {
        // Resetear estado
        this.estado = {
            preguntas: [],
            respuestas: {},
            activo: false,
            enviado: false
        };

        const modal = document.getElementById('cuestionarioInvitacionModal');
        if (modal) {
            modal.classList.add('show');
        }
    },

    /**
     * Usuario acepta responder el cuestionario
     */
    async aceptarCuestionario() {
        this.cerrarModal('cuestionarioInvitacionModal');

        try {
            // Cargar preguntas del backend
            await this.cargarPreguntas();

            // Mostrar el cuestionario
            this.renderizarCuestionario();
            this.abrirModal('cuestionarioModal');
            this.estado.activo = true;

        } catch (error) {
            console.error('Error al cargar cuestionario:', error);
            this.mostrarError('No se pudo cargar el cuestionario. Por favor, intenta más tarde.');
        }
    },

    /**
     * Usuario omite el cuestionario
     */
    omitirCuestionario() {
        this.cerrarModal('cuestionarioInvitacionModal');

        // Limpiar sesión y redirigir después de omitir
        sessionStorage.removeItem('dniVerificado');
        sessionStorage.removeItem('electorData');

        this.mostrarMensajeFinal('Gracias por participar en el proceso electoral. Será redirigido en unos momentos.');
    },

    /**
     * Carga las preguntas del backend
     */
    async cargarPreguntas() {
        const response = await fetch('http://localhost:5000/api/preguntas/');
        if (!response.ok) {
            throw new Error('Error al cargar preguntas');
        }
        this.estado.preguntas = await response.json();
    },

    /**
     * Renderiza el cuestionario en el modal
     */
    renderizarCuestionario() {
        const container = document.getElementById('preguntasContainer');
        if (!container) return;

        container.innerHTML = '';

        this.estado.preguntas.forEach((pregunta, index) => {
            const preguntaDiv = document.createElement('div');
            preguntaDiv.className = 'pregunta-item';
            preguntaDiv.dataset.preguntaId = pregunta.id_pregunta;

            // Número y texto de la pregunta
            const preguntaHeader = document.createElement('div');
            preguntaHeader.className = 'pregunta-header';
            preguntaHeader.innerHTML = `
                <span class="pregunta-numero">${index + 1}.</span>
                <span class="pregunta-texto">${pregunta.texto}</span>
            `;
            preguntaDiv.appendChild(preguntaHeader);

            // Opciones
            const opcionesDiv = document.createElement('div');
            opcionesDiv.className = 'opciones-container';

            pregunta.opciones.forEach(opcion => {
                const opcionLabel = document.createElement('label');
                opcionLabel.className = 'opcion-item';
                opcionLabel.innerHTML = `
                    <input type="radio"
                           name="pregunta_${pregunta.id_pregunta}"
                           value="${opcion.id_opcion}"
                           data-pregunta-id="${pregunta.id_pregunta}">
                    <span class="opcion-radio"></span>
                    <span class="opcion-texto">${opcion.texto}</span>
                `;

                // Event listener para selección
                const radio = opcionLabel.querySelector('input');
                radio.addEventListener('change', (e) => {
                    this.seleccionarOpcion(pregunta.id_pregunta, opcion.id_opcion);
                });

                opcionesDiv.appendChild(opcionLabel);
            });

            preguntaDiv.appendChild(opcionesDiv);
            container.appendChild(preguntaDiv);
        });

        // Actualizar progreso inicial
        this.actualizarProgreso();
    },

    /**
     * Registra la selección de una opción
     */
    seleccionarOpcion(idPregunta, idOpcion) {
        this.estado.respuestas[idPregunta] = idOpcion;
        this.actualizarProgreso();
    },

    /**
     * Actualiza el indicador de progreso
     */
    actualizarProgreso() {
        const total = this.estado.preguntas.length;
        const respondidas = Object.keys(this.estado.respuestas).length;

        const progressText = document.getElementById('cuestionarioProgreso');
        if (progressText) {
            progressText.textContent = `${respondidas} de ${total} preguntas respondidas`;
        }

        // Habilitar/deshabilitar botón de enviar
        const btnEnviar = document.getElementById('btnEnviarCuestionario');
        if (btnEnviar) {
            btnEnviar.disabled = respondidas < total;
            if (respondidas < total) {
                btnEnviar.title = `Responde todas las preguntas (faltan ${total - respondidas})`;
            } else {
                btnEnviar.title = 'Enviar cuestionario';
            }
        }
    },

    /**
     * Envía el cuestionario al backend
     */
    async enviarCuestionario() {
        // Validar que todas las preguntas están respondidas
        if (Object.keys(this.estado.respuestas).length < this.estado.preguntas.length) {
            alert('Por favor, responde todas las preguntas antes de enviar.');
            return;
        }

        try {
            // Preparar datos para enviar
            const respuestasArray = Object.entries(this.estado.respuestas).map(([idPregunta, idOpcion]) => ({
                id_pregunta: parseInt(idPregunta),
                id_opcion: parseInt(idOpcion)
            }));

            const response = await fetch('http://localhost:5000/api/cuestionarios/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    respuestas: respuestasArray
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Error al enviar cuestionario');
            }

            this.estado.enviado = true;
            this.cerrarModal('cuestionarioModal');

            // Limpiar sesión después de enviar el cuestionario
            sessionStorage.removeItem('dniVerificado');
            sessionStorage.removeItem('electorData');

            this.mostrarMensajeFinal('¡Gracias por completar el cuestionario de conocimiento ciudadano! Será redirigido en unos momentos.');

        } catch (error) {
            console.error('Error al enviar cuestionario:', error);
            this.mostrarError('No se pudo enviar el cuestionario. Por favor, intenta nuevamente.');
        }
    },

    /**
     * Muestra el mensaje final
     */
    mostrarMensajeFinal(mensaje) {
        const mensajeElement = document.getElementById('cuestionarioMensajeFinal');
        if (mensajeElement) {
            mensajeElement.textContent = mensaje;
        }
        this.abrirModal('cuestionarioFinalModal');
    },

    /**
     * Cierra el cuestionario completamente y redirige a verificación
     */
    cerrarCuestionario() {
        this.cerrarModal('cuestionarioFinalModal');
        this.estado.activo = false;

        // Redirigir a la página de verificación
        setTimeout(() => {
            window.location.href = 'verificacion.html';
        }, 500);
    },

    /**
     * Muestra un mensaje de error
     */
    mostrarError(mensaje) {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = mensaje;
            toast.className = 'toast show error';
            setTimeout(() => toast.classList.remove('show'), 5000);
        }
    },

    /**
     * Abre un modal
     */
    abrirModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('show');
    },

    /**
     * Cierra un modal
     */
    cerrarModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('show');
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    Cuestionario.init();
});

// Exportar para uso en otros módulos
window.Cuestionario = Cuestionario;
