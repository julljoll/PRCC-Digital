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
  <div class="min-h-screen bg-slate-100 py-8 px-4 sm:px-6 lg:px-8 print:p-0 print:bg-white flex justify-center">
    <!-- Email-like Container (Max 600px, Min 320px) -->
    <div class="w-full max-w-[600px] min-w-[320px] bg-white shadow-xl rounded-xl overflow-hidden border border-slate-200 print:shadow-none print:border-none print:max-w-none print:w-full">
      
      <!-- Header Section -->
      <div class="bg-emerald-600 p-6 text-center border-b-4 border-emerald-800">
        <h2 class="text-white font-bold text-lg uppercase tracking-widest leading-tight">
          Planilla de Registro de Cadena de Custodia
        </h2>
        <p class="text-emerald-50 opacity-90 text-xs mt-2 tracking-widest">(PRCC)</p>
      </div>

      <!-- Section I: Datos Generales -->
      <section class="border-b border-slate-200">
        <div class="bg-slate-900 px-6 py-3">
          <h3 class="text-white font-bold text-sm flex items-center gap-2">
            <FileText :size="16" class="text-emerald-300" />
            I. DATOS GENERALES
          </h3>
        </div>
        <div class="p-6 space-y-4 bg-slate-50/50 print:grid print:grid-cols-2 print:gap-4 print:space-y-0">
          <!-- Stacked for email layout -->
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">a. N° de Expediente</label>
            <input type="text" v-model="formData.expediente" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">b. N° PRCC</label>
            <input type="text" v-model="formData.prcc" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">c. Despacho que instruye</label>
            <input type="text" v-model="formData.despachoInstruye" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">d. Organismo que investiga e instructivo</label>
            <input type="text" v-model="formData.organismoInvestiga" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">e. Despacho que inicia la custodia</label>
            <input type="text" v-model="formData.despachoCustodia" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">f. Organismo que custodia</label>
            <input type="text" v-model="formData.organismoCustodia" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">g. Dirección de Obtención</label>
            <input type="text" v-model="formData.direccionObtencion" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
          <div class="space-y-1">
            <label class="block text-[11px] font-bold text-slate-700 uppercase tracking-tight">h. Fecha y Hora</label>
            <input type="text" v-model="formData.fechaHora" class="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all print:border-slate-300 print:py-1" />
          </div>
        </div>
      </section>

      <!-- Section II: Formas de Obtención -->
      <section class="border-b border-slate-200">
        <div class="bg-slate-900 px-6 py-3">
          <h3 class="text-white font-bold text-sm flex items-center gap-2">
            <Search :size="16" class="text-emerald-300" />
            II. FORMAS DE OBTENCIÓN
          </h3>
        </div>
        <div class="grid grid-cols-2 print:grid-cols-4 divide-x divide-y divide-slate-200 border-b border-slate-200">
          <div v-for="(label, num) in {'1': 'Técnica', '2': 'Aseguramiento', '3': 'Consignación', '4': 'Derivación'}" :key="num" 
               @click="toggleObtencion(num)"
               class="flex items-center justify-between p-4 bg-white hover:bg-slate-50 transition-colors cursor-pointer">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-600">{{num}}.</span>
              <span class="text-xs font-bold text-slate-900 uppercase tracking-tight">{{label}}</span>
            </div>
            <div :class="['w-5 h-5 border rounded-sm flex items-center justify-center transition-colors print:border-slate-400', obtencion[num] ? 'bg-emerald-500 border-emerald-600' : 'bg-slate-50 border-slate-300']">
              <Check v-if="obtencion[num]" :size="12" class="text-white" />
            </div>
          </div>
        </div>
      </section>

      <!-- Section III: Funcionario -->
      <section class="border-b border-slate-200">
        <div class="bg-slate-900 px-6 py-3">
          <h3 class="text-white font-bold text-sm flex items-center gap-2">
            <User :size="16" class="text-emerald-300" />
            III. FUNCIONARIO QUE OBTIENE
          </h3>
        </div>
        <div class="p-6 space-y-6 print:grid print:grid-cols-2 print:gap-6 print:space-y-0">
          <div v-for="title in ['PROTECCIÓN', 'OBSERVACIÓN PRELIMINAR', 'FIJACIÓN', 'COLECCIÓN']" :key="title" class="bg-slate-50 rounded-lg p-5 border border-slate-200 break-inside-avoid page-break-inside-avoid print:bg-white print:border-slate-300">
            <h4 class="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wider border-b border-slate-200 pb-2">{{title}}</h4>
            <div class="space-y-3 mb-6">
              <div class="flex flex-col gap-1">
                <span class="text-[10px] font-bold text-slate-600 uppercase">a. Nombres y Apellidos:</span>
                <input type="text" class="w-full border-b border-slate-300 bg-transparent focus:border-emerald-500 outline-none text-xs py-1 text-slate-900" />
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-[10px] font-bold text-slate-600 uppercase">b. C.I:</span>
                <input type="text" class="w-full border-b border-slate-300 bg-transparent focus:border-emerald-500 outline-none text-xs py-1 text-slate-900" />
              </div>
            </div>
            <div class="grid grid-cols-3 gap-3">
              <div class="space-y-1">
                <div class="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
                  <FileText :size="16" class="text-emerald-700 absolute top-1 right-1" />
                  <span class="absolute top-1 left-1 text-[8px] text-emerald-800 uppercase font-bold">Firma</span>
                </div>
                <span class="block text-[9px] text-center text-slate-600 uppercase">c. Firma</span>
              </div>
              <div class="space-y-1">
                <div class="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
                  <Fingerprint :size="16" class="text-emerald-700 absolute top-1 right-1" />
                  <span class="absolute top-1 left-1 text-[8px] text-emerald-800 uppercase font-bold">Huella</span>
                </div>
                <span class="block text-[9px] text-center text-slate-600 uppercase leading-tight">Pulgar Izq.</span>
              </div>
              <div class="space-y-1">
                <div class="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
                  <Fingerprint :size="16" class="text-emerald-700 absolute top-1 right-1" />
                  <span class="absolute top-1 left-1 text-[8px] text-emerald-800 uppercase font-bold">Huella</span>
                </div>
                <span class="block text-[9px] text-center text-slate-600 uppercase leading-tight">Pulgar Der.</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Section VI: Descripción -->
      <section class="border-b border-slate-200">
        <div class="bg-slate-900 px-6 py-3">
          <h3 class="text-white font-bold text-sm flex items-center gap-2">
            <ClipboardCheck :size="16" class="text-emerald-300" />
            VI. DESCRIPCIÓN DE LA EVIDENCIA
          </h3>
        </div>
        <div class="p-0">
          <div v-for="num in 7" :key="num" :class="['flex items-center px-6 py-3 border-b border-slate-100 last:border-0', num % 2 === 0 ? 'bg-white' : 'bg-slate-50']">
            <span class="text-xs font-bold text-slate-600 w-8">{{num}}</span>
            <input type="text" class="flex-1 bg-transparent border-none focus:ring-0 text-sm text-slate-900" placeholder="..." />
          </div>
          <div class="p-4 flex justify-end items-center gap-3 bg-slate-50 border-t border-slate-200">
            <span class="text-xs font-bold text-slate-700 uppercase">(ANEXO A)</span>
            <div class="w-5 h-5 border border-slate-400 rounded-sm bg-emerald-50 flex items-center justify-center cursor-pointer hover:bg-emerald-100 transition-colors">
              <CheckCircle2 :size="12" class="text-emerald-600" />
            </div>
          </div>
        </div>
      </section>

      <!-- Section V: Transferencia -->
      <section>
        <div class="bg-slate-900 px-6 py-3">
          <h3 class="text-white font-bold text-sm flex items-center gap-2">
            <ArrowRightLeft :size="16" class="text-emerald-300" />
            V. TRANSFERENCIA DE EVIDENCIA
          </h3>
        </div>
        <div class="p-6 space-y-6">
          <div>
            <h4 class="text-xs font-bold text-slate-900 mb-3 uppercase tracking-wider">a. MOTIVO:</h4>
            <div class="space-y-2 print:grid print:grid-cols-5 print:gap-2 print:space-y-0">
              <div v-for="(motivo, i) in ['Traslado', 'Peritaje', 'Resguardo', 'Disposición Judicial', 'Disposición Final']" :key="motivo" 
                   @click="toggleMotivo(motivo)"
                   class="flex items-center gap-2 p-3 bg-slate-50 rounded border border-slate-200 cursor-pointer hover:bg-slate-100 transition-colors">
                <span class="text-[10px] font-bold text-slate-600">{{i + 1}}.</span>
                <span class="text-[11px] font-medium text-slate-900 flex-1">{{motivo}}</span>
                <div :class="['w-4 h-4 border rounded-sm flex items-center justify-center transition-colors print:border-slate-400', motivos[motivo] ? 'bg-emerald-500 border-emerald-600' : 'bg-white border-slate-300']">
                  <Check v-if="motivos[motivo]" :size="10" class="text-white" />
                </div>
              </div>
            </div>
          </div>
          
          <div class="space-y-6 pt-4 print:grid print:grid-cols-2 print:gap-6 print:space-y-0 print:pt-0">
            <div v-for="title in ['b. ENTREGA', 'c. RECIBE']" :key="title" class="bg-slate-50 rounded-lg p-5 border border-slate-200 break-inside-avoid page-break-inside-avoid print:bg-white print:border-slate-300">
              <h4 class="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wider border-b border-slate-200 pb-2">{{title}}</h4>
              <div class="space-y-3 mb-6">
                <div v-for="label in ['a. Nombres y Apellidos', 'b. Organismo', 'c. Despacho', 'd. C.I./Cred', 'e. Fecha']" :key="label" class="flex flex-col gap-1">
                  <span class="text-[10px] font-bold text-slate-600 uppercase">{{label}}:</span>
                  <input type="text" class="w-full border-b border-slate-300 bg-transparent focus:border-emerald-500 outline-none text-xs py-1 text-slate-900" />
                </div>
              </div>
              <div class="grid grid-cols-3 gap-3">
                <div class="space-y-1">
                  <div class="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
                    <FileText :size="16" class="text-emerald-700 absolute top-1 right-1" />
                    <span class="absolute top-1 left-1 text-[8px] text-emerald-800 uppercase font-bold">Firma</span>
                  </div>
                  <span class="block text-[9px] text-center text-slate-600 uppercase">f. Firma</span>
                </div>
                <div class="space-y-1">
                  <div class="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
                    <Fingerprint :size="16" class="text-emerald-700 absolute top-1 right-1" />
                    <span class="absolute top-1 left-1 text-[8px] text-emerald-800 uppercase font-bold">Huella</span>
                  </div>
                  <span class="block text-[9px] text-center text-slate-600 uppercase leading-tight">Pulgar Izq.</span>
                </div>
                <div class="space-y-1">
                  <div class="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
                    <Fingerprint :size="16" class="text-emerald-700 absolute top-1 right-1" />
                    <span class="absolute top-1 left-1 text-[8px] text-emerald-800 uppercase font-bold">Huella</span>
                  </div>
                  <span class="block text-[9px] text-center text-slate-600 uppercase leading-tight">Pulgar Der.</span>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-slate-200">
            <h4 class="text-xs font-bold text-slate-900 mb-3 uppercase tracking-wider">d. OBSERVACIÓN</h4>
            <div class="space-y-2">
              <div v-for="n in 3" :key="n" class="h-8 border-b border-slate-200 flex items-center">
                <span class="text-[10px] text-slate-500 mr-4">{{n}}</span>
                <input type="text" class="flex-1 bg-transparent border-none focus:ring-0 text-sm h-full text-slate-900" />
              </div>
            </div>
            <p class="mt-6 text-[10px] text-slate-700 leading-relaxed italic border-l-2 border-emerald-500 pl-4">
              Nota: la planilla de Registro de Cadena de Custodia debe permanecer siempre con la evidencia, y sólo en original, desde el instante de su llenado en el lugar de obtención hasta la disposición final de la evidencia.
            </p>
          </div>
        </div>
      </section>
      
      <!-- Action Buttons at the bottom -->
      <div class="p-6 bg-slate-50 border-t border-slate-200 flex flex-col gap-3 no-print">
        <button 
          @click="printDoc"
          class="w-full flex justify-center items-center gap-2 px-6 py-3 bg-emerald-600 rounded-xl text-sm font-bold text-white hover:bg-emerald-700 transition-all shadow-sm active:scale-95"
        >
          <Printer :size="18" />
          IMPRIMIR FORMULARIO
        </button>
        <button 
          @click="printDoc"
          class="w-full flex justify-center items-center gap-2 px-6 py-3 bg-white border border-slate-200 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 transition-all shadow-sm active:scale-95"
        >
          <Download :size="18" />
          EXPORTAR A PDF
        </button>
      </div>

      <footer class="p-6 text-center no-print bg-slate-100 border-t border-slate-200">
        <p class="text-slate-600 text-[10px] font-medium uppercase tracking-wider">
          &copy; {{ new Date().getFullYear() }} PRCC Digital
        </p>
      </footer>
    </div>
  </div>
</template>
