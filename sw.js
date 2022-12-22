const cacheName = 'v1';

const cacheAssets = [
    '/static/assets/Logo.png',
    '/static/assets/sfondo.jpg',
    '/static/assets/icons/icon192.png',
    '/static/mdb/js/mdb.min.js',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/login.js',    
    '/static/css/bootstrap.min.css',
    '/static/mdb/css/mdb.min.css',
    'main.js',
    'manifest.json'
];

self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open(cacheName).then(function (cache) {
            return cache.addAll(cacheAssets);
        })
    );
});

/* Serve cached content when offline */
self.addEventListener('fetch', function (e) {
    e.respondWith(
        caches.match(e.request).then(function (response) {
            return response || fetch(e.request);
        })
    );
});
