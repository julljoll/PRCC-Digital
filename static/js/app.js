// PRCC Digital - Windows 95 Edition
// Aplicación de Registro de Cadena de Custodia

// Estado de la aplicación
const appState = {
    expediente: '',
    prcc: '',
    despacho_instruye: '',
    organismo_investiga: '',
    despacho_custodia: '',
    organismo_custodia: '',
    direccion_obtencion: '',
    fecha_hora: '',
    formas_obtencion: {
        tecnica: false,
        aseguramiento: false,
        consignacion: false,
        derivacion: false
    }
};

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', function() {
    updateDateTime();
    setInterval(updateDateTime, 1000);
    loadSavedData();
});

// Actualizar fecha y hora
function updateDateTime() {
    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    };
    document.getElementById('fecha_hora').value = now.toLocaleString('es-ES', options);
    appState.fecha_hora = document.getElementById('fecha_hora').value;
}

// Guardar datos en localStorage
function saveData() {
    // Recoger datos del formulario
    appState.expediente = document.getElementById('expediente').value;
    appState.prcc = document.getElementById('prcc').value;
    appState.despacho_instruye = document.getElementById('despacho_instruye').value;
    appState.organismo_investiga = document.getElementById('organismo_investiga').value;
    appState.despacho_custodia = document.getElementById('despacho_custodia').value;
    appState.organismo_custodia = document.getElementById('organismo_custodia').value;
    appState.direccion_obtencion = document.getElementById('direccion_obtencion').value;
    
    // Formas de obtención
    appState.formas_obtencion.tecnica = document.getElementById('obtencion_tecnica').checked;
    appState.formas_obtencion.aseguramiento = document.getElementById('obtencion_aseguramiento').checked;
    appState.formas_obtencion.consignacion = document.getElementById('obtencion_consignacion').checked;
    appState.formas_obtencion.derivacion = document.getElementById('obtencion_derivacion').checked;
    
    // Guardar en localStorage
    localStorage.setItem('prcc_data', JSON.stringify(appState));
    
    // Mostrar notificación
    showNotification('Datos guardados exitosamente');
    
    console.log('Datos guardados:', appState);
}

// Cargar datos guardados
function loadSavedData() {
    const savedData = localStorage.getItem('prcc_data');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            
            document.getElementById('expediente').value = data.expediente || '';
            document.getElementById('prcc').value = data.prcc || '';
            document.getElementById('despacho_instruye').value = data.despacho_instruye || '';
            document.getElementById('organismo_investiga').value = data.organismo_investiga || '';
            document.getElementById('despacho_custodia').value = data.despacho_custodia || '';
            document.getElementById('organismo_custodia').value = data.organismo_custodia || '';
            document.getElementById('direccion_obtencion').value = data.direccion_obtencion || '';
            
            document.getElementById('obtencion_tecnica').checked = data.formas_obtencion?.tecnica || false;
            document.getElementById('obtencion_aseguramiento').checked = data.formas_obtencion?.aseguramiento || false;
            document.getElementById('obtencion_consignacion').checked = data.formas_obtencion?.consignacion || false;
            document.getElementById('obtencion_derivacion').checked = data.formas_obtencion?.derivacion || false;
            
            console.log('Datos cargados desde localStorage');
        } catch (e) {
            console.error('Error al cargar datos:', e);
        }
    }
}

// Exportar a JSON
function exportJSON() {
    saveData(); // Asegurar que los datos estén actualizados
    
    const jsonString = JSON.stringify(appState, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `PRCC_${appState.expediente || 'sin_expediente'}_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Archivo JSON exportado');
}

// Mostrar notificación
function showNotification(message) {
    const notification = document.getElementById('notification');
    const messageEl = document.getElementById('notification-message');
    
    messageEl.textContent = message;
    notification.classList.remove('hidden');
}

// Cerrar notificación
function closeNotification() {
    document.getElementById('notification').classList.add('hidden');
}

// Utilidad para formatear fechas
function formatDate(date) {
    return date.toISOString().slice(0, 19).replace('T', ' ');
}

// Utilidad para validar campos
function validateField(fieldId, fieldName) {
    const field = document.getElementById(fieldId);
    if (!field.value.trim()) {
        showNotification(`El campo "${fieldName}" es requerido`);
        field.focus();
        return false;
    }
    return true;
}

// Exportar funciones para uso global
window.saveData = saveData;
window.exportJSON = exportJSON;
window.closeNotification = closeNotification;
window.validateField = validateField;
