import fitz  # PyMuPDF
import matplotlib.pyplot as plt
import io

def gerar_relatorio_pdf(base_pdf, saida_pdf, dados_aluno):
    """
    Gera um relatório em PDF com informações do aluno, incluindo suas notas e um gráfico de desempenho.
    
    Parâmetros:
        base_pdf (str): Caminho para o arquivo PDF base que será usado como modelo.
        saida_pdf (str): Caminho onde o PDF gerado será salvo.
        dados_aluno (dict): Dicionário contendo informações do aluno, incluindo:
            - 'nome' (str): Nome do aluno.
            - 'email' (str): Email do aluno.
            - 'disciplinas' (list): Lista de dicionários com informações das disciplinas:
                - 'disciplina' (str): Nome da disciplina.
                - 'nota' (float): Nota do aluno na disciplina.
                - 'carga_horaria' (int): Carga horária da disciplina.
                - 'semestre' (int): Semestre da disciplina.
    
    Retorno:
        None: O PDF gerado é salvo no caminho especificado por saida_pdf.
    """
    # Abre o PDF modelo
    doc = fitz.open(base_pdf)
    page = doc[0]  # Pega a primeira página

    # Adicionar cabeçalho do aluno
    x_inicio, y_inicio = 100, 150
    page.insert_text((x_inicio, y_inicio), f"Nome: {dados_aluno['nome']}", fontsize=12, color=(0, 0, 0))
    page.insert_text((x_inicio, y_inicio + 20), f"Email: {dados_aluno['email']}", fontsize=12, color=(0, 0, 0))

    # Adicionar notas e informações das disciplinas
    y_pos = y_inicio + 60
    for disciplina in dados_aluno["disciplinas"]:
        texto = f"{disciplina['disciplina']} - Nota: {disciplina['nota']} - Carga Horária: {disciplina['carga_horaria']}h - Semestre: {disciplina['semestre']}"
        page.insert_text((x_inicio, y_pos), texto, fontsize=11, color=(0, 0, 0))
        y_pos += 20

    # Calcular média
    media_geral = sum(d["nota"] for d in dados_aluno["disciplinas"]) / len(dados_aluno["disciplinas"])
    page.insert_text((x_inicio, y_pos + 20), f"Média Geral: {media_geral:.2f}", fontsize=12, color=(0, 0, 0))

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(8, 4))
    disciplinas = [d["disciplina"] for d in dados_aluno["disciplinas"]]
    notas = [d["nota"] for d in dados_aluno["disciplinas"]]
    cores = ["red" if nota < 7 else "yellow" if nota == 7 else "green" for nota in notas]

    ax.bar(disciplinas, notas, color=cores, width=0.4)
    ax.set_ylabel("Nota")
    ax.set_title("Desempenho do Aluno")

    plt.xticks(rotation=30, ha="right", fontsize=10)
    plt.subplots_adjust(bottom=0.3)

    # Criar um buffer de imagem (área da memória usada para armazenar temporariamente os dados de uma imagem antes de serem processados ou salvos)
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png", bbox_inches="tight", dpi=200)
    img_buffer.seek(0)
    plt.close(fig)

    # Carregar a imagem no PyMuPDF
    img = fitz.Pixmap(img_buffer)

    # Posicionar o gráfico no PDF
    page.insert_image((x_inicio, y_pos + 70, x_inicio + 400, y_pos + 270), pixmap=img)

    # Salvar o PDF no caminho especificado
    doc.save(saida_pdf)
