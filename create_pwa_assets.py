"""
Generate PWA icons and assets for ViralStudio KA-363
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

STATIC_DIR = Path(r"C:\Users\User\projects\tiktok-viral-analyzer\static")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

def generate_icon(size: int, output_path: Path):
    img = Image.new("RGBA", (size, size), (11, 13, 19, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded square with gradient look
    pad = int(size * 0.08)
    draw.rounded_rectangle(
        [(pad, pad), (size - pad, size - pad)],
        radius=int(size * 0.22),
        fill=(220, 38, 38, 255),
        outline=(245, 158, 11, 255),
        width=int(size * 0.02)
    )
    
    # Draw inner badge circle
    center = size // 2
    inner_rad = int(size * 0.32)
    draw.ellipse(
        [(center - inner_rad, center - inner_rad), (center + inner_rad, center + inner_rad)],
        fill=(15, 17, 23, 255)
    )
    
    # Draw text "KA" or donut symbol
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.35))
    except Exception:
        font = ImageFont.load_default()
        
    text = "KA"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((center - tw // 2, center - th // 2 - int(size * 0.04)), text, fill=(255, 255, 255, 255), font=font)
    
    # Small donut ring
    d_pad = int(size * 0.05)
    draw.ellipse(
        [(size - pad - d_pad * 2, pad), (size - pad, pad + d_pad * 2)],
        fill=(245, 158, 11, 255),
        outline=(255, 255, 255, 255),
        width=int(size * 0.01)
    )

    img.save(output_path, "PNG")
    print(f"[+] Saved icon: {output_path} ({size}x{size})")


# Generate 192x192 and 512x512 icons
generate_icon(192, STATIC_DIR / "icon-192.png")
generate_icon(512, STATIC_DIR / "icon-512.png")

# Write manifest.json
manifest_content = """{
  "name": "ViralStudio KA-363 | Khairul Aming Intelligence & Doh-Nut",
  "short_name": "ViralStudio",
  "description": "Short-Form Video Viral Retention Engine & Doh-Nut Proven Campaign Studio",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#080a0f",
  "theme_color": "#dc2626",
  "icons": [
    {
      "src": "/static/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/static/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "categories": ["productivity", "business", "multimedia"]
}"""

with open(STATIC_DIR / "manifest.json", "w", encoding="utf-8") as f:
    f.write(manifest_content)
print("[+] Saved manifest.json")

# Write Service Worker
sw_content = """const CACHE_NAME = 'viralstudio-v2.5';
const ASSETS_TO_CACHE = [
  '/',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png',
  'https://cdn.tailwindcss.com',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Caching app shell');
      return cache.addAll(ASSETS_TO_CACHE).catch(err => console.log('Cache add error:', err));
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).catch(() => {
        // Fallback or offline support
      });
    })
  );
});
"""

with open(STATIC_DIR / "sw.js", "w", encoding="utf-8") as f:
    f.write(sw_content)
print("[+] Saved sw.js")
