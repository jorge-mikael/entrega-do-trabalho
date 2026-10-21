from docx import Document
from docx.shared import Cm
from config.storage import Storage
import win32com.client
from pathlib import Path


def docx_to_pdf(docx_path, pdf_path):
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False

    doc = word.Documents.Open(str(docx_path))
    doc.SaveAs(str(pdf_path), FileFormat=17)  # 17 = PDF
    doc.Close(False)
    word.Quit()


def substituir_placeholders(substituicoes, caminho_saida, nome, destino):
    """Substitui os placeholders no documento."""
    def substituir_em_paragrafos(paragrafos, substituicoes):
        for paragrafo in paragrafos:
            for placeholder, substituicao in substituicoes.items():

                if placeholder in paragrafo.text:

                    if placeholder == '{{elaborador}}':
                        paragrafo.clear()
                        run = paragrafo.add_run()
                        storage = Storage(f'assinaturas/{substituicao}')
                        assinatura = storage.baixar_arquivo_temporario()
                        run.add_picture(assinatura, width=Cm(7), height=Cm(3))

                    elif placeholder == '{{aprovador}}':
                        paragrafo.clear()
                        run = paragrafo.add_run()
                        storage = Storage(f'assinaturas/{substituicao}')
                        assinatura = storage.baixar_arquivo_temporario()
                        run.add_picture(assinatura, width=Cm(7), height=Cm(3))

                    else:
                        paragrafo.text = paragrafo.text.replace(
                            placeholder,
                            substituicao
                        )


    def substituir_em_tabelas(tabelas, substituicoes):
        for tabela in tabelas:
            for linha in tabela.rows:
                for celula in linha.cells:
                    substituir_em_paragrafos(celula.paragraphs, substituicoes)

    # Abrir o documento
    storage = storage = Storage('modelos/modelo.docx')
    modelo_path = storage.baixar_arquivo_temporario()
    documento = Document(modelo_path)

    # Substituir em parágrafos do corpo principal
    substituir_em_paragrafos(documento.paragraphs, substituicoes)

    # Substituir em tabelas do corpo principal
    substituir_em_tabelas(documento.tables, substituicoes)

    # Substituir em cabeçalhos e rodapés
    for section in documento.sections:
        if section.header:
            substituir_em_paragrafos(section.header.paragraphs, substituicoes)
            substituir_em_tabelas(section.header.tables, substituicoes)
        if section.footer:
            substituir_em_paragrafos(section.footer.paragraphs, substituicoes)
            substituir_em_tabelas(section.footer.tables, substituicoes)

    # Salvar o documento editado
    documento.save(caminho_saida)

    destino_path = Path(destino)

    docx_to_pdf(caminho_saida, destino_path / (f"{nome}.pdf"))
