/**
 * Módulo principal de la cédula de votación
 */

const App = {
    // Datos cargados del backend
    datos: {
        presidente: null,
        senadorNacional: null,
        senadorRegional: null,
        diputado: null,
        parlamento: null
    },

    // Selecciones actuales por categoría
    selecciones: {
        presidente: { partido: null, candidatos: [] },
        'senador-nacional': { partido: null, candidatos: [] },
        'senador-regional': { partido: null, candidatos: [] },
        diputado: { partido: null, candidatos: [] },
        parlamento: { partido: null, candidatos: [] }
    },

    /**
     * Inicializa la aplicación
     */
    async init() {
        try {
            // Verificar que el DNI haya sido verificado
            if (!this.verificarSesion()) {
                return; // La función ya redirige
            }

            this.showLoading(true);

            // Verificar conexión con el servidor
            const connected = await API.checkConnection();
            if (!connected) {
                throw new Error('No se puede conectar con el servidor. Verifica que esté ejecutándose en http://localhost:5000');
            }

            // Cargar datos de todas las categorías
            await this.cargarDatos();

            // Renderizar las cédulas
            this.renderizarTodasLasCategorias();

            // Configurar eventos
            this.setupEventListeners();

            this.showLoading(false);
            this.showToast('Datos cargados correctamente', 'success');

        } catch (error) {
            console.error('Error al inicializar:', error);
            this.showLoading(false);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    },

    /**
     * Verifica que exista una sesión activa con DNI verificado
     * Si no existe, redirige a la página de verificación
     */
    verificarSesion() {
        const dniVerificado = sessionStorage.getItem('dniVerificado');

        if (!dniVerificado) {
            // No hay sesión activa, redirigir a verificación
            alert('Debe verificar su DNI antes de acceder a la votación.');
            window.location.href = 'verificacion.html';
            return false;
        }

        // Mostrar información del elector
        const electorData = sessionStorage.getItem('electorData');
        if (electorData) {
            try {
                const elector = JSON.parse(electorData);
                console.log('Sesión activa para:', elector.nombres, elector.apellidos, '- DNI:', dniVerificado);
            } catch (e) {
                console.error('Error al parsear datos del elector:', e);
            }
        }

        return true;
    },

    /**
     * Carga los datos de todas las categorías desde el backend
     */
    async cargarDatos() {
        try {
            const [presidente, senadorNacional, senadorRegional, diputado, parlamento] = await Promise.all([
                API.getCandidatosPorCategoria('Presidente'),
                API.getCandidatosPorCategoria('Senador Nacional'),
                API.getCandidatosPorCategoria('Senador Regional'),
                API.getCandidatosPorCategoria('Diputado'),
                API.getCandidatosPorCategoria('Parlamento')
            ]);

            this.datos.presidente = presidente;
            this.datos.senadorNacional = senadorNacional;
            this.datos.senadorRegional = senadorRegional;
            this.datos.diputado = diputado;
            this.datos.parlamento = parlamento;

        } catch (error) {
            console.error('Error cargando datos:', error);
            throw error;
        }
    },

    /**
     * Renderiza todas las categorías
     */
    renderizarTodasLasCategorias() {
        this.renderizarCategoria('presidentes-lista', this.datos.presidente, 'presidente', false);
        this.renderizarCategoria('senador-nacional-lista', this.datos.senadorNacional, 'senador-nacional', true);
        this.renderizarCategoria('senador-regional-lista', this.datos.senadorRegional, 'senador-regional', true);
        this.renderizarCategoria('diputado-lista', this.datos.diputado, 'diputado', true);
        this.renderizarCategoria('parlamento-lista', this.datos.parlamento, 'parlamento', true);
    },

    /**
     * Renderiza una categoría específica
     */
    renderizarCategoria(containerId, data, categoriaKey, tienePreferenciales) {
        const container = document.getElementById(containerId);
        if (!container || !data) return;

        container.innerHTML = '';

        for (const item of data.partidosConCandidatos) {
            const partidoItem = this.crearPartidoItem(item, categoriaKey, tienePreferenciales);
            container.appendChild(partidoItem);
        }
    },

    /**
     * Crea el elemento HTML para un partido
     */
    crearPartidoItem(item, categoriaKey, tienePreferenciales) {
        const { partido, candidatos } = item;

        const div = document.createElement('div');
        div.className = 'partido-item';
        div.dataset.categoriaKey = categoriaKey;
        div.dataset.partidoId = partido.id_partido;

        // Header del partido
        const partidoHeader = document.createElement('div');
        partidoHeader.className = 'partido-header';

        // Logo del partido
        const logoImg = document.createElement('img');
        logoImg.className = 'partido-logo';
        logoImg.src = partido.logo || 'images/default-logo.png';
        logoImg.alt = partido.nombre_partido;
        logoImg.onerror = () => {
            logoImg.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="30" height="30"%3E%3Crect fill="%23ddd" width="30" height="30"/%3E%3C/svg%3E';
        };

        // Nombre del partido
        const nombreSpan = document.createElement('span');
        nombreSpan.className = 'partido-nombre';
        nombreSpan.textContent = partido.nombre_partido;

        // Checkbox del partido
        const checkbox = document.createElement('div');
        checkbox.className = 'partido-checkbox';
        checkbox.dataset.partidoId = partido.id_partido;

        partidoHeader.appendChild(logoImg);
        partidoHeader.appendChild(nombreSpan);
        partidoHeader.appendChild(checkbox);

        div.appendChild(partidoHeader);

        // Si tiene preferenciales, agregar lista de candidatos
        if (tienePreferenciales && candidatos.length > 0) {
            const candidatosDiv = document.createElement('div');
            candidatosDiv.className = 'candidatos-preferenciales';
            candidatosDiv.dataset.partidoId = partido.id_partido;

            for (const candidato of candidatos) {
                if (candidato.numero_candidato) { // Solo mostrar candidatos con número
                    const candItem = this.crearCandidatoItem(candidato, categoriaKey);
                    candidatosDiv.appendChild(candItem);
                }
            }

            div.appendChild(candidatosDiv);
        }

        // Event listener para seleccionar partido
        partidoHeader.addEventListener('click', (e) => {
            this.togglePartido(categoriaKey, partido.id_partido, div);
        });

        return div;
    },

    /**
     * Crea el elemento HTML para un candidato preferencial
     */
    crearCandidatoItem(candidato, categoriaKey) {
        const div = document.createElement('div');
        div.className = 'candidato-item disabled';
        div.dataset.categoriaKey = categoriaKey;
        div.dataset.candidatoId = candidato.id_candidato;
        div.dataset.partidoId = candidato.id_partido;
        div.dataset.numeroCandidato = candidato.numero_candidato;

        const numeroSpan = document.createElement('span');
        numeroSpan.className = 'candidato-numero';
        numeroSpan.textContent = candidato.numero_candidato;

        const nombreSpan = document.createElement('span');
        nombreSpan.className = 'candidato-nombre';
        nombreSpan.textContent = candidato.nombre_candidato;

        const checkbox = document.createElement('div');
        checkbox.className = 'candidato-checkbox';

        div.appendChild(numeroSpan);
        div.appendChild(nombreSpan);
        div.appendChild(checkbox);

        // Event listener
        div.addEventListener('click', (e) => {
            e.stopPropagation();
            if (!div.classList.contains('disabled')) {
                this.toggleCandidato(categoriaKey, candidato, div);
            }
        });

        return div;
    },

    /**
     * Toggle selección de partido
     */
    togglePartido(categoriaKey, partidoId, element) {
        const seleccion = this.selecciones[categoriaKey];
        const checkbox = element.querySelector('.partido-checkbox');

        // Si ya está seleccionado, deseleccionar
        if (seleccion.partido === partidoId) {
            seleccion.partido = null;
            seleccion.candidatos = [];
            checkbox.classList.remove('checked');

            // Deshabilitar candidatos
            const candidatosDiv = element.querySelector('.candidatos-preferenciales');
            if (candidatosDiv) {
                candidatosDiv.classList.remove('visible');
                candidatosDiv.querySelectorAll('.candidato-item').forEach(item => {
                    item.classList.add('disabled');
                    item.querySelector('.candidato-checkbox').classList.remove('checked');
                });
            }
        } else {
            // Deseleccionar otros partidos de la misma categoría
            const container = element.parentElement;
            container.querySelectorAll('.partido-checkbox').forEach(cb => cb.classList.remove('checked'));
            container.querySelectorAll('.candidatos-preferenciales').forEach(div => {
                div.classList.remove('visible');
                div.querySelectorAll('.candidato-item').forEach(item => {
                    item.classList.add('disabled');
                    item.querySelector('.candidato-checkbox').classList.remove('checked');
                });
            });

            // Seleccionar nuevo partido
            seleccion.partido = partidoId;
            seleccion.candidatos = [];
            checkbox.classList.add('checked');

            // Habilitar candidatos de este partido
            const candidatosDiv = element.querySelector('.candidatos-preferenciales');
            if (candidatosDiv) {
                candidatosDiv.classList.add('visible');
                candidatosDiv.querySelectorAll('.candidato-item').forEach(item => {
                    item.classList.remove('disabled');
                });
            }
        }

        this.validarCategoria(categoriaKey);
    },

    /**
     * Toggle selección de candidato preferencial
     */
    toggleCandidato(categoriaKey, candidato, element) {
        const seleccion = this.selecciones[categoriaKey];
        const checkbox = element.querySelector('.candidato-checkbox');

        const index = seleccion.candidatos.findIndex(c => c.id_candidato === candidato.id_candidato);

        if (index !== -1) {
            // Deseleccionar
            seleccion.candidatos.splice(index, 1);
            checkbox.classList.remove('checked');
        } else {
            // Seleccionar
            const maxPreferenciales = VoteValidator.votosPorCategoria[categoriaKey].max_preferenciales;

            if (seleccion.candidatos.length >= maxPreferenciales) {
                this.showToast(VoteValidator.getMensajeError(categoriaKey, 'demasiados-preferenciales'), 'warning');
                element.classList.add('warning');
                setTimeout(() => element.classList.remove('warning'), 1000);
                return;
            }

            seleccion.candidatos.push(candidato);
            checkbox.classList.add('checked');
        }

        this.validarCategoria(categoriaKey);
    },

    /**
     * Valida una categoría y actualiza su estado
     */
    validarCategoria(categoriaKey) {
        const seleccion = this.selecciones[categoriaKey];
        let estado;

        if (categoriaKey === 'presidente') {
            estado = VoteValidator.validarPresidente(seleccion.partido);
        } else {
            estado = VoteValidator.validarCategoriaConPreferenciales(
                categoriaKey,
                seleccion.partido,
                seleccion.candidatos
            );
        }

        this.actualizarBadgeEstado(categoriaKey, estado);

        // Mostrar advertencia si es nulo
        if (estado === 'nulo') {
            let mensaje = 'Voto nulo en ' + VoteValidator.votosPorCategoria[categoriaKey].nombre;

            if (seleccion.candidatos.length > 0 && !seleccion.partido) {
                mensaje = VoteValidator.getMensajeError(categoriaKey, 'candidatos-sin-partido');
            } else if (seleccion.candidatos.length > VoteValidator.votosPorCategoria[categoriaKey].max_preferenciales) {
                mensaje = VoteValidator.getMensajeError(categoriaKey, 'demasiados-preferenciales');
            }

            this.showToast(mensaje, 'warning');
        }
    },

    /**
     * Actualiza el badge de estado de una categoría
     */
    actualizarBadgeEstado(categoriaKey, estado) {
        const validationItem = document.querySelector(`.validation-item[data-categoria="${categoriaKey}"]`);
        if (!validationItem) return;

        const badge = validationItem.querySelector('.estado-badge');
        badge.dataset.estado = estado;

        const textos = {
            'valido': 'Válido',
            'nulo': 'Nulo',
            'blanco': 'En Blanco'
        };

        badge.textContent = textos[estado] || 'En Blanco';
    },

    /**
     * Configura los event listeners de los botones
     */
    setupEventListeners() {
        // Botón reset
        document.getElementById('btnReset').addEventListener('click', () => {
            this.resetearTodo();
        });

        // Botón submit
        document.getElementById('btnSubmit').addEventListener('click', () => {
            this.mostrarModalConfirmacion();
        });

        // Modal de confirmación
        document.getElementById('btnCancelModal').addEventListener('click', () => {
            this.cerrarModal('confirmModal');
        });

        document.getElementById('btnConfirmSubmit').addEventListener('click', () => {
            this.enviarVoto();
        });

        // Modal de resultado
        document.getElementById('btnCloseResult').addEventListener('click', () => {
            this.cerrarModal('resultModal');

            // Si el voto fue exitoso, mostrar cuestionario
            if (this._mostrarCuestionarioPostVoto) {
                this._mostrarCuestionarioPostVoto = false;
                // Mostrar invitación al cuestionario después de un breve delay
                setTimeout(() => {
                    if (window.Cuestionario) {
                        Cuestionario.mostrarInvitacion();
                    }
                }, 500);
            }
        });
    },

    /**
     * Resetea todas las selecciones
     */
    resetearTodo() {
        // Limpiar selecciones
        for (const key in this.selecciones) {
            this.selecciones[key] = { partido: null, candidatos: [] };
        }

        // Limpiar validador
        VoteValidator.resetAll();

        // Limpiar UI
        document.querySelectorAll('.partido-checkbox').forEach(cb => cb.classList.remove('checked'));
        document.querySelectorAll('.candidato-checkbox').forEach(cb => cb.classList.remove('checked'));
        document.querySelectorAll('.candidatos-preferenciales').forEach(div => {
            div.classList.remove('visible');
            div.querySelectorAll('.candidato-item').forEach(item => item.classList.add('disabled'));
        });

        // Actualizar badges
        for (const key in this.selecciones) {
            this.actualizarBadgeEstado(key, 'blanco');
        }

        this.showToast('Todas las selecciones han sido limpiadas', 'success');
    },

    /**
     * Muestra el modal de confirmación
     */
    mostrarModalConfirmacion() {
        // Validar que no haya votos nulos sin resolver
        if (VoteValidator.hayVotosNulosSinResolver()) {
            this.showToast('Hay votos nulos. Por favor corrígelos antes de continuar.', 'error');
            return;
        }

        // Generar resumen
        const summary = VoteValidator.generarResumen();
        document.getElementById('modalSummary').innerHTML = `
            <p style="margin-bottom: 15px;">¿Confirmas tu voto con las siguientes selecciones?</p>
            ${summary}
            <style>
                .resumen-categoria { margin: 10px 0; }
                .badge-valido { background: #4caf50; color: white; padding: 2px 8px; border-radius: 3px; }
                .badge-nulo { background: #f44336; color: white; padding: 2px 8px; border-radius: 3px; }
                .badge-blanco { background: #9e9e9e; color: white; padding: 2px 8px; border-radius: 3px; }
            </style>
        `;

        this.abrirModal('confirmModal');
    },

    /**
     * Envía el voto al backend
     */
    async enviarVoto() {
        this.cerrarModal('confirmModal');
        this.showLoading(true);

        try {
            // Obtener DNI de la sesión verificada
            const dni = sessionStorage.getItem('dniVerificado');

            if (!dni || dni.length !== 8) {
                throw new Error('Sesión inválida. Por favor, verifique su DNI nuevamente.');
            }

            // Preparar votos
            const votosPorCategoria = VoteValidator.getVotosParaEnviar();

            // Enviar al backend
            const resultado = await API.registrarVoto(dni, votosPorCategoria);

            this.showLoading(false);

            // NO limpiar sesión aquí - se limpiará después de la encuesta o al omitirla

            // Mostrar resultado
            document.getElementById('resultTitle').textContent = '¡Voto Registrado Exitosamente!';
            document.getElementById('resultMessage').innerHTML = `
                <p>Tu voto ha sido registrado correctamente.</p>
                <p><strong>ID del voto:</strong> ${resultado.voto.id_voto}</p>
                <p><strong>Fecha:</strong> ${new Date(resultado.voto.fecha).toLocaleString('es-PE')}</p>
                <p><strong>Tipo de voto:</strong> ${resultado.voto.tipo_voto}</p>
            `;

            this.abrirModal('resultModal');

            // Resetear y mostrar cuestionario después de cerrar el modal de resultado
            this.resetearTodo();

            // Guardar referencia para mostrar cuestionario después
            this._mostrarCuestionarioPostVoto = true;

            // NO redirigir automáticamente - se redirigirá después de la encuesta

        } catch (error) {
            this.showLoading(false);
            console.error('Error al enviar voto:', error);

            // Manejar error de DNI duplicado
            if (error.type === 'DNI_YA_VOTO') {
                document.getElementById('resultTitle').textContent = 'DNI Ya Ha Votado';
                document.getElementById('resultMessage').innerHTML = `
                    <p style="color: #e65100;">${error.message}</p>
                    <p>Este DNI ya registró su voto anteriormente.</p>
                    <p style="font-size: 14px; color: #666;">Será redirigido a la página de verificación.</p>
                `;

                // Limpiar sesión y redirigir
                sessionStorage.removeItem('dniVerificado');
                sessionStorage.removeItem('electorData');

                setTimeout(() => {
                    window.location.href = 'verificacion.html';
                }, 3000);
            } else {
                document.getElementById('resultTitle').textContent = 'Error al Registrar Voto';
                document.getElementById('resultMessage').innerHTML = `
                    <p style="color: red;">${error.message || 'Error desconocido'}</p>
                    <p>Por favor, intenta nuevamente.</p>
                `;
            }

            this.abrirModal('resultModal');
        }
    },

    /**
     * Muestra/oculta el overlay de loading
     */
    showLoading(show) {
        let overlay = document.querySelector('.loading-overlay');

        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'loading-overlay';
            overlay.innerHTML = '<div class="spinner"></div>';
            document.body.appendChild(overlay);
        }

        if (show) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    },

    /**
     * Muestra un toast de notificación
     */
    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
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
    App.init();
});
