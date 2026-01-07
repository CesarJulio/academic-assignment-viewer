import json
import os

# Paths
json_path = 'data.json'
html_path = 'visor_asignacion.html'

def generate_html():
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data_json = f.read()
            # Parse to ensure valid JSON
            json.loads(data_json)

        # HTML Template as a raw string to avoid f-string escaping hell
        html_template = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visor de Asignación Académica</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Filters and PDF Libs -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.31/jspdf.plugin.autotable.min.js"></script>
    <!-- SheetJS for Excel -->
    <script src="https://cdn.sheetjs.com/xlsx-0.20.0/package/dist/xlsx.full.min.js"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                    colors: {
                        primary: '#2563eb',
                        secondary: '#4f46e5',
                    }
                }
            }
        }
    </script>

    <style>
        body {
            background-color: #f3f4f6;
            /* Subtle pattern or gradient */
            background-image: radial-gradient(#e5e7eb 1px, transparent 1px);
            background-size: 20px 20px;
        }
        .glass-panel {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .custom-select {
            appearance: none;
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 0.5rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
        }
        /* Custom scrollbar for webkit */
        .custom-scrollbar::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent; 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #cbd5e1; 
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #94a3b8; 
        }
    </style>
</head>
<body class="text-gray-800 h-screen flex flex-col overflow-hidden font-sans">

    <!-- Header -->
    <header class="bg-white border-b border-gray-200 shadow-sm z-20 flex-none backdrop-blur-md bg-white/90 sticky top-0">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="bg-primary/10 p-2 rounded-lg">
                    <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                </div>
                <div>
                    <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                        Visor de Asignación Académica
                    </h1>
                    <p class="text-xs text-gray-500 font-medium hidden sm:block">Consulta y descarga</p>
                </div>
            </div>
            <div class="bg-gray-100 px-3 py-1 rounded-full border border-gray-200">
                <span class="text-xs font-semibold text-gray-600" id="record-count">Cargando...</span>
            </div>
        </div>
    </header>

    <!-- Filters Section -->
    <div class="bg-white border-b border-gray-200 p-4 shadow-sm flex-none z-10 transition-all">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <!-- Facultad Filter -->
            <div class="relative group">
                <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 pl-1">Facultad</label>
                <div class="relative">
                    <select id="facultadSelect" class="custom-select w-full bg-gray-50 border border-gray-200 text-gray-700 py-2.5 px-4 pr-8 rounded-lg outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all shadow-sm hover:bg-gray-100 cursor-pointer font-medium text-sm">
                        <option value="TODOS">TODOS</option>
                    </select>
                </div>
            </div>

            <!-- Programa Filter -->
            <div class="relative group">
                <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 pl-1">Programa</label>
                <div class="relative">
                    <select id="programaSelect" class="custom-select w-full bg-gray-50 border border-gray-200 text-gray-700 py-2.5 px-4 pr-8 rounded-lg outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all shadow-sm hover:bg-gray-100 cursor-pointer font-medium text-sm">
                        <option value="TODOS">TODOS</option>
                    </select>
                </div>
            </div>

            <!-- Semestre Filter -->
            <div class="relative group">
                <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1 pl-1">Semestre</label>
                <div class="relative">
                    <select id="semestreSelect" class="custom-select w-full bg-gray-50 border border-gray-200 text-gray-700 py-2.5 px-4 pr-8 rounded-lg outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all shadow-sm hover:bg-gray-100 cursor-pointer font-medium text-sm">
                        <option value="TODOS">TODOS</option>
                    </select>
                </div>
            </div>

        </div>
    </div>

    <!-- Main Content (Table) -->
    <main class="flex-grow overflow-hidden relative bg-gray-50/50">
        <div class="absolute inset-0 overflow-auto px-4 py-6 sm:px-6 custom-scrollbar">
            <div class="max-w-7xl mx-auto">
                <div class="bg-white rounded-xl shadow-lg border border-gray-200/60 overflow-hidden ring-1 ring-black ring-opacity-5">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50/80 backdrop-blur">
                                <tr>
                                    <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-24">Semestre</th>
                                    <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Código - Asignatura</th>
                                    <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-20">Grupo</th>
                                    <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Docente</th>
                                </tr>
                            </thead>
                            <tbody id="tableBody" class="bg-white divide-y divide-gray-100">
                                <!-- Rows will be injected here -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Empty State -->
                <div id="emptyState" class="hidden flex flex-col items-center justify-center py-20 text-gray-500">
                    <div class="bg-gray-100 p-4 rounded-full mb-4">
                        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </div>
                    <p class="text-lg font-semibold text-gray-700">No se encontraron resultados</p>
                    <p class="text-sm mt-1">Intenta cambiar los filtros para ver más información</p>
                </div>

                <div class="h-24"></div> <!-- Spacer for FAB -->
            </div>
        </div>
    </main>

    <!-- Floating Action Buttons -->
    <div class="absolute bottom-6 right-6 sm:bottom-10 sm:right-10 z-30 flex flex-col sm:flex-row gap-3">
        <!-- Button Excel -->
        <button onclick="exportToXLSX()" class="group flex items-center justify-center gap-2 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-700 hover:to-green-600 text-white font-bold py-3.5 px-6 rounded-full shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-green-300 ring-offset-2">
            <svg class="w-5 h-5 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <span>Descargar Excel</span>
        </button>

        <!-- Button PDF -->
        <button onclick="exportToPDF()" class="group flex items-center justify-center gap-2 bg-gradient-to-r from-red-600 to-red-500 hover:from-red-700 hover:to-red-600 text-white font-bold py-3.5 px-6 rounded-full shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-red-300 ring-offset-2">
            <svg class="w-5 h-5 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
            </svg>
            <span>Descargar PDF</span>
        </button>
    </div>

    <!-- Logic -->
    <script>
        // RAW DATA INJECTION
        const rawData = {{DATA_PLACEHOLDER}};
        
        // State
        let filteredData = [];
        
        // Elements
        const tableBody = document.getElementById('tableBody');
        const emptyState = document.getElementById('emptyState');
        const countLabel = document.getElementById('record-count');
        
        const facultadSelect = document.getElementById('facultadSelect');
        const programaSelect = document.getElementById('programaSelect');
        const semestreSelect = document.getElementById('semestreSelect');

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            preprocessData();
            initFilters();
            applyFilters();
        });

        function preprocessData() {
            // Add helper fields if needed
            rawData.forEach(item => {
                // Create "Code - Name" fields
                item.facultadDisplay = `${item['Facultad Code']} - ${item['Facultad']}`;
                item.programaDisplay = `${item['Programa Code']} - ${item['Programa']}`;
                item.asignaturaDisplay = `${item['Asignatura Code']} - ${item['Asignatura']}`;
                
                // Format Docente full name with ID
                // "Documento - Apellidos Nombres"
                const docName = (item['Docente Apellidos'] || '') + ' ' + (item['Docente Nombres'] || '');
                item.docenteDisplay = item['Docente Documento'] ? `<div class="font-medium text-gray-900">${item['Docente Documento']}</div><div class="text-xs text-gray-500 uppercase">${docName}</div>` : '<span class="text-gray-400 italic text-xs">Sin asignar</span>';
                item.docenteFull = item['Docente Documento'] ? `${item['Docente Documento']} - ${docName}` : 'Sin asignar';
            });
        }

        function initFilters() {
            // Helper to populate select
            const populate = (select, values) => {
                // Keep 'TODOS'
                select.innerHTML = '<option value="TODOS">TODOS</option>';
                values.sort().forEach(val => {
                    if(!val) return;
                    const option = document.createElement('option');
                    option.value = val;
                    option.textContent = val;
                    select.appendChild(option);
                });
            };

            // Get unique values
            const facultades = [...new Set(rawData.map(d => d.facultadDisplay))];
            populate(facultadSelect, facultades);

            // Initial populate 
            const programas = [...new Set(rawData.map(d => d.programaDisplay))];
            populate(programaSelect, programas);

            // Semesters: Sort numerically if possible, otherwise string sort
            const semestres = [...new Set(rawData.map(d => d['Semestre Asignatura']))];
            // Custom sort for semesters (handle numbers vs text)
            semestres.sort((a, b) => {
                const numA = parseInt(a);
                const numB = parseInt(b);
                if (!isNaN(numA) && !isNaN(numB)) return numA - numB;
                return String(a).localeCompare(String(b));
            });
            populate(semestreSelect, semestres);

            // Listeners
            facultadSelect.addEventListener('change', handleFacultadChange);
            programaSelect.addEventListener('change', applyFilters);
            semestreSelect.addEventListener('change', applyFilters);
        }

        function handleFacultadChange() {
            const selectedFac = facultadSelect.value;
            
            // Filter programs based on selected faculty if not TODOS
            let relevantPrograms;
            if (selectedFac === 'TODOS') {
                relevantPrograms = [...new Set(rawData.map(d => d.programaDisplay))];
            } else {
                relevantPrograms = [...new Set(rawData
                    .filter(d => d.facultadDisplay === selectedFac)
                    .map(d => d.programaDisplay)
                )];
            }
            
            // Update Program Select
            // Save current selection if possible
            const currentProg = programaSelect.value;
            
            // Repopulate
            const populate = (select, values) => {
                select.innerHTML = '<option value="TODOS">TODOS</option>';
                values.sort().forEach(val => {
                    if(!val) return;
                    const option = document.createElement('option');
                    option.value = val;
                    option.textContent = val;
                    select.appendChild(option);
                });
            };
            populate(programaSelect, relevantPrograms);
            
            // Restore selection if valid, else TODOS
            if (relevantPrograms.includes(currentProg)) {
                programaSelect.value = currentProg;
            } else {
                programaSelect.value = 'TODOS';
            }

            applyFilters();
        }

        function applyFilters() {
            const fac = facultadSelect.value;
            const prog = programaSelect.value;
            const sem = semestreSelect.value;

            filteredData = rawData.filter(item => {
                const matchFac = fac === 'TODOS' || item.facultadDisplay === fac;
                const matchProg = prog === 'TODOS' || item.programaDisplay === prog;
                const matchSem = sem === 'TODOS' || item['Semestre Asignatura'] === sem;
                return matchFac && matchProg && matchSem;
            });

            // Sort: 1. Semestre (asc), 2. Asignatura (asc), 3. Grupo (asc)
            filteredData.sort((a, b) => {
                // Semestre
                const semA = parseInt(a['Semestre Asignatura']) || 999;
                const semB = parseInt(b['Semestre Asignatura']) || 999;
                if (semA !== semB) return semA - semB;
                
                // Asignatura
                if (a.asignaturaDisplay < b.asignaturaDisplay) return -1;
                if (a.asignaturaDisplay > b.asignaturaDisplay) return 1;

                // Grupo
                if (a['Grupo'] < b['Grupo']) return -1;
                if (a['Grupo'] > b['Grupo']) return 1;
                
                return 0;
            });

            renderTable();
            countLabel.textContent = `${filteredData.length} registros`;
        }

        function renderTable() {
            tableBody.innerHTML = '';
            
            if (filteredData.length === 0) {
                emptyState.classList.remove('hidden');
                return;
            }
            emptyState.classList.add('hidden');

            const fragment = document.createDocumentFragment();

            filteredData.forEach(item => {
                const row = document.createElement('tr');
                row.className = 'hover:bg-blue-50/50 transition-colors duration-150 group';
                
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-800 border-r border-transparent group-hover:border-blue-100">
                        ${item['Semestre Asignatura']}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                        ${item.asignaturaDisplay}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700">
                            ${item['Grupo']}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                        ${item.docenteDisplay}
                    </td>
                `;
                fragment.appendChild(row);
            });
            
            tableBody.appendChild(fragment);
        }

        function exportToPDF() {
            if (filteredData.length === 0) {
                alert("No hay datos para exportar.");
                return;
            }

            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            // Header info
            const fac = facultadSelect.value !== 'TODOS' ? facultadSelect.value : 'Todas las Facultades';
            const prog = programaSelect.value !== 'TODOS' ? programaSelect.value : 'Todos los Programas';
            const sem = semestreSelect.value !== 'TODOS' ? 'Semestre ' + semestreSelect.value : 'Todos los Semestres';
            
            doc.setFontSize(14);
            doc.setTextColor(30, 64, 175); // Blue
            doc.text("Reporte de Asignación Académica", 14, 15);
            
            doc.setFontSize(9);
            doc.setTextColor(100);
            doc.text(`Filtros: ${fac}`, 14, 22);
            doc.text(`Programa: ${prog} | Semestre: ${sem}`, 14, 27);
            doc.text(`Fecha de generación: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`, 14, 32);

            const tableColumn = ["Sem.", "Asignatura", "Gr.", "Docente"];
            const tableRows = [];

            filteredData.forEach(item => {
                const row = [
                    item['Semestre Asignatura'],
                    item.asignaturaDisplay,
                    item['Grupo'],
                    item.docenteFull
                ];
                tableRows.push(row);
            });

            doc.autoTable({
                head: [tableColumn],
                body: tableRows,
                startY: 36,
                styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },
                headStyles: { fillColor: [37, 99, 235], textColor: 255, fontStyle: 'bold' },
                columnStyles: {
                    0: { cellWidth: 15, halign: 'center' }, // Sem
                    1: { cellWidth: 'auto' }, // Asignatura
                    2: { cellWidth: 15, halign: 'center' }, // Grupo
                    3: { cellWidth: 60 } // Docente
                },
                theme: 'grid'
            });

            // Save
            const safeProg = prog.replace(/[^a-z0-9]/gi, '_').substring(0, 20);
            doc.save(`Asignacion_${safeProg}.pdf`);
        }

        function exportToXLSX() {
            if (filteredData.length === 0) {
                alert("No hay datos para exportar.");
                return;
            }
            
            // Prepare data for SheetJS
            const ws_data = filteredData.map(item => ({
                "Facultad": item['Facultad'],
                "Programa": item['Programa'],
                "Semestre": item['Semestre Asignatura'],
                "Código Asignatura": item['Asignatura Code'],
                "Asignatura": item['Asignatura'],
                "Grupo": item['Grupo'],
                "Docente ID": item['Docente Documento'],
                "Docente Nombre": (item['Docente Apellidos'] || '') + ' ' + (item['Docente Nombres'] || '')
            }));

            const ws = XLSX.utils.json_to_sheet(ws_data);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Asignacion");

            // Auto-width columns (simple)
            const wscols = [
                {wch: 30}, // Facultad
                {wch: 30}, // Programa
                {wch: 10}, // Semestre
                {wch: 15}, // Codigo
                {wch: 40}, // Asignatura
                {wch: 10}, // Grupo
                {wch: 15}, // Docente ID
                {wch: 30}  // Docente Nombre
            ];
            ws['!cols'] = wscols;

            const prog = programaSelect.value !== 'TODOS' ? programaSelect.value : 'General';
            const safeProg = prog.replace(/[^a-z0-9]/gi, '_').substring(0, 20);
            
            XLSX.writeFile(wb, `Asignacion_${safeProg}.xlsx`);
        }
    </script>
</body>
</html>"""

        # Replace placeholder and write
        final_html = html_template.replace("{{DATA_PLACEHOLDER}}", data_json)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"HTML generated successfully at {html_path}")
            
    except Exception as e:
        print(f"Error generating HTML: {e}")

if __name__ == '__main__':
    generate_html()
