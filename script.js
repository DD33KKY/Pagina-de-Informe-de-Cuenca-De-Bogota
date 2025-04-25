// Función para inicializar la página
document.addEventListener('DOMContentLoaded', function() {
    // Establecer la fecha actual
    actualizarFecha();
    
    // Establecer el año actual en el footer
    document.getElementById('current-year').textContent = new Date().getFullYear();
    
    // Inicializar efectos de navegación
    inicializarNavegacion();
    
    // Agregar eventos de despliegue para las tarjetas
    agregarEventosTarjetas();
    
    // Inicializar tooltips (requiere Bootstrap)
    inicializarTooltips();
    
    // Función para inicializar los eventos de las imágenes
    initImageEvents();
});

// Establecer la fecha actual en formato local
function actualizarFecha() {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const fecha = new Date().toLocaleDateString('es-ES', options);
    
    // Capitalizar primera letra
    const fechaCapitalizada = fecha.charAt(0).toUpperCase() + fecha.slice(1);
    
    document.getElementById('current-date').textContent = fechaCapitalizada;
}

// Inicializar efectos de navegación
function inicializarNavegacion() {
    // Obtener todos los enlaces de navegación
    const navLinks = document.querySelectorAll('.navbar .nav-link');
    
    // Agregar evento de clic a cada enlace
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Si el enlace apunta a un ID dentro de la página
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                
                // Obtener el ID del destino
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                // Si el elemento existe, desplazar hasta él
                if (targetElement) {
                    // Desactivar clase activa en todos los enlaces
                    navLinks.forEach(navLink => navLink.classList.remove('active'));
                    
                    // Activar clase activa en el enlace actual
                    this.classList.add('active');
                    
                    // Desplazar hasta el elemento con animación suave
                    window.scrollTo({
                        top: targetElement.offsetTop - 70, // Ajuste para compensar la barra de navegación
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Activar enlace correspondiente al desplazar la página
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        // Encontrar la sección actual
        document.querySelectorAll('main section').forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                // Desactivar todos los enlaces activos
                navLinks.forEach(link => link.classList.remove('active'));
                
                // Activar el enlace correspondiente a la sección actual
                const targetLink = document.querySelector(`.navbar .nav-link[href="#${section.id}"]`);
                if (targetLink) {
                    targetLink.classList.add('active');
                }
            }
        });
    });
}

// Agregar eventos para las tarjetas de gráficos
function agregarEventosTarjetas() {
    // Obtener todas las tarjetas de gráficos
    const tarjetasGraficos = document.querySelectorAll('.card img.img-fluid');
    
    // Variables para controlar el estado del modal y temporizador
    let modalActivo = null;
    let tiempoEspera = null;
    
    tarjetasGraficos.forEach(img => {
        // Al hacer clic en la imagen, mostrarla en tamaño completo
        img.addEventListener('click', function() {
            const modal = crearModal(this.src, this.alt);
            document.body.appendChild(modal);
            modalActivo = modal;
            
            // Mostrar el modal con efecto de fade in
            setTimeout(() => {
                modal.style.opacity = '1';
            }, 10);
            
            // Cerrar el modal al hacer clic fuera de la imagen
            modal.addEventListener('click', function(e) {
                if (e.target === modal || e.target.classList.contains('modal-close')) {
                    cerrarModal(modal);
                }
            });
        });
        
        // Al pasar el cursor por encima de la imagen
        img.addEventListener('mouseenter', function() {
            // Crear un retraso corto para evitar que se abra inmediatamente
            tiempoEspera = setTimeout(() => {
                if (!modalActivo) {
                    const modal = crearModal(this.src, this.alt);
                    document.body.appendChild(modal);
                    modalActivo = modal;
                    
                    // Mostrar el modal con efecto de fade in
                    setTimeout(() => {
                        modal.style.opacity = '1';
                    }, 10);
                    
                    // Cerrar el modal al hacer clic fuera de la imagen o presionar ESC
                    modal.addEventListener('click', function(e) {
                        if (e.target === modal || e.target.classList.contains('modal-close')) {
                            cerrarModal(modal);
                        }
                    });
                    
                    // Agregar evento al modal para que no se cierre si el cursor está sobre él
                    modal.addEventListener('mouseenter', function() {
                        clearTimeout(tiempoEspera);
                    });
                    
                    // Cerrar el modal al salir del modal si el cursor no está sobre la imagen original
                    modal.addEventListener('mouseleave', function(e) {
                        if (!img.matches(':hover')) {
                            cerrarModal(modal);
                        }
                    });
                }
            }, 300); // Retraso de 300ms antes de mostrar el modal
        });
        
        // Al quitar el cursor de la imagen
        img.addEventListener('mouseleave', function() {
            clearTimeout(tiempoEspera);
            
            // Dar tiempo para que el usuario mueva el cursor al modal si lo desea
            tiempoEspera = setTimeout(() => {
                if (modalActivo && !modalActivo.matches(':hover')) {
                    cerrarModal(modalActivo);
                }
            }, 300);
        });
    });
    
    // Función para cerrar el modal
    function cerrarModal(modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            if (modal.parentNode) {
                document.body.removeChild(modal);
            }
            if (modalActivo === modal) {
                modalActivo = null;
            }
        }, 300);
    }
    
    // Agregar evento para cerrar con tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalActivo) {
            cerrarModal(modalActivo);
        }
    });
}

// Crear un modal para mostrar imágenes en tamaño completo
function crearModal(imagenSrc, imagenAlt) {
    const modal = document.createElement('div');
    modal.className = 'modal-imagen';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '9999';
    modal.style.opacity = '0';
    modal.style.transition = 'opacity 0.3s ease';
    
    // Crear el botón de cierre
    const closeButton = document.createElement('span');
    closeButton.className = 'modal-close';
    closeButton.innerHTML = '&times;';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '20px';
    closeButton.style.right = '30px';
    closeButton.style.color = 'white';
    closeButton.style.fontSize = '40px';
    closeButton.style.fontWeight = 'bold';
    closeButton.style.cursor = 'pointer';
    
    // Crear la imagen
    const imagen = document.createElement('img');
    imagen.src = imagenSrc;
    imagen.alt = imagenAlt;
    imagen.style.maxWidth = '90%';
    imagen.style.maxHeight = '90%';
    imagen.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)';
    
    // Añadir elementos al modal
    modal.appendChild(closeButton);
    modal.appendChild(imagen);
    
    return modal;
}

// Inicializar tooltips (requiere Bootstrap)
function inicializarTooltips() {
    // Verificar si la función de Bootstrap está disponible
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
}

// Función para marcar secciones como activas al desplazarse
function marcarSeccionesActivas() {
    const sections = document.querySelectorAll('main section');
    
    window.addEventListener('scroll', function() {
        let currentSection = '';
        const scrollPosition = window.scrollY;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = section.id;
                
                // Aplicar efecto visual a la sección actual
                section.classList.add('seccion-activa');
            } else {
                section.classList.remove('seccion-activa');
            }
        });
    });
}

// Llamar a la función para marcar secciones activas
document.addEventListener('DOMContentLoaded', marcarSeccionesActivas);

// Definición de puntos y geometrías
// Punto del nacimiento del río Bogotá en el Páramo de Guacheneque
var puntoNacimiento = /* color: #98ff00 */ee.Geometry.Point([-73.52789, 5.23477]);

// Geometría detallada del río Bogotá basada en coordenadas precisas
var rioBogota = /* color: #0b4a8b */ee.Geometry.LineString([
  [-73.52789, 5.23477], // Nacimiento en Páramo de Guacheneque
  [-73.53000, 5.23000],
  [-73.54000, 5.22000],
  [-73.55000, 5.21000],
  [-73.56000, 5.20000],
  [-73.60000, 5.18000],
  [-73.65000, 5.16000],
  [-73.68300, 5.14500],
  [-73.70000, 5.14000],
  [-73.75000, 5.12000],
  [-73.78000, 5.11000],
  [-73.80000, 5.08300],
  [-73.85000, 5.03000],
  [-73.87800, 4.98300],
  [-73.90000, 4.96000],
  [-73.91700, 4.93300],
  [-73.93000, 4.93000],
  [-73.95000, 4.90000],
  [-73.99600, 5.02200],
  [-74.01000, 5.00000],
  [-74.02000, 4.96000],
  [-74.02800, 4.91800],
  [-74.04000, 4.88000],
  [-74.05800, 4.86100],
  [-74.07000, 4.84000],
  [-74.10000, 4.80900],
  [-74.12000, 4.78000],
  [-74.10000, 4.75000],
  [-74.10000, 4.72500], // Villa Pinzón
  [-74.10000, 4.70000],
  [-74.11000, 4.68000],
  [-74.13000, 4.68000],
  [-74.14000, 4.65000],
  [-74.15000, 4.63000],
  [-74.16000, 4.61000],
  [-74.18000, 4.59000],
  [-74.21600, 4.57900],
  [-74.23500, 4.53000],
  [-74.24700, 4.48500],
  [-74.27000, 4.45000],
  [-74.35000, 4.43300],
  [-74.37500, 4.48000],
  [-74.39500, 4.50000],
  [-74.47000, 4.63000],
  [-74.50000, 4.58000],
  [-74.53000, 4.55000],
  [-74.62000, 4.52000],
  [-74.64000, 4.47000],
  [-74.67000, 4.38000],
  [-74.80000, 4.29000] // Desembocadura
]);

// Buffer alrededor del río para crear un área de análisis (ya no se usará)
var bufferRio = rioBogota.buffer(5000); // 5km de buffer a cada lado del río

// Definición de un cuadro rectangular como área de análisis
// Coordenadas: [min lon, min lat, max lon, max lat]
// Definimos un cuadro que cubre gran parte de la cuenca del río Bogotá
var roi = ee.Geometry.Rectangle([-74.70, 4.30, -73.50, 5.25]);

// Importar colecciones de imágenes
var chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY");
var chirts = ee.ImageCollection("UCSB-CHG/CHIRTS/DAILY");
var fldas = ee.ImageCollection("NASA/FLDAS/NOAH01/C/GL/M/V001");

// Centrar el mapa en el río Bogotá con un zoom adecuado
Map.centerObject(rioBogota, 8);

// Función para recortar imágenes según el área de interés
function recortarImagenes(imgs){
  return imgs.clip(roi);
}

// Filtrado de datos diarios y aplicación de la función de recorte
var lluviasDiarias = chirps.select('precipitation').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);

var tempMaxDia = chirts.select('maximum_temperature').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);
  
var tempMinDia = chirts.select('minimum_temperature').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);
  
var humRelDia = chirts.select('relative_humidity').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);

var humSuelo = fldas.select('SoilMoi00_10cm_tavg').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);

var tempSuelo = fldas.select('SoilTemp00_10cm_tavg').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);

// Añadimos datos de evaporación desde FLDAS
var evaporacion = fldas.select('Evap_tavg').filterDate('2000-01-01','2024-06-30')
  .filterBounds(roi).map(recortarImagenes);

// Visualizar el río y el área de análisis
Map.addLayer(rioBogota, {color: 'blue'}, 'Río Bogotá');
Map.addLayer(roi, {color: 'red', opacity: 0.3}, 'Área de análisis (cuadro)');

// Función para inicializar los eventos de las imágenes
function initImageEvents() {
    // Seleccionar todas las imágenes en cards que deberían tener la funcionalidad de modal
    const imageCards = document.querySelectorAll('.card-img-top, .card-img');
    
    imageCards.forEach(img => {
        // Crear un modal único para cada imagen
        const modal = document.createElement('div');
        modal.className = 'modal-imagen';
        modal.style.opacity = '0';
        modal.style.pointerEvents = 'none';
        
        // Crear la imagen dentro del modal
        const modalImg = document.createElement('img');
        modalImg.src = img.src;
        modalImg.alt = img.alt || 'Imagen ampliada';
        
        // Crear el botón de cierre
        const closeBtn = document.createElement('span');
        closeBtn.className = 'modal-close';
        closeBtn.innerHTML = '&times;';
        
        // Agregar elementos al modal
        modal.appendChild(modalImg);
        modal.appendChild(closeBtn);
        
        // Agregar el modal al body
        document.body.appendChild(modal);
        
        // Mostrar modal al pasar el cursor sobre la imagen
        img.addEventListener('mouseenter', () => {
            modal.style.opacity = '1';
            modal.style.pointerEvents = 'auto';
        });
        
        // Ocultar modal al quitar el cursor de la imagen
        img.addEventListener('mouseleave', () => {
            modal.style.opacity = '0';
            modal.style.pointerEvents = 'none';
        });
        
        // Ocultar modal al hacer clic en el botón de cierre
        closeBtn.addEventListener('click', () => {
            modal.style.opacity = '0';
            modal.style.pointerEvents = 'none';
        });
        
        // Ocultar modal al hacer clic fuera de la imagen
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.opacity = '0';
                modal.style.pointerEvents = 'none';
            }
        });
    });
} 