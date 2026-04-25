const CACHE_NAME = 'prcc-win95-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/styles.css',
  '/static/js/app.js',
  '/manifest.json'
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Cacheando assets principales');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Activación y limpieza de cachés antiguas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
});

// Interceptación de solicitudes (estrategia: Cache First, luego Network)
self.addEventListener('fetch', (event) => {
  // Ignorar solicitudes que no sean GET
  if (event.request.method !== 'GET') {
    return;
  }

  // Ignorar solicitudes de API para asegurar datos frescos
  if (event.request.url.includes('/api/')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Devolver desde caché si existe
        return cachedResponse;
      }

      // Si no está en caché, intentar obtener de la red
      return fetch(event.request).then((networkResponse) => {
        // Verificar que la respuesta sea válida
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }

        // Clonar la respuesta para guardar en caché
        const responseToCache = networkResponse.clone();

        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      }).catch(() => {
        // Fallback para cuando no hay conexión ni caché
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('/');
        }
      });
    })
  );
});

// Mensajería para actualizar caché manualmente si es necesario
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
