import os

def read_files_recursively(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                outfile.write(f"Nome do arquivo: {file_path}\n")
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                outfile.write("\n\n")  # Adiciona uma nova linha entre os conteúdos dos arquivos

def main():
    input_directory = 'backend'  # Substitua pelo caminho do seu diretório
    output_file = 'output.txt'  # Substitua pelo nome desejado para o arquivo de saída
    read_files_recursively(input_directory, output_file)
    print(f"Todo o conteúdo dos arquivos em {input_directory} foi concatenado em {output_file}")

if __name__ == "__main__":
    main()
