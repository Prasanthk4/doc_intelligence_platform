from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import json
from typing import List, Dict

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
        )
    
    def generate_qa_report(self, chat_history: List[Dict], output_path: str):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        title = Paragraph("Document Intelligence Q&A Report", self.title_style)
        story.append(title)
        
        date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                             self.styles['Normal'])
        story.append(date_text)
        story.append(Spacer(1, 0.3*inch))
        
        for i, chat in enumerate(chat_history, 1):
            question_text = Paragraph(f"<b>Question {i}:</b> {chat['question']}", 
                                     self.styles['Heading2'])
            story.append(question_text)
            story.append(Spacer(1, 0.1*inch))
            
            answer_text = Paragraph(f"<b>Answer:</b> {chat['answer']}", 
                                   self.styles['Normal'])
            story.append(answer_text)
            story.append(Spacer(1, 0.2*inch))
            
            if 'sources' in chat and chat['sources']:
                sources_header = Paragraph("<b>Sources:</b>", self.styles['Normal'])
                story.append(sources_header)
                
                for source in chat['sources']:
                    source_text = Paragraph(
                        f"• {source['filename']} - {source['text'][:100]}...",
                        self.styles['Normal']
                    )
                    story.append(source_text)
            
            story.append(Spacer(1, 0.3*inch))
        
        doc.build(story)
        return output_path
    
    def export_to_json(self, data: Dict, output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_path
    
    def generate_analytics_report(self, analytics: Dict, entities: Dict, output_path: str):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        title = Paragraph("Document Analytics Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        metrics_data = [
            ["Metric", "Value"],
            ["Total Queries", str(analytics.get('total_queries', 0))],
            ["Avg Response Time", f"{analytics.get('avg_response_time', 0):.2f}s"],
            ["Min Response Time", f"{analytics.get('min_response_time', 0):.2f}s"],
            ["Max Response Time", f"{analytics.get('max_response_time', 0):.2f}s"],
        ]
        
        metrics_table = Table(metrics_data)
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 0.3*inch))
        
        if entities:
            entities_header = Paragraph("<b>Extracted Entities:</b>", self.styles['Heading2'])
            story.append(entities_header)
            story.append(Spacer(1, 0.1*inch))
            
            for entity_type, values in entities.items():
                if values:
                    entity_text = Paragraph(
                        f"<b>{entity_type}:</b> {', '.join([v[0] for v in values[:5]])}",
                        self.styles['Normal']
                    )
                    story.append(entity_text)
                    story.append(Spacer(1, 0.1*inch))
        
        doc.build(story)
        return output_path
