/**
 * Módulo de verificación de DNI
 * Verifica si un DNI existe y si ya ha votado antes de permitir acceso a la votación
 */

const API_BASE_URL = 'http://localhost:5000/api';

// Elementos del DOM
const formVerificacion = document.getElementById('formVerificacion');
const inputDNI = document.getElementById('inputDNI');
const inputHelper = document.getElementById('inputHelper');
const btnVerificar = document.getElementById('btnVerificar');
const mensajeEstado = document.getElementById('mensajeEstado');
const loadingSpinner = document.getElementById('loadingSpinner');
const toast = document.getElementById('toast');

/**
 * Inicialización
 */
document.addEventListener('DOMContentLoaded', () => {
    // Verificar si ya hay una sesión activa
    verificarSesionActiva();

    // Event listeners
    formVerificacion.addEventListener('submit', handleSubmit);
    inputDNI.addEventListener('input', handleInputChange);
    inputDNI.addEventListener('keypress', handleKeyPress);

    // Enfocar el input
    inputDNI.focus();
});

/**
 * Verifica si ya existe una sesión activa con DNI verificado
 */
function verificarSesionActiva() {
    const dniVerificado = sessionStorage.getItem('dniVerificado');

    if (dniVerificado) {
        mostrarMensaje(
            'info',
            'Sesión activa detectada',
            `Ya tiene una sesión activa con el DNI ${dniVerificado}. Redirigiendo a la votación...`
        );

        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
    }
}

/**
 * Maneja el cambio en el input de DNI
 */
function handleInputChange(e) {
    // Solo permitir números
    e.target.value = e.target.value.replace(/[^0-9]/g, '');

    // Validar longitud
    const dni = e.target.value;

    if (dni.length === 0) {
        inputHelper.textContent = 'Ingrese exactamente 8 dígitos';
        inputHelper.classList.remove('error');
        inputDNI.classList.remove('error', 'success');
    } else if (dni.length < 8) {
        inputHelper.textContent = `Faltan ${8 - dni.length} dígitos`;
        inputHelper.classList.add('error');
        inputDNI.classList.add('error');
        inputDNI.classList.remove('success');
    } else if (dni.length === 8) {
        inputHelper.textContent = '✓ DNI válido';
        inputHelper.classList.remove('error');
        inputDNI.classList.remove('error');
        inputDNI.classList.add('success');
    }
}

/**
 * Maneja la tecla presionada en el input
 */
function handleKeyPress(e) {
    // Solo permitir números
    if (!/[0-9]/.test(e.key) && e.key !== 'Enter' && e.key !== 'Backspace') {
        e.preventDefault();
    }
}

/**
 * Maneja el envío del formulario
 */
async function handleSubmit(e) {
    e.preventDefault();

    const dni = inputDNI.value.trim();

    // Validar DNI
    if (!validarDNI(dni)) {
        return;
    }

    // Verificar DNI
    await verificarDNI(dni);
}

/**
 * Valida el formato del DNI
 */
function validarDNI(dni) {
    if (dni.length !== 8) {
        mostrarToast('error', 'El DNI debe tener exactamente 8 dígitos');
        inputDNI.classList.add('error');
        inputDNI.focus();
        return false;
    }

    if (!/^\d{8}$/.test(dni)) {
        mostrarToast('error', 'El DNI solo debe contener números');
        inputDNI.classList.add('error');
        inputDNI.focus();
        return false;
    }

    return true;
}

/**
 * Verifica el DNI en el backend
 */
async function verificarDNI(dni) {
    try {
        // Mostrar loading
        mostrarLoading(true);
        ocultarMensaje();
        btnVerificar.disabled = true;

        // Llamar al endpoint de verificación
        const response = await fetch(`${API_BASE_URL}/electores/verificar/${dni}`);

        if (!response.ok) {
            throw new Error('Error al conectar con el servidor');
        }

        const resultado = await response.json();

        // Procesar resultado
        procesarResultado(dni, resultado);

    } catch (error) {
        console.error('Error al verificar DNI:', error);
        mostrarMensaje(
            'error',
            'Error de conexión',
            'No se pudo conectar con el servidor. Por favor, verifique que el servidor esté ejecutándose e intente nuevamente.'
        );
        mostrarToast('error', 'Error al verificar DNI');
    } finally {
        mostrarLoading(false);
        btnVerificar.disabled = false;
    }
}

/**
 * Procesa el resultado de la verificación
 */
function procesarResultado(dni, resultado) {
    const { exists, has_voted, elector, message } = resultado;

    if (!exists) {
        // DNI no existe en la base de datos
        mostrarMensaje(
            'error',
            'DNI no registrado',
            'El DNI ingresado no se encuentra registrado en la base de datos de electores. Por favor, verifique el número ingresado o contacte con el administrador.'
        );
        mostrarToast('error', 'DNI no encontrado');
        inputDNI.classList.add('error');

    } else if (has_voted) {
        // DNI ya votó
        const fechaVoto = resultado.voto ? new Date(resultado.voto.fecha).toLocaleString('es-PE') : 'No disponible';

        mostrarMensaje(
            'warning',
            'Ya ha votado',
            `El DNI ${dni} ya ha registrado su voto el ${fechaVoto}. No puede votar más de una vez.`,
            elector
        );
        mostrarToast('warning', 'Este DNI ya ha votado');
        inputDNI.classList.add('error');

    } else {
        // DNI válido y puede votar
        mostrarMensaje(
            'success',
            '✓ Verificación exitosa',
            'DNI verificado correctamente. Será redirigido a la cédula de votación en unos momentos...',
            elector
        );
        mostrarToast('success', 'DNI verificado correctamente');
        inputDNI.classList.add('success');

        // Guardar DNI en sessionStorage
        sessionStorage.setItem('dniVerificado', dni);
        sessionStorage.setItem('electorData', JSON.stringify(elector));

        // Redirigir a la página de votación
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
    }
}

/**
 * Muestra un mensaje de estado
 */
function mostrarMensaje(tipo, titulo, mensaje, elector = null) {
    mensajeEstado.className = `mensaje-estado ${tipo} show`;

    let html = `
        <strong>${titulo}</strong>
        <p>${mensaje}</p>
    `;

    if (elector) {
        html += `
            <div class="elector-info">
                <p><strong>Nombre:</strong> ${elector.nombres} ${elector.apellidos}</p>
                <p><strong>Distrito:</strong> ${elector.distrito}</p>
                <p><strong>Región:</strong> ${elector.region}</p>
            </div>
        `;
    }

    mensajeEstado.innerHTML = html;
}

/**
 * Oculta el mensaje de estado
 */
function ocultarMensaje() {
    mensajeEstado.classList.remove('show');
}

/**
 * Muestra u oculta el loading spinner
 */
function mostrarLoading(mostrar) {
    if (mostrar) {
        loadingSpinner.classList.add('show');
    } else {
        loadingSpinner.classList.remove('show');
    }
}

/**
 * Muestra un toast de notificación
 */
function mostrarToast(tipo, mensaje) {
    toast.textContent = mensaje;
    toast.className = `toast ${tipo} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
