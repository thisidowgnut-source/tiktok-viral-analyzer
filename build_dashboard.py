"""
Compiler script to generate a standalone interactive HTML Dashboard for all 363 Khairul Aming TikTok Videos.
Includes interactive Chart.js Scatter Plot, KPI Cards, Category Breakdown, and a searchable filterable data table.
"""

import json
from pathlib import Path

INPUT_JSON = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_all_363_analysis.json"
OUTPUT_HTML = r"C:\Users\User\projects\tiktok-viral-analyzer\dashboard.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ms">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Khairul Aming TikTok 363-Video Virality Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0f1117; color: #e2e8f0; }
    .glass-card { background: rgba(26, 29, 39, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 1rem; }
    .custom-scroll::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scroll::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
  </style>
</head>
<body class="p-6 max-w-7xl mx-auto space-y-6">

  <!-- Header -->
  <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
    <div>
      <div class="flex items-center gap-3">
        <span class="px-3 py-1 bg-red-500/20 text-red-400 border border-red-500/30 rounded-full text-xs font-bold uppercase tracking-wider">TikTok Intelligence</span>
        <span class="px-3 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-bold uppercase tracking-wider">TypeSafe AI Jev</span>
      </div>
      <h1 class="text-3xl font-extrabold text-white mt-2">@khairulaming: Analisis Virality 363 Video</h1>
      <p class="text-slate-400 text-sm mt-1">Bedah siasat penuh 100% arkib kandungan TikTok, metrik retensi, dan formula penceritaan.</p>
    </div>
    <div class="text-right">
      <span class="text-xs text-slate-500 block">Katalog Terakhir Dikemas Kini</span>
      <span class="text-sm font-semibold text-slate-300">24 September 2026</span>
    </div>
  </div>

  <!-- KPI Metrics Grid -->
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <div class="glass-card p-5">
      <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Jumlah Tontonan</div>
      <div class="text-3xl font-extrabold text-amber-400 mt-2">213.4M</div>
      <div class="text-xs text-slate-500 mt-1">213,389,111 Paparan Organik</div>
    </div>
    <div class="glass-card p-5">
      <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Jumlah Suka (Likes)</div>
      <div class="text-3xl font-extrabold text-rose-400 mt-2">18.69M</div>
      <div class="text-xs text-slate-500 mt-1">Purata 51.5K Suka per video</div>
    </div>
    <div class="glass-card p-5">
      <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Perkongsian (Shares)</div>
      <div class="text-3xl font-extrabold text-cyan-400 mt-2">1.35M</div>
      <div class="text-xs text-slate-500 mt-1">Kunci utama algoritma FYP</div>
    </div>
    <div class="glass-card p-5">
      <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Jumlah Video Dituai</div>
      <div class="text-3xl font-extrabold text-emerald-400 mt-2">363</div>
      <div class="text-xs text-slate-500 mt-1">100% daripada profil akaun</div>
    </div>
  </div>

  <!-- Chart Section: Scatter Plot -->
  <div class="glass-card p-6 space-y-4">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-2">
      <div>
        <h2 class="text-xl font-bold text-white">Carta Serakan (Scatter Plot): Tontonan vs Perkongsian Video</h2>
        <p class="text-xs text-slate-400">Paksi X: Indeks Video | Paksi Y: Jumlah Tontonan | Saiz Gelembung: Perkongsian (Shares)</p>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <span class="inline-block w-3 h-3 rounded-full bg-amber-400"></span> Resepi Ramadan
        <span class="inline-block w-3 h-3 rounded-full bg-cyan-400 ml-2"></span> Bisnes / BTS
        <span class="inline-block w-3 h-3 rounded-full bg-rose-400 ml-2"></span> Resepi Viral Harian
      </div>
    </div>
    <div class="h-80 w-full">
      <canvas id="scatterChart"></canvas>
    </div>
  </div>

  <!-- Filter & Search Controls -->
  <div class="glass-card p-4 flex flex-col md:flex-row items-center justify-between gap-4">
    <div class="relative w-full md:w-96">
      <input type="text" id="searchInput" placeholder="Cari tajuk masakan, kapsyen, atau topik..." 
             class="w-full bg-slate-900/80 border border-slate-700 text-sm rounded-lg px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-amber-400">
    </div>
    <div class="flex items-center gap-3 w-full md:w-auto">
      <select id="categoryFilter" class="bg-slate-900/80 border border-slate-700 text-sm rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-400">
        <option value="ALL">Semua Kategori (363)</option>
        <option value="RESEPI_RAMADAN">Resepi Ramadan (343)</option>
        <option value="BEHIND_THE_SCENES_BISNES">Behind The Scenes Bisnes (16)</option>
        <option value="RESEPI_VIRAL_HARIAN">Resepi Viral Harian (4)</option>
      </select>
      <select id="sortFilter" class="bg-slate-900/80 border border-slate-700 text-sm rounded-lg px-3 py-2 text-white focus:outline-none focus:border-amber-400">
        <option value="views_desc">Tontonan Tertinggi (Views ↓)</option>
        <option value="shares_desc">Perkongsian Tertinggi (Shares ↓)</option>
        <option value="likes_desc">Suka Tertinggi (Likes ↓)</option>
        <option value="order_asc">Susunan Asal</option>
      </select>
    </div>
  </div>

  <!-- Video Table Explorer -->
  <div class="glass-card overflow-hidden">
    <div class="overflow-x-auto custom-scroll max-h-[550px]">
      <table class="w-full text-left text-sm text-slate-300">
        <thead class="bg-slate-900/90 text-xs uppercase tracking-wider text-slate-400 sticky top-0 border-b border-slate-800">
          <tr>
            <th class="py-3 px-4">#</th>
            <th class="py-3 px-4">Kategori & Hook</th>
            <th class="py-3 px-4">Kapsyen / Tajuk Video</th>
            <th class="py-3 px-4 text-right">Views</th>
            <th class="py-3 px-4 text-right">Likes</th>
            <th class="py-3 px-4 text-right">Shares</th>
            <th class="py-3 px-4 text-center">Pautan</th>
          </tr>
        </thead>
        <tbody id="videoTableBody" class="divide-y divide-slate-800/60 font-normal">
          <!-- Populated by JavaScript -->
        </tbody>
      </table>
    </div>
    <div class="p-3 bg-slate-900/60 border-t border-slate-800 text-xs text-slate-400 flex justify-between items-center">
      <span id="resultCount">Memaparkan 363 video</span>
      <span>Dikuasakan oleh TypeSafe AI Jev System One</span>
    </div>
  </div>

  <script>
    const rawData = DATA_PLACEHOLDER;

    // Render Scatter Chart
    const ctx = document.getElementById('scatterChart').getContext('2d');
    const chartData = rawData.map((d, i) => {
      let color = '#fbbf24'; // amber
      if (d.topic_category === 'BEHIND_THE_SCENES_BISNES') color = '#22d3ee'; // cyan
      if (d.topic_category === 'RESEPI_VIRAL_HARIAN') color = '#f43f5e'; // rose
      return {
        x: d.order,
        y: d.views,
        r: Math.max(4, Math.min(22, (d.shares / 15000))),
        backgroundColor: color,
        videoTitle: d.title,
        views: d.views,
        shares: d.shares
      };
    });

    const scatterChart = new Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: [{
          label: 'Semua Video',
          data: chartData,
          borderColor: 'transparent'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(context) {
                const p = context.raw;
                return [
                  p.videoTitle.substring(0, 50) + '...',
                  'Views: ' + p.views.toLocaleString(),
                  'Shares: ' + p.shares.toLocaleString()
                ];
              }
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Nombor Indeks Video', color: '#94a3b8' }
          },
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            title: { display: true, text: 'Jumlah Tontonan (Views)', color: '#94a3b8' },
            ticks: {
              callback: function(value) { return (value / 1e6).toFixed(0) + 'M'; }
            }
          }
        }
      }
    });

    // Table rendering & filtering
    const tableBody = document.getElementById('videoTableBody');
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const sortFilter = document.getElementById('sortFilter');
    const resultCount = document.getElementById('resultCount');

    function renderTable() {
      const q = searchInput.value.toLowerCase().trim();
      const cat = categoryFilter.value;
      const sort = sortFilter.value;

      let filtered = rawData.filter(item => {
        const matchQ = (item.title || '').toLowerCase().includes(q);
        const matchCat = (cat === 'ALL') || (item.topic_category === cat);
        return matchQ && matchCat;
      });

      // Sort
      if (sort === 'views_desc') filtered.sort((a, b) => b.views - a.views);
      else if (sort === 'shares_desc') filtered.sort((a, b) => b.shares - a.shares);
      else if (sort === 'likes_desc') filtered.sort((a, b) => b.likes - a.likes);
      else filtered.sort((a, b) => a.order - b.order);

      resultCount.innerText = `Memaparkan ${filtered.length} daripada ${rawData.length} video`;

      tableBody.innerHTML = filtered.map(v => {
        let badgeClass = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
        if (v.topic_category === 'BEHIND_THE_SCENES_BISNES') badgeClass = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30';
        if (v.topic_category === 'RESEPI_VIRAL_HARIAN') badgeClass = 'bg-rose-500/20 text-rose-300 border-rose-500/30';

        return `
          <tr class="hover:bg-slate-800/40 transition">
            <td class="py-3 px-4 font-mono text-slate-500 text-xs">${v.order}</td>
            <td class="py-3 px-4">
              <span class="inline-block px-2 py-0.5 rounded text-[10px] font-semibold border ${badgeClass}">
                ${v.topic_category.replace(/_/g, ' ')}
              </span>
              <span class="block text-[11px] text-slate-400 mt-1">${v.hook_type}</span>
            </td>
            <td class="py-3 px-4 font-medium text-white max-w-md truncate" title="${v.title}">
              ${v.title || '<span class="text-slate-500 italic">Tiada Kapsyen</span>'}
            </td>
            <td class="py-3 px-4 text-right font-mono font-semibold text-amber-400">${(v.views || 0).toLocaleString()}</td>
            <td class="py-3 px-4 text-right font-mono text-slate-300">${(v.likes || 0).toLocaleString()}</td>
            <td class="py-3 px-4 text-right font-mono text-cyan-300 font-semibold">${(v.shares || 0).toLocaleString()}</td>
            <td class="py-3 px-4 text-center">
              <a href="${v.url}" target="_blank" class="px-2.5 py-1 bg-slate-800 hover:bg-amber-400 hover:text-slate-900 border border-slate-700 rounded text-xs transition inline-block">
                Tengok ↗
              </a>
            </td>
          </tr>
        `;
      }).join('');
    }

    searchInput.addEventListener('input', renderTable);
    categoryFilter.addEventListener('change', renderTable);
    sortFilter.addEventListener('change', renderTable);

    renderTable();
  </script>
</body>
</html>
"""

def build_dashboard():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)
    html_content = HTML_TEMPLATE.replace("DATA_PLACEHOLDER", json_str)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] Berjaya menghasilkan Dashboard Interaktif 363 Video!")
    print(f"[+] Lokasi Fail: {OUTPUT_HTML}")

if __name__ == "__main__":
    build_dashboard()
