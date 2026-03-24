<script setup lang="ts">
import { ref } from 'vue'
import { 
  FileText, 
  User, 
  ClipboardCheck, 
  ArrowRightLeft, 
  Search, 
  Printer, 
  Download,
  Fingerprint,
  CheckCircle2,
  Check
} from 'lucide-vue-next'

const formData = ref({
  expediente: '',
  prcc: '',
  despachoInstruye: '',
  organismoInvestiga: '',
  despachoCustodia: '',
  organismoCustodia: '',
  direccionObtencion: '',
  fechaHora: new Date().toLocaleString(),
})

const obtencion = ref<Record<string, boolean>>({
  '1': false,
  '2': false,
  '3': false,
  '4': false,
})

const motivos = ref<Record<string, boolean>>({
  'Traslado': false,
  'Peritaje': false,
  'Resguardo': false,
  'Disposición Judicial': false,
  'Disposición Final': false,
})

const toggleObtencion = (id: string) => {
  obtencion.value[id] = !obtencion.value[id]
}

const toggleMotivo = (id: string) => {
  motivos.value[id] = !motivos.value[id]
}

const printDoc = () => {
  window.print()
}
</script>

<template>
  <div class="min-h-screen bg-[#0a0f1c] pt-0 pb-8 px-4 sm:px-6 lg:px-8 print:p-0 print:bg-white flex flex-col items-center gap-8 text-slate-300">
    
    <!-- PAGE 1 -->
    <div class="w-full max-w-[600px] min-w-[320px] min-h-[33cm] pt-0 pb-[2cm] bg-[#161b2a] shadow-2xl rounded-b-xl sm:rounded-xl overflow-hidden border border-slate-800/60 border-t-0 sm:border-t print:shadow-none print:border-none print:max-w-none print:w-full print:text-black print:p-0 print:m-0 print:break-after-page flex flex-col">
      
      <!-- Header Section -->
      <div class="bg-[#080d1a] p-6 border-b-4 border-emerald-500/30 print:bg-white print:border-b-2 print:border-black flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-start">
          <img src="https://ik.imagekit.io/p5pirzkod/sha256.us/Logo.svg" alt="SHA256.US forensic laboratory" class="h-12 sm:h-14 object-contain print:h-12" />
        </div>
        <!-- Title -->
        <div class="text-right">
          <h2 class="text-emerald-400 font-bold text-sm sm:text-base uppercase tracking-widest leading-tight print:text-black">
            Planilla de Registro<br/>de Cadena de Custodia
          </h2>
          <p class="text-slate-400 text-[10px] sm:text-xs mt-1 tracking-widest print:text-black">(PRCC)</p>
        </div>
      </div>

      <!-- Section I: Datos Generales -->
      <section class="border-b border-slate-800/60 print:border-slate-300">
        <div class="bg-[#080d1a] px-6 py-3 print:bg-slate-100">
          <h3 class="text-slate-100 font-bold text-sm flex items-center gap-2 print:text-black">
            <FileText :size="16" class="text-emerald-400 print:text-black" />
            I. DATOS GENERALES
          </h3>
        </div>
        <div class="p-6 space-y-4 bg-[#161b2a] print:bg-white print:grid print:grid-cols-2 print:gap-4 print:space-y-0">
          <!-- Stacked for email layout -->
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">a. N° de Expediente</label>
            <input type="text" v-model="formData.expediente" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">b. N° PRCC</label>
            <input type="text" v-model="formData.prcc" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">c. Despacho que instruye</label>
            <input type="text" v-model="formData.despachoInstruye" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">d. Organismo que investiga e instructivo</label>
            <input type="text" v-model="formData.organismoInvestiga" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">e. Despacho que inicia la custodia</label>
            <input type="text" v-model="formData.despachoCustodia" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">f. Organismo que custodia</label>
            <input type="text" v-model="formData.organismoCustodia" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">g. Dirección de Obtención</label>
            <input type="text" v-model="formData.direccionObtencion" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-400 uppercase tracking-tight print:text-slate-700">h. Fecha y Hora</label>
            <input type="text" v-model="formData.fechaHora" class="w-full bg-[#0a0f1c] border border-slate-700/80 rounded px-3 py-2 text-sm text-slate-200 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:bg-white print:text-black print:border-slate-300 print:py-1" />
          </div>
        </div>
      </section>

      <!-- Section II: Formas de Obtención -->
      <section class="border-b border-slate-800/60 print:border-slate-300">
        <div class="bg-[#080d1a] px-6 py-3 print:bg-slate-100">
          <h3 class="text-slate-100 font-bold text-sm flex items-center gap-2 print:text-black">
            <Search :size="16" class="text-emerald-400 print:text-black" />
            II. FORMAS DE OBTENCIÓN
          </h3>
        </div>
        <div class="grid grid-cols-2 print:grid-cols-4 divide-x divide-y divide-slate-800/60 border-b border-slate-800/60 print:divide-slate-200 print:border-slate-200">
          <div v-for="(label, num) in {'1': 'Técnica', '2': 'Aseguramiento', '3': 'Consignación', '4': 'Derivación'}" :key="num" 
               @click="toggleObtencion(num)"
               class="flex items-center justify-between p-4 bg-[#161b2a] hover:bg-[#1a202e] transition-colors cursor-pointer print:bg-white print:hover:bg-slate-50">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-400 print:text-slate-600">{{num}}.</span>
              <span class="text-xs font-bold text-slate-200 uppercase tracking-tight print:text-slate-900">{{label}}</span>
            </div>
            <div :class="['w-5 h-5 border rounded-sm flex items-center justify-center transition-colors print:border-slate-400', obtencion[num] ? 'bg-emerald-500 border-emerald-600' : 'bg-[#0a0f1c] border-slate-700/80 print:bg-slate-50 print:border-slate-300']">
              <Check v-if="obtencion[num]" :size="12" class="text-white" />
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- PAGE 2 -->
    <div class="w-full max-w-[600px] min-w-[320px] min-h-[33cm] py-[2cm] bg-[#161b2a] shadow-2xl rounded-xl overflow-hidden border border-slate-800/60 print:shadow-none print:border-none print:max-w-none print:w-full print:text-black print:p-0 print:m-0 print:break-after-page flex flex-col">
      
      <!-- Section III: Funcionario -->
      <section class="border-b border-slate-800/60 print:border-slate-300">
        <div class="bg-[#080d1a] px-6 py-3 print:bg-slate-100">
          <h3 class="text-slate-100 font-bold text-sm flex items-center gap-2 print:text-black">
            <User :size="16" class="text-emerald-400 print:text-black" />
            III. FUNCIONARIO QUE OBTIENE
          </h3>
        </div>
        <div class="p-6 space-y-6 bg-[#161b2a] print:bg-white print:grid print:grid-cols-2 print:gap-6 print:space-y-0">
          <div v-for="title in ['PROTECCIÓN', 'OBSERVACIÓN PRELIMINAR', 'FIJACIÓN', 'COLECCIÓN']" :key="title" class="bg-[#0a0f1c] rounded-lg p-5 border border-slate-800/60 break-inside-avoid page-break-inside-avoid print:bg-slate-50 print:border-slate-300">
            <h4 class="text-sm font-bold text-slate-200 mb-4 uppercase tracking-wider border-b border-slate-800/60 pb-2 print:text-slate-900 print:border-slate-200">{{title}}</h4>
            <div class="space-y-3 mb-6">
              <div class="flex flex-col gap-1">
                <span class="text-[10px] font-bold text-slate-400 uppercase print:text-slate-600">a. Nombres y Apellidos:</span>
                <input type="text" class="w-full border-b border-slate-700/80 bg-transparent focus:border-emerald-500 outline-none text-xs py-1 text-slate-200 print:border-slate-300 print:text-slate-900" />
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-[10px] font-bold text-slate-400 uppercase print:text-slate-600">b. C.I:</span>
                <input type="text" class="w-full border-b border-slate-700/80 bg-transparent focus:border-emerald-500 outline-none text-xs py-1 text-slate-200 print:border-slate-300 print:text-slate-900" />
              </div>
            </div>
            <div class="grid grid-cols-3 gap-3">
              <div class="space-y-1">
                <div class="aspect-square bg-[#161b2a] border border-slate-700/80 rounded relative overflow-hidden print:bg-emerald-50/50 print:border-emerald-200">
                  <FileText :size="16" class="text-emerald-500/50 absolute top-1 right-1 print:text-emerald-700" />
                  <span class="absolute top-1 left-1 text-[8px] text-emerald-500/70 uppercase font-bold print:text-emerald-800">Firma</span>
                </div>
                <span class="block text-[9px] text-center text-slate-400 uppercase print:text-slate-600">c. Firma</span>
              </div>
              <div class="space-y-1">
                <div class="aspect-square bg-[#161b2a] border border-slate-700/80 rounded relative overflow-hidden print:bg-emerald-50/50 print:border-emerald-200">
                  <Fingerprint :size="16" class="text-emerald-500/50 absolute top-1 right-1 print:text-emerald-700" />
                  <span class="absolute top-1 left-1 text-[8px] text-emerald-500/70 uppercase font-bold print:text-emerald-800">Huella</span>
                </div>
                <span class="block text-[9px] text-center text-slate-400 uppercase leading-tight print:text-slate-600">Pulgar Izq.</span>
              </div>
              <div class="space-y-1">
                <div class="aspect-square bg-[#161b2a] border border-slate-700/80 rounded relative overflow-hidden print:bg-emerald-50/50 print:border-emerald-200">
                  <Fingerprint :size="16" class="text-emerald-500/50 absolute top-1 right-1 print:text-emerald-700" />
                  <span class="absolute top-1 left-1 text-[8px] text-emerald-500/70 uppercase font-bold print:text-emerald-800">Huella</span>
                </div>
                <span class="block text-[9px] text-center text-slate-400 uppercase leading-tight print:text-slate-600">Pulgar Der.</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- PAGE 3 -->
    <div class="w-full max-w-[600px] min-w-[320px] min-h-[33cm] py-[2cm] bg-[#161b2a] shadow-2xl rounded-xl overflow-hidden border border-slate-800/60 print:shadow-none print:border-none print:max-w-none print:w-full print:text-black print:p-0 print:m-0 print:break-after-page flex flex-col">
      
      <!-- Section VI: Descripción -->
      <section class="border-b border-slate-800/60 print:border-slate-300">
        <div class="bg-[#080d1a] px-6 py-3 print:bg-slate-100">
          <h3 class="text-slate-100 font-bold text-sm flex items-center gap-2 print:text-black">
            <ClipboardCheck :size="16" class="text-emerald-400 print:text-black" />
            VI. DESCRIPCIÓN DE LA EVIDENCIA
          </h3>
        </div>
        <div class="p-0 bg-[#161b2a] print:bg-white">
          <div v-for="num in 7" :key="num" :class="['flex items-center px-6 py-3 border-b border-slate-800/60 last:border-0 print:border-slate-100', num % 2 === 0 ? 'bg-[#1a202e] print:bg-white' : 'bg-[#0a0f1c] print:bg-slate-50']">
            <span class="text-xs font-bold text-slate-400 w-8 print:text-slate-600">{{num}}</span>
            <input type="text" class="flex-1 bg-transparent border-none focus:ring-0 text-sm text-slate-200 print:text-slate-900" placeholder="..." />
          </div>
          <div class="p-4 flex justify-end items-center gap-3 bg-[#0a0f1c] border-t border-slate-800/60 print:bg-slate-50 print:border-slate-200">
            <span class="text-xs font-bold text-slate-400 uppercase print:text-slate-700">(ANEXO A)</span>
            <div class="w-5 h-5 border border-slate-700/80 rounded-sm bg-[#161b2a] flex items-center justify-center cursor-pointer hover:bg-[#1a202e] transition-colors print:border-slate-400 print:bg-emerald-50 print:hover:bg-emerald-100">
              <CheckCircle2 :size="12" class="text-emerald-500 print:text-emerald-600" />
            </div>
          </div>
        </div>
      </section>

      <!-- Section V: Transferencia -->
      <section>
        <div class="bg-[#080d1a] px-6 py-3 print:bg-slate-100">
          <h3 class="text-slate-100 font-bold text-sm flex items-center gap-2 print:text-black">
            <ArrowRightLeft :size="16" class="text-emerald-400 print:text-black" />
            V. TRANSFERENCIA DE EVIDENCIA
          </h3>
        </div>
        <div class="p-6 space-y-6 bg-[#161b2a] print:bg-white">
          <div>
            <h4 class="text-xs font-bold text-slate-200 mb-3 uppercase tracking-wider print:text-slate-900">a. MOTIVO:</h4>
            <div class="space-y-2 print:grid print:grid-cols-5 print:gap-2 print:space-y-0">
              <div v-for="(motivo, i) in ['Traslado', 'Peritaje', 'Resguardo', 'Disposición Judicial', 'Disposición Final']" :key="motivo" 
                   @click="toggleMotivo(motivo)"
                   class="flex items-center gap-2 p-3 bg-[#0a0f1c] rounded border border-slate-800/60 cursor-pointer hover:bg-[#1a202e] transition-colors print:bg-slate-50 print:border-slate-200 print:hover:bg-slate-100">
                <span class="text-[10px] font-bold text-slate-400 print:text-slate-600">{{i + 1}}.</span>
                <span class="text-[11px] font-medium text-slate-200 flex-1 print:text-slate-900">{{motivo}}</span>
                <div :class="['w-4 h-4 border rounded-sm flex items-center justify-center transition-colors print:border-slate-400', motivos[motivo] ? 'bg-emerald-500 border-emerald-600' : 'bg-[#161b2a] border-slate-700/80 print:bg-white print:border-slate-300']">
                  <Check v-if="motivos[motivo]" :size="10" class="text-white" />
                </div>
              </div>
            </div>
          </div>
          
          <div class="space-y-6 pt-4 print:grid print:grid-cols-2 print:gap-6 print:space-y-0 print:pt-0">
            <div v-for="title in ['b. ENTREGA', 'c. RECIBE']" :key="title" class="bg-[#0a0f1c] rounded-lg p-5 border border-slate-800/60 break-inside-avoid page-break-inside-avoid print:bg-slate-50 print:border-slate-300">
              <h4 class="text-sm font-bold text-slate-200 mb-4 uppercase tracking-wider border-b border-slate-800/60 pb-2 print:text-slate-900 print:border-slate-200">{{title}}</h4>
              <div class="space-y-3 mb-6">
                <div v-for="label in ['a. Nombres y Apellidos', 'b. Organismo', 'c. Despacho', 'd. C.I./Cred', 'e. Fecha']" :key="label" class="flex flex-col gap-1">
                  <span class="text-[10px] font-bold text-slate-400 uppercase print:text-slate-600">{{label}}:</span>
                  <input type="text" class="w-full border-b border-slate-700/80 bg-transparent focus:border-emerald-500 outline-none text-xs py-1 text-slate-200 print:border-slate-300 print:text-slate-900" />
                </div>
              </div>
              <div class="grid grid-cols-3 gap-3">
                <div class="space-y-1">
                  <div class="aspect-square bg-[#161b2a] border border-slate-700/80 rounded relative overflow-hidden print:bg-emerald-50/50 print:border-emerald-200">
                    <FileText :size="16" class="text-emerald-500/50 absolute top-1 right-1 print:text-emerald-700" />
                    <span class="absolute top-1 left-1 text-[8px] text-emerald-500/70 uppercase font-bold print:text-emerald-800">Firma</span>
                  </div>
                  <span class="block text-[9px] text-center text-slate-400 uppercase print:text-slate-600">f. Firma</span>
                </div>
                <div class="space-y-1">
                  <div class="aspect-square bg-[#161b2a] border border-slate-700/80 rounded relative overflow-hidden print:bg-emerald-50/50 print:border-emerald-200">
                    <Fingerprint :size="16" class="text-emerald-500/50 absolute top-1 right-1 print:text-emerald-700" />
                    <span class="absolute top-1 left-1 text-[8px] text-emerald-500/70 uppercase font-bold print:text-emerald-800">Huella</span>
                  </div>
                  <span class="block text-[9px] text-center text-slate-400 uppercase leading-tight print:text-slate-600">Pulgar Izq.</span>
                </div>
                <div class="space-y-1">
                  <div class="aspect-square bg-[#161b2a] border border-slate-700/80 rounded relative overflow-hidden print:bg-emerald-50/50 print:border-emerald-200">
                    <Fingerprint :size="16" class="text-emerald-500/50 absolute top-1 right-1 print:text-emerald-700" />
                    <span class="absolute top-1 left-1 text-[8px] text-emerald-500/70 uppercase font-bold print:text-emerald-800">Huella</span>
                  </div>
                  <span class="block text-[9px] text-center text-slate-400 uppercase leading-tight print:text-slate-600">Pulgar Der.</span>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-slate-800/60 print:border-slate-200">
            <h4 class="text-xs font-bold text-slate-200 mb-3 uppercase tracking-wider print:text-slate-900">d. OBSERVACIÓN</h4>
            <div class="space-y-2">
              <div v-for="n in 3" :key="n" class="h-8 border-b border-slate-800/60 flex items-center print:border-slate-200">
                <span class="text-[10px] text-slate-400 mr-4 print:text-slate-600">{{n}}</span>
                <input type="text" class="flex-1 bg-transparent border-none focus:ring-0 text-sm h-full text-slate-200 print:text-slate-900" />
              </div>
            </div>
            <p class="mt-6 text-[10px] text-slate-400 leading-relaxed italic border-l-2 border-emerald-500 pl-4 print:text-slate-700">
              Nota: la planilla de Registro de Cadena de Custodia debe permanecer siempre con la evidencia, y sólo en original, desde el instante de su llenado en el lugar de obtención hasta la disposición final de la evidencia.
            </p>
          </div>
        </div>
      </section>
    </div>
      
    <!-- CONTROLS -->
    <div class="w-full max-w-[600px] min-w-[320px] bg-[#161b2a] shadow-2xl rounded-xl overflow-hidden border border-slate-800/60 print:hidden flex flex-col">
      <!-- Action Buttons at the bottom -->
      <div class="p-6 bg-[#080d1a] flex flex-col gap-3 no-print">
        <button 
          @click="printDoc"
          class="w-full flex justify-center items-center gap-2 px-6 py-3 bg-emerald-600 rounded-xl text-sm font-bold text-white hover:bg-emerald-500 transition-all shadow-sm active:scale-95"
        >
          <Printer :size="18" />
          IMPRIMIR FORMULARIO
        </button>
        <button 
          @click="printDoc"
          class="w-full flex justify-center items-center gap-2 px-6 py-3 bg-[#161b2a] border border-slate-700/80 rounded-xl text-sm font-bold text-slate-300 hover:bg-[#1a202e] hover:text-white transition-all shadow-sm active:scale-95"
        >
          <Download :size="18" />
          EXPORTAR A PDF
        </button>
      </div>

      <footer class="p-8 flex flex-col items-center justify-center gap-1.5 no-print bg-[#0a0f1c] border-t border-slate-800/60">
        <div class="flex items-center gap-2">
          <div class="w-1.5 h-1.5 bg-[#0fa968] rounded-full"></div>
          <span class="text-slate-200 font-semibold tracking-tight text-sm">sha256.us</span>
        </div>
        <p class="text-slate-500 text-[10px] font-mono uppercase tracking-widest">
          Laboratorio Informático Forense
        </p>
      </footer>
    </div>
  </div>
</template>

<style>
@media print {
  @page {
    size: legal;
    margin-top: 2cm;
    margin-bottom: 2cm;
  }
}
</style>
