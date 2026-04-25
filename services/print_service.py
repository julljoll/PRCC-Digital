"""
Servicio de impresión y generación de PDF para formularios forenses
Utiliza reportlab para generar documentos legales imprimibles
"""

from io import BytesIO
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfgen import canvas


class PrintService:
    """Servicio para generación de PDF e impresión de formularios"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos_personalizados()
    
    def _configurar_estilos_personalizados(self):
        """Configurar estilos personalizados para documentos legales"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TituloPrincipal',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.black,
            spaceAfter=12,
            alignment=1  # Center
        ))
        
        # Subtítulo de sección
        self.styles.add(ParagraphStyle(
            name='SubtituloSeccion',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.darkblue,
            spaceAfter=8,
            spaceBefore=12
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12
        ))
        
        # Texto pequeño para labels
        self.styles.add(ParagraphStyle(
            name='Label',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.gray
        ))
    
    def generar_prcc_pdf(self, datos_caso: Dict[str, Any], datos_dispositivo: Dict[str, Any], 
                         datos_prcc: Dict[str, Any]) -> bytes:
        """
        Generar PDF de la Planilla de Registro de Cadena de Custodia
        
        Args:
            datos_caso: Información del caso
            datos_dispositivo: Información del dispositivo
            datos_prcc: Información de la PRCC
        
        Returns:
            Bytes del PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elementos = []
        
        # Encabezado institucional
        elementos.append(Paragraph("REPÚBLICA BOLIVARIANA DE VENEZUELA", self.styles['TextoNormal']))
        elementos.append(Paragraph("MINISTERIO PÚBLICO", self.styles['TextoNormal']))
        elementos.append(Paragraph("DIRECCIÓN GENERAL DE CIENCIAS FORENSES", self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.3*inch))
        
        # Título del documento
        elementos.append(Paragraph("PLANILLA DE REGISTRO DE CADENA DE CUSTODIA", self.styles['TituloPrincipal']))
        elementos.append(Paragraph(f"N° {datos_prcc.get('numero_prcc', 'PENDING')}", self.styles['SubtituloSeccion']))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Datos generales del caso
        datos_generales = [
            ['Número de Expediente:', datos_caso.get('numero_caso', '')],
            ['Fiscal Asignado:', datos_caso.get('fiscal', '')],
            ['Fecha de Registro:', datos_prcc.get('fecha_creacion', datetime.now().strftime('%Y-%m-%d %H:%M'))],
            ['Órgano Receptor:', datos_prcc.get('organo', '')]
        ]
        
        tabla_generales = Table(datos_generales, colWidths=[2.5*inch, 4*inch])
        tabla_generales.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elementos.append(tabla_generales)
        elementos.append(Spacer(1, 0.2*inch))
        
        # Descripción de la evidencia
        elementos.append(Paragraph("DESCRIPCIÓN DE LA EVIDENCIA", self.styles['SubtituloSeccion']))
        
        datos_evidencia = [
            ['Tipo de Objeto:', 'Dispositivo Móvil'],
            ['Marca:', datos_dispositivo.get('marca', '')],
            ['Modelo:', datos_dispositivo.get('modelo', '')],
            ['IMEI:', datos_dispositivo.get('imei', '')],
            ['SIM Card N°:', datos_dispositivo.get('sim_card', '')],
            ['Número Telefónico:', datos_dispositivo.get('numero_tel', '')],
            ['Estado Físico:', datos_dispositivo.get('estado_fisico', '')],
            ['Modo de Aislamiento:', 'Modo Avión' if datos_dispositivo.get('modo_aislamiento') == 'modo_avion' else 'Bolsa Faraday']
        ]
        
        tabla_evidencia = Table(datos_evidencia, colWidths=[2.5*inch, 4*inch])
        tabla_evidencia.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elementos.append(tabla_evidencia)
        elementos.append(Spacer(1, 0.2*inch))
        
        # Hashes y embalaje
        elementos.append(Paragraph("INTEGRIDAD Y EMBALAJE", self.styles['SubtituloSeccion']))
        
        datos_integridad = [
            ['Hash SHA-256:', datos_prcc.get('hash_sha256', 'N/A')],
            ['Hash MD5:', datos_prcc.get('hash_md5', 'N/A')],
            ['Tipo de Embalaje:', datos_prcc.get('tipo_embalaje', '')],
            ['N° de Precinto:', datos_prcc.get('numero_precinto', '')],
            ['Estado del Embalaje:', datos_prcc.get('estado_embalaje', '')]
        ]
        
        tabla_integridad = Table(datos_integridad, colWidths=[2.5*inch, 4*inch])
        tabla_integridad.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('WORDWRAP', (1, 0), (1, 1), True)
        ]))
        elementos.append(tabla_integridad)
        elementos.append(Spacer(1, 0.3*inch))
        
        # Funcionario colector
        elementos.append(Paragraph("FUNCIONARIO COLECTOR", self.styles['SubtituloSeccion']))
        
        datos_funcionario = [
            ['Nombre:', datos_prcc.get('funcionario_colector', '')],
            ['Cargo:', datos_prcc.get('cargo', '')],
            ['Firma:', '___________________________'],
            ['Huella Dactilar:', '[Espacio para huella del pulgar derecho]']
        ]
        
        tabla_funcionario = Table(datos_funcionario, colWidths=[2.5*inch, 4*inch])
        tabla_funcionario.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 2), (-1, 3), 20)
        ]))
        elementos.append(tabla_funcionario)
        
        # Pie de página
        elementos.append(Spacer(1, 0.5*inch))
        elementos.append(Paragraph(
            "Este documento certifica la cadena de custodia de la evidencia digital "
            "de acuerdo con los protocolos establecidos en el Manual de Procedimiento "
            "Forense venezolano.",
            self.styles['Label']
        ))
        elementos.append(Paragraph(
            f"Generado electrónicamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Label']
        ))
        
        # Construir PDF
        doc.build(elementos)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def generar_dictamen_pdf(self, datos_caso: Dict[str, Any], datos_dictamen: Dict[str, Any],
                             datos_dispositivo: Dict[str, Any], evidencias: List[Dict[str, Any]]) -> bytes:
        """
        Generar PDF del Dictamen Pericial
        
        Args:
            datos_caso: Información del caso
            datos_dictamen: Información del dictamen
            datos_dispositivo: Información del dispositivo
            evidencias: Lista de evidencias derivadas
        
        Returns:
            Bytes del PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        elementos = []
        
        # Encabezado
        elementos.append(Paragraph("REPÚBLICA BOLIVARIANA DE VENEZUELA", self.styles['TextoNormal']))
        elementos.append(Paragraph("MINISTERIO PÚBLICO", self.styles['TextoNormal']))
        elementos.append(Paragraph("DIRECCIÓN GENERAL DE CIENCIAS FORENSES", self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.3*inch))
        
        # Título
        numero_dictamen = datos_dictamen.get('numero_dictamen', 'PENDING')
        elementos.append(Paragraph(f"DICTAMEN PERICIAL N° {numero_dictamen}", self.styles['TituloPrincipal']))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Motivo
        elementos.append(Paragraph("1. MOTIVO", self.styles['SubtituloSeccion']))
        motivo = datos_dictamen.get('motivo', 'Sin especificar')
        elementos.append(Paragraph(motivo, self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Descripción de la evidencia
        elementos.append(Paragraph("2. DESCRIPCIÓN DE LA EVIDENCIA", self.styles['SubtituloSeccion']))
        descripcion = (
            f"Dispositivo móvil marca {datos_dispositivo.get('marca', 'N/A')} modelo {datos_dispositivo.get('modelo', 'N/A')}, "
            f"con IMEI {datos_dispositivo.get('imei', 'N/A')}, número de SIM {datos_dispositivo.get('sim_card', 'N/A')}. "
            f"Estado físico: {datos_dispositivo.get('estado_fisico', 'N/A')}."
        )
        elementos.append(Paragraph(descripcion, self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Exámenes practicados
        elementos.append(Paragraph("3. EXÁMENES PRACTICADOS", self.styles['SubtituloSeccion']))
        examenes = datos_dictamen.get('examenes_practicados', 'Sin especificar')
        elementos.append(Paragraph(examenes, self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Resultados
        elementos.append(Paragraph("4. RESULTADOS OBTENIDOS", self.styles['SubtituloSeccion']))
        
        if evidencias:
            datos_tabla = [['Archivo', 'Tamaño', 'Fecha Creación', 'Hash SHA-256']]
            for ev in evidencias:
                tamano_kb = ev.get('tamanio_bytes', 0) / 1024
                datos_tabla.append([
                    ev.get('nombre_nativo', 'N/A'),
                    f"{tamano_kb:.2f} KB",
                    ev.get('fecha_creacion_metadata', 'N/A'),
                    ev.get('hash_sha256', 'N/A')[:32] + '...'
                ])
            
            tabla_resultados = Table(datos_tabla, colWidths=[2*inch, 0.8*inch, 1.2*inch, 2.5*inch])
            tabla_resultados.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            elementos.append(tabla_resultados)
        else:
            elementos.append(Paragraph("No se obtuvieron evidencias derivadas.", self.styles['TextoNormal']))
        
        elementos.append(Spacer(1, 0.2*inch))
        
        # Conclusiones
        elementos.append(Paragraph("5. CONCLUSIONES", self.styles['SubtituloSeccion']))
        conclusiones = datos_dictamen.get('conclusiones', 'Sin conclusiones.')
        elementos.append(Paragraph(conclusiones, self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.3*inch))
        
        # Consumo de evidencia
        elementos.append(Paragraph("6. CONSUMO DE EVIDENCIA", self.styles['SubtituloSeccion']))
        consumo = datos_dictamen.get('consumo_evidencia', 'No se alteró la data original (solo lectura).')
        elementos.append(Paragraph(consumo, self.styles['TextoNormal']))
        elementos.append(Spacer(1, 0.5*inch))
        
        # Firma del perito
        elementos.append(Paragraph("PERITO ACTUANTE", self.styles['SubtituloSeccion']))
        datos_perito = [
            ['Nombre:', datos_dictamen.get('perito', '')],
            ['Credencial N°:', datos_dictamen.get('credencial', '')],
            ['Firma:', '___________________________'],
            ['Fecha:', datos_dictamen.get('fecha_emision', datetime.now().strftime('%Y-%m-%d'))]
        ]
        
        tabla_perito = Table(datos_perito, colWidths=[2*inch, 4*inch])
        tabla_perito.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 2), (-1, 2), 20)
        ]))
        elementos.append(tabla_perito)
        
        # Construir PDF
        doc.build(elementos)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def guardar_pdf(self, pdf_bytes: bytes, ruta_salida: str) -> bool:
        """
        Guardar PDF en archivo
        
        Args:
            pdf_bytes: Bytes del PDF
            ruta_salida: Ruta completa del archivo de salida
        
        Returns:
            True si se guardó exitosamente
        """
        try:
            ruta = Path(ruta_salida)
            ruta.parent.mkdir(parents=True, exist_ok=True)
            
            with open(ruta, 'wb') as f:
                f.write(pdf_bytes)
            
            return True
        except Exception as e:
            print(f"Error guardando PDF: {e}")
            return False


# Instancia global
print_service = PrintService()
