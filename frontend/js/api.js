/**
 * Módulo de comunicación con el backend Flask
 * Actualizado con validaciones de DNI y voto en blanco
 */

const API_BASE_URL = 'http://localhost:5000/api';

const API = {
    /**
     * Realiza una petición fetch con reintentos
     */
    async fetchWithRetry(url, options = {}, retries = 3) {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch(url, {
                    ...options,
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    }
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || `HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                if (i === retries - 1) throw error;
                // Esperar antes de reintentar (backoff exponencial)
                await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
            }
        }
    },

    /**
     * Obtiene todos los candidatos de una categoría específica
     */
    async getCandidatosPorCategoria(nombreCategoria) {
        try {
            // Primero obtener la categoría
            const categorias = await this.fetchWithRetry(`${API_BASE_URL}/categorias/`);
            const categoria = categorias.find(c =>
                c.nombre_categoria.toLowerCase().includes(nombreCategoria.toLowerCase())
            );

            if (!categoria) {
                throw new Error(`Categoría ${nombreCategoria} no encontrada`);
            }

            // Obtener todos los candidatos
            const candidatos = await this.fetchWithRetry(`${API_BASE_URL}/candidatos/`);

            // Filtrar por categoría
            const candidatosFiltrados = candidatos.filter(c =>
                c.id_categoria === categoria.id_categoria
            );

            // Obtener información de partidos para cada candidato
            const partidos = await this.fetchWithRetry(`${API_BASE_URL}/partidos/`);

            // Agrupar candidatos por partido
            const candidatosPorPartido = {};

            for (const candidato of candidatosFiltrados) {
                const partido = partidos.find(p => p.id_partido === candidato.id_partido);

                if (!candidatosPorPartido[candidato.id_partido]) {
                    candidatosPorPartido[candidato.id_partido] = {
                        partido: partido,
                        candidatos: []
                    };
                }

                candidatosPorPartido[candidato.id_partido].candidatos.push(candidato);
            }

            return {
                categoria: categoria,
                partidosConCandidatos: Object.values(candidatosPorPartido)
            };

        } catch (error) {
            console.error(`Error al obtener candidatos de ${nombreCategoria}:`, error);
            throw error;
        }
    },

    /**
     * Obtiene todos los partidos políticos
     */
    async getPartidos() {
        return await this.fetchWithRetry(`${API_BASE_URL}/partidos/`);
    },

    /**
     * Obtiene todas las categorías
     */
    async getCategorias() {
        return await this.fetchWithRetry(`${API_BASE_URL}/categorias/`);
    },

    /**
     * Obtiene todos los tipos de voto
     */
    async getTiposVoto() {
        return await this.fetchWithRetry(`${API_BASE_URL}/tipos-voto/`);
    },

    /**
     * Verifica si un DNI ya ha votado
     */
    async verificarDNI(dni) {
        try {
            return await this.fetchWithRetry(`${API_BASE_URL}/votos/verificar-dni/${dni}`, {}, 1);
        } catch (error) {
            console.error('Error al verificar DNI:', error);
            throw error;
        }
    },

    /**
     * Crea un nuevo elector
     */
    async crearElector(dni, nombres, apellidos, distrito, region) {
        return await this.fetchWithRetry(`${API_BASE_URL}/electores/`, {
            method: 'POST',
            body: JSON.stringify({
                dni,
                nombres,
                apellidos,
                distrito,
                region
            })
        });
    },

    /**
     * Registra un voto completo con determinación automática del tipo
     * El backend determina si es válido o en blanco según las categorías
     */
    async registrarVoto(dni, votosPorCategoria) {
        try {
            // Obtener todas las categorías para asegurar que se envían todas
            const categorias = await this.getCategorias();

            // Preparar los votos por categoría
            const votosCategoria = [];

            // Recorrer TODAS las categorías
            for (const categoria of categorias) {
                const voto = votosPorCategoria.find(v => v.id_categoria === categoria.id_categoria);

                // Si hay un voto válido con partido
                if (voto && voto.estado === 'valido' && voto.id_partido) {
                    votosCategoria.push({
                        id_categoria: categoria.id_categoria,
                        id_partido: voto.id_partido,
                        numero_preferencial_1: voto.candidatos_preferenciales?.[0] || null,
                        numero_preferencial_2: voto.candidatos_preferenciales?.[1] || null
                    });
                } else {
                    // Voto en blanco para esta categoría
                    votosCategoria.push({
                        id_categoria: categoria.id_categoria,
                        id_partido: null,  // NULL indica voto en blanco
                        numero_preferencial_1: null,
                        numero_preferencial_2: null
                    });
                }
            }

            // Registrar el voto (el backend determina automáticamente el tipo)
            const response = await fetch(`${API_BASE_URL}/votos/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    dni: dni,
                    votos_categoria: votosCategoria
                })
            });

            if (!response.ok) {
                const error = await response.json();

                // Manejar específicamente el error de DNI duplicado
                if (response.status === 409) {
                    throw {
                        type: 'DNI_YA_VOTO',
                        message: error.error || 'Este DNI ya ha registrado un voto',
                        details: error
                    };
                }

                throw new Error(error.error || 'Error al registrar el voto');
            }

            const voto = await response.json();
            return voto;

        } catch (error) {
            console.error('Error al registrar voto:', error);
            throw error;
        }
    },

    /**
     * Verifica la conexión con el servidor
     */
    async checkConnection() {
        try {
            await this.fetchWithRetry(`${API_BASE_URL}/categorias/`, {}, 1);
            return true;
        } catch (error) {
            return false;
        }
    }
};

// Exportar para uso en otros módulos
window.API = API;
