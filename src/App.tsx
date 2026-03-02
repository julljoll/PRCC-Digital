import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Shield, 
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
} from 'lucide-react';

export default function App() {
  const [formData, setFormData] = useState({
    expediente: '',
    prcc: '',
    despachoInstruye: '',
    organismoInvestiga: '',
    despachoCustodia: '',
    organismoCustodia: '',
    direccionObtencion: '',
    fechaHora: new Date().toLocaleString(),
  });

  const [obtencion, setObtencion] = useState<Record<string, boolean>>({
    '1': false,
    '2': false,
    '3': false,
    '4': false,
  });

  const [motivos, setMotivos] = useState<Record<string, boolean>>({
    'Traslado': false,
    'Peritaje': false,
    'Resguardo': false,
    'Disposición Judicial': false,
    'Disposición Final': false,
  });

  const toggleObtencion = (id: string) => {
    setObtencion(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleMotivo = (id: string) => {
    setMotivos(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      {/* Main Document */}
      <motion.main 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl mx-auto bg-white document-shadow rounded-sm overflow-hidden border border-slate-200"
      >
        {/* Header Section */}
        <div className="bg-emerald-600 p-6 text-center border-b border-emerald-700">
          <h2 className="text-white font-bold text-xl uppercase tracking-widest">
            PLANILLA DE REGISTRO DE CADENA DE CUSTODIA (PRCC)
          </h2>
        </div>


        {/* Section I: Datos Generales */}
        <section className="border-b border-slate-200">
          <div className="bg-slate-900 px-6 py-2">
            <h3 className="text-white font-bold text-sm flex items-center gap-2">
              <FileText size={16} className="text-emerald-400" />
              I. DATOS GENERALES
            </h3>
          </div>
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50/50">
            <div className="space-y-4">
              <InputField label="a. N° de Expediente" value={formData.expediente} onChange={(v) => setFormData({...formData, expediente: v})} />
              <InputField label="c. Despacho que instruye" value={formData.despachoInstruye} onChange={(v) => setFormData({...formData, despachoInstruye: v})} />
              <InputField label="e. Despacho que inicia la custodia" value={formData.despachoCustodia} onChange={(v) => setFormData({...formData, despachoCustodia: v})} />
            </div>
            <div className="space-y-4">
              <InputField label="b. N° PRCC" value={formData.prcc} onChange={(v) => setFormData({...formData, prcc: v})} />
              <InputField label="d. Organismo que investiga e instructivo" value={formData.organismoInvestiga} onChange={(v) => setFormData({...formData, organismoInvestiga: v})} />
              <InputField label="f. Organismo que custodia" value={formData.organismoCustodia} onChange={(v) => setFormData({...formData, organismoCustodia: v})} />
            </div>
            <div className="md:col-span-2 space-y-4">
              <InputField label="g. Dirección de Obtención" value={formData.direccionObtencion} onChange={(v) => setFormData({...formData, direccionObtencion: v})} />
              <InputField label="h. Fecha y Hora" value={formData.fechaHora} onChange={(v) => setFormData({...formData, fechaHora: v})} />
            </div>
          </div>
        </section>

        {/* Section II: Formas de Obtención */}
        <section className="border-b border-slate-200">
          <div className="bg-slate-900 px-6 py-2">
            <h3 className="text-white font-bold text-sm flex items-center gap-2">
              <Search size={16} className="text-emerald-400" />
              II. FORMAS DE OBTENCIÓN DE LA EVIDENCIA
            </h3>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-slate-200">
            <ObtencionItem number="1" label="Técnica" checked={obtencion['1']} onToggle={() => toggleObtencion('1')} />
            <ObtencionItem number="2" label="Aseguramiento" checked={obtencion['2']} onToggle={() => toggleObtencion('2')} />
            <ObtencionItem number="3" label="Consignación" checked={obtencion['3']} onToggle={() => toggleObtencion('3')} />
            <ObtencionItem number="4" label="Derivación" checked={obtencion['4']} onToggle={() => toggleObtencion('4')} />
          </div>
        </section>

        {/* Section III: Funcionario */}
        <section className="border-b border-slate-200">
          <div className="bg-slate-900 px-6 py-2">
            <h3 className="text-white font-bold text-sm flex items-center gap-2">
              <User size={16} className="text-emerald-400" />
              III. FUNCIONARIO QUE OBTIENE LA EVIDENCIA
            </h3>
          </div>
          <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
            <FuncionarioCard title="PROTECCIÓN" />
            <FuncionarioCard title="OBSERVACIÓN PRELIMINAR" />
            <FuncionarioCard title="FIJACIÓN" />
            <FuncionarioCard title="COLECCIÓN" />
          </div>
        </section>

        {/* Section VI: Descripción */}
        <section className="border-b border-slate-200">
          <div className="bg-slate-900 px-6 py-2">
            <h3 className="text-white font-bold text-sm flex items-center gap-2">
              <ClipboardCheck size={16} className="text-emerald-400" />
              VI. DESCRIPCIÓN DE LA EVIDENCIA
            </h3>
          </div>
          <div className="p-0">
            {[1, 2, 3, 4, 5, 6, 7].map((num) => (
              <div key={num} className={`flex items-center px-6 py-3 border-b border-slate-100 last:border-0 ${num % 2 === 0 ? 'bg-white' : 'bg-slate-50'}`}>
                <span className="text-xs font-bold text-slate-400 w-8">{num}</span>
                <input type="text" className="flex-1 bg-transparent border-none focus:ring-0 text-sm" placeholder="..." />
              </div>
            ))}
            <div className="p-4 flex justify-end items-center gap-3 bg-slate-50 border-t border-slate-200">
              <span className="text-xs font-bold text-slate-600 uppercase">(ANEXO A)</span>
              <div className="w-5 h-5 border border-slate-400 rounded-sm bg-emerald-50 flex items-center justify-center cursor-pointer hover:bg-emerald-100 transition-colors">
                <CheckCircle2 size={12} className="text-emerald-600" />
              </div>
            </div>
          </div>
        </section>

        {/* Section V: Transferencia */}
        <section>
          <div className="bg-slate-900 px-6 py-2">
            <h3 className="text-white font-bold text-sm flex items-center gap-2">
              <ArrowRightLeft size={16} className="text-emerald-400" />
              V. TRANSFERENCIA DE EVIDENCIA
            </h3>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <h4 className="text-xs font-bold text-slate-900 mb-3 uppercase tracking-wider">a. MOTIVO:</h4>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {['Traslado', 'Peritaje', 'Resguardo', 'Disposición Judicial', 'Disposición Final'].map((motivo, i) => (
                  <div 
                    key={motivo} 
                    onClick={() => toggleMotivo(motivo)}
                    className="flex items-center gap-2 p-2 bg-slate-50 rounded border border-slate-200 cursor-pointer hover:bg-slate-100 transition-colors"
                  >
                    <span className="text-[10px] font-bold text-slate-400">{i + 1}.</span>
                    <span className="text-[11px] font-medium text-slate-700 flex-1">{motivo}</span>
                    <div className={`w-4 h-4 border border-slate-300 rounded-sm flex items-center justify-center transition-colors ${motivos[motivo] ? 'bg-emerald-500 border-emerald-600' : 'bg-white'}`}>
                      {motivos[motivo] && <Check size={10} className="text-white" />}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 pt-4">
              <TransferCard title="b. ENTREGA" />
              <TransferCard title="c. RECIBE" />
            </div>

            <div className="mt-8 pt-6 border-t border-slate-200">
              <h4 className="text-xs font-bold text-slate-900 mb-3 uppercase tracking-wider">d. OBSERVACIÓN</h4>
              <div className="space-y-2">
                {[1, 2, 3].map(n => (
                  <div key={n} className="h-8 border-b border-slate-200 flex items-center">
                    <span className="text-[10px] text-slate-300 mr-4">{n}</span>
                    <input type="text" className="flex-1 bg-transparent border-none focus:ring-0 text-sm h-full" />
                  </div>
                ))}
              </div>
              <p className="mt-6 text-[10px] text-slate-500 leading-relaxed italic border-l-2 border-emerald-500 pl-4">
                Nota: la planilla de Registro de Cadena de Custodia debe permanecer siempre con la evidencia, y sólo en original, desde el instante de su llenado en el lugar de obtención hasta la disposición final de la evidencia.
              </p>
            </div>
          </div>
        </section>
      </motion.main>

      {/* Action Buttons at the bottom */}
      <div className="max-w-5xl mx-auto mt-8 flex justify-center gap-4 no-print">
        <button 
          onClick={() => window.print()}
          className="flex items-center gap-2 px-6 py-3 bg-white border border-slate-200 rounded-xl text-sm font-bold text-slate-600 hover:bg-slate-50 transition-all shadow-sm hover:shadow-md active:scale-95"
        >
          <Printer size={18} />
          IMPRIMIR FORMULARIO
        </button>
        <button 
          onClick={() => window.print()}
          className="flex items-center gap-2 px-6 py-3 bg-emerald-600 rounded-xl text-sm font-bold text-white hover:bg-emerald-700 transition-all shadow-sm hover:shadow-md active:scale-95"
        >
          <Download size={18} />
          EXPORTAR A PDF
        </button>
      </div>

      <footer className="max-w-5xl mx-auto mt-12 text-center no-print border-t border-slate-200 pt-8">
        <p className="text-slate-400 text-xs font-medium">
          &copy; {new Date().getFullYear()} PRCC Digital - Sistema de Gestión de Evidencias
        </p>
      </footer>
    </div>
  );
}

function InputField({ label, value, onChange }: { label: string, value: string, onChange: (v: string) => void }) {
  return (
    <div className="space-y-1">
      <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-tight">{label}</label>
      <input 
        type="text" 
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-white border border-slate-200 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 outline-none transition-all"
      />
    </div>
  );
}

function ObtencionItem({ number, label, checked, onToggle }: { number: string, label: string, checked: boolean, onToggle: () => void }) {
  return (
    <div 
      onClick={onToggle}
      className="flex items-center justify-between p-4 bg-white hover:bg-slate-50 transition-colors cursor-pointer"
    >
      <div className="flex items-center gap-3">
        <span className="text-xs font-bold text-slate-400">{number}.</span>
        <span className="text-xs font-bold text-slate-800 uppercase tracking-tight">{label}</span>
      </div>
      <div className={`w-5 h-5 border border-slate-300 rounded-sm flex items-center justify-center transition-colors ${checked ? 'bg-emerald-500 border-emerald-600' : 'bg-slate-50'}`}>
        {checked && <Check size={12} className="text-white" />}
      </div>
    </div>
  );
}

function FuncionarioCard({ title }: { title: string }) {
  return (
    <div className="bg-slate-50 rounded-lg p-5 border border-slate-200">
      <h4 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wider border-b border-slate-200 pb-2">{title}</h4>
      <div className="space-y-3 mb-6">
        <div className="flex items-end gap-2">
          <span className="text-[10px] font-bold text-slate-400 whitespace-nowrap">a. Nombres y Apellidos:</span>
          <input type="text" className="flex-1 border-b border-slate-300 bg-transparent focus:border-emerald-500 outline-none text-xs" />
        </div>
        <div className="flex items-end gap-2">
          <span className="text-[10px] font-bold text-slate-400 whitespace-nowrap">b. C.I:</span>
          <input type="text" className="flex-1 border-b border-slate-300 bg-transparent focus:border-emerald-500 outline-none text-xs" />
        </div>
      </div>
      <div className="grid grid-cols-3 gap-3">
        <div className="space-y-1">
          <div className="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
            <FileText className="text-emerald-200 absolute top-1 right-1" size={16} />
            <span className="absolute top-1 left-1 text-[8px] text-emerald-300 uppercase font-bold">Firma</span>
          </div>
          <span className="block text-[9px] text-center text-slate-400 uppercase">c. Firma</span>
        </div>
        <div className="space-y-1">
          <div className="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
            <Fingerprint className="text-emerald-200 absolute top-1 right-1" size={16} />
            <span className="absolute top-1 left-1 text-[8px] text-emerald-300 uppercase font-bold">Huella</span>
          </div>
          <span className="block text-[9px] text-center text-slate-400 uppercase leading-tight">Pulgar Izquierdo</span>
        </div>
        <div className="space-y-1">
          <div className="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
            <Fingerprint className="text-emerald-200 absolute top-1 right-1" size={16} />
            <span className="absolute top-1 left-1 text-[8px] text-emerald-300 uppercase font-bold">Huella</span>
          </div>
          <span className="block text-[9px] text-center text-slate-400 uppercase leading-tight">Pulgar Derecho</span>
        </div>
      </div>
    </div>
  );
}

function TransferCard({ title }: { title: string }) {
  return (
    <div className="bg-slate-50 rounded-lg p-5 border border-slate-200">
      <h4 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wider border-b border-slate-200 pb-2">{title}</h4>
      <div className="space-y-3 mb-6">
        {['a. Nombres y Apellidos', 'b. Organismo', 'c. Despacho', 'd. C.I./Cred', 'e. Fecha'].map(label => (
          <div key={label} className="flex items-end gap-2">
            <span className="text-[10px] font-bold text-slate-400 whitespace-nowrap">{label}:</span>
            <input type="text" className="flex-1 border-b border-slate-300 bg-transparent focus:border-emerald-500 outline-none text-xs" />
          </div>
        ))}
      </div>
      <div className="grid grid-cols-3 gap-3">
        <div className="space-y-1">
          <div className="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
            <FileText className="text-emerald-200 absolute top-1 right-1" size={16} />
            <span className="absolute top-1 left-1 text-[8px] text-emerald-300 uppercase font-bold">Firma</span>
          </div>
          <span className="block text-[9px] text-center text-slate-400 uppercase">f. Firma</span>
        </div>
        <div className="space-y-1">
          <div className="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
            <Fingerprint className="text-emerald-200 absolute top-1 right-1" size={16} />
            <span className="absolute top-1 left-1 text-[8px] text-emerald-300 uppercase font-bold">Huella</span>
          </div>
          <span className="block text-[9px] text-center text-slate-400 uppercase leading-tight">Pulgar Izquierdo</span>
        </div>
        <div className="space-y-1">
          <div className="aspect-square bg-emerald-50/50 border border-emerald-200 rounded relative overflow-hidden">
            <Fingerprint className="text-emerald-200 absolute top-1 right-1" size={16} />
            <span className="absolute top-1 left-1 text-[8px] text-emerald-300 uppercase font-bold">Huella</span>
          </div>
          <span className="block text-[9px] text-center text-slate-400 uppercase leading-tight">Pulgar Derecho</span>
        </div>
      </div>
    </div>
  );
}
